"""
Reef Pulse - Real NOAA Data Fetcher
Downloads actual sea surface temperature and anomaly data from NOAA Coral Reef Watch
via the ERDDAP API. Run this script once to populate the data/noaa/ folder.

Usage:
    python fetch_noaa.py
"""

import os
import sys
import time
import requests
import pandas as pd

DATA_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "data", "noaa")
os.makedirs(DATA_DIR, exist_ok=True)

ERDDAP_BASE = "https://coastwatch.pfeg.noaa.gov/erddap/griddap"
DATASET_ID = "NOAA_DHW_monthly"
VARIABLES = ["sea_surface_temperature", "sea_surface_temperature_anomaly"]

# Reef regions with bounding boxes [south_lat, north_lat, west_lon, east_lon]
REGIONS = {
    "great_barrier_reef": {"name": "Great Barrier Reef", "bbox": [-24.0, -10.0, 142.0, 155.0]},
    "coral_triangle": {"name": "Coral Triangle", "bbox": [-10.0, 15.0, 115.0, 155.0]},
    "caribbean": {"name": "Caribbean", "bbox": [10.0, 26.0, -90.0, -60.0]},
    "indian_ocean": {"name": "Indian Ocean", "bbox": [-15.0, 12.0, 39.0, 75.0]},
    "red_sea": {"name": "Red Sea", "bbox": [10.0, 28.0, 32.0, 44.0]},
    "central_pacific": {"name": "Central Pacific", "bbox": [-25.0, 10.0, 130.0, 180.0]},
    "eastern_pacific": {"name": "Eastern Pacific", "bbox": [-5.0, 12.0, -92.0, -77.0]},
}

START_YEAR = 2015
END_YEAR = 2025

# Use a large stride to keep data manageable (every 10th lat/lon point)
STRIDE = 10


def download_region(key, info):
    """Download NOAA CRW monthly SST data for a region."""
    name = info["name"]
    south, north, west, east = info["bbox"]

    print(f"\n{'='*60}")
    print(f"  Downloading: {name}")
    print(f"  Bounding box: [{south}, {north}, {west}, {east}]")
    print(f"{'='*60}")

    time_start = f"{START_YEAR}-01-01T00:00:00Z"
    time_end = f"{END_YEAR}-12-31T00:00:00Z"

    # Build ERDDAP URL with stride to reduce data volume
    dim = f"[({time_start}):1:({time_end})][({south}):{STRIDE}:({north})][({west}):{STRIDE}:({east})]"
    var_parts = [f"{v}{dim}" for v in VARIABLES]
    url = f"{ERDDAP_BASE}/{DATASET_ID}.csv?{','.join(var_parts)}"

    print(f"  Requesting data (this may take 30-60 seconds)...")

    try:
        response = requests.get(url, timeout=300)
        response.raise_for_status()

        output_file = os.path.join(DATA_DIR, f"{key}_sst_monthly.csv")
        with open(output_file, "w") as f:
            f.write(response.text)

        # Parse and summarize
        lines = response.text.strip().split("\n")
        data_rows = len(lines) - 2  # subtract header and units rows
        print(f"  Downloaded {data_rows:,} data points")
        print(f"  Saved to: {output_file}")
        return True

    except requests.exceptions.HTTPError as e:
        print(f"  HTTP Error: {e}")
        if response is not None:
            print(f"  Response: {response.text[:300]}")
        return False
    except requests.exceptions.Timeout:
        print(f"  Timed out. Try again or reduce the region size.")
        return False
    except Exception as e:
        print(f"  Failed: {e}")
        return False


def process_downloaded_data():
    """Process raw NOAA CSVs into a clean combined dataset."""
    print(f"\n{'='*60}")
    print("  Processing downloaded data...")
    print(f"{'='*60}")

    all_rows = []
    for key, info in REGIONS.items():
        filepath = os.path.join(DATA_DIR, f"{key}_sst_monthly.csv")
        if not os.path.exists(filepath):
            print(f"  Skipping {info['name']} (no data file)")
            continue

        try:
            # ERDDAP CSVs have a units row after the header — skip it
            df = pd.read_csv(filepath, skiprows=[1])
            df["region"] = info["name"]

            # Rename columns to standard names
            col_map = {}
            for col in df.columns:
                if "sea_surface_temperature_anomaly" in col.lower():
                    col_map[col] = "sst_anomaly"
                elif "sea_surface_temperature" in col.lower():
                    col_map[col] = "sst_celsius"
                elif "time" in col.lower():
                    col_map[col] = "date"
                elif "latitude" in col.lower():
                    col_map[col] = "latitude"
                elif "longitude" in col.lower():
                    col_map[col] = "longitude"
            df = df.rename(columns=col_map)

            # Compute regional monthly averages
            if "date" in df.columns and "sst_celsius" in df.columns:
                df["date"] = pd.to_datetime(df["date"])
                monthly = df.groupby([pd.Grouper(key="date", freq="MS"), "region"]).agg(
                    sst_celsius=("sst_celsius", "mean"),
                    sst_anomaly=("sst_anomaly", "mean"),
                ).reset_index()
                all_rows.append(monthly)
                print(f"  Processed {info['name']}: {len(monthly)} monthly records")

        except Exception as e:
            print(f"  Error processing {info['name']}: {e}")

    if all_rows:
        combined = pd.concat(all_rows, ignore_index=True)
        combined = combined.round(3)
        output = os.path.join(os.path.dirname(DATA_DIR), "noaa_real_sst.csv")
        combined.to_csv(output, index=False)
        print(f"\n  Combined dataset: {len(combined)} rows")
        print(f"  Saved to: {output}")
        return True
    else:
        print("\n  No data to process.")
        return False


def main():
    print("=" * 60)
    print("  REEF PULSE - NOAA Real Data Fetcher")
    print(f"  Period: {START_YEAR} to {END_YEAR}")
    print(f"  Regions: {len(REGIONS)}")
    print("=" * 60)

    results = {}
    for key, info in REGIONS.items():
        results[key] = download_region(key, info)
        time.sleep(2)  # Be polite to NOAA's servers

    print(f"\n{'='*60}")
    print("  DOWNLOAD SUMMARY")
    print(f"{'='*60}")
    for key, success in results.items():
        status = "OK" if success else "FAILED"
        print(f"  {status} - {REGIONS[key]['name']}")

    successful = sum(1 for s in results.values() if s)
    print(f"\n  {successful}/{len(results)} regions downloaded")

    if successful > 0:
        process_downloaded_data()

    print(f"\n{'='*60}")
    print("  Done! Run the dashboard: streamlit run app.py")
    print("=" * 60)


if __name__ == "__main__":
    main()
