"""
Reef Pulse - Data Generator v3
Creates curated datasets including reef connectivity data.
Run this once before launching the dashboard.
"""

import pandas as pd
import numpy as np
import os

np.random.seed(42)
DATA_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "data")
os.makedirs(DATA_DIR, exist_ok=True)


def generate_reef_sites():
    sites = [
        ("GBR-N", "Northern GBR", "Great Barrier Reef", "Australia", -14.5, 145.5, 11500, "Barrier", 22, 18, "Critical"),
        ("GBR-C", "Central GBR", "Great Barrier Reef", "Australia", -18.2, 147.5, 14200, "Barrier", 35, 28, "Threatened"),
        ("GBR-S", "Southern GBR", "Great Barrier Reef", "Australia", -22.0, 152.0, 8900, "Barrier", 42, 36, "Moderate"),
        ("GBR-CS", "Coral Sea Reefs", "Great Barrier Reef", "Australia", -16.0, 150.0, 3200, "Platform", 48, 42, "Fair"),
        ("CT-RI", "Raja Ampat", "Coral Triangle", "Indonesia", -0.5, 130.5, 4500, "Fringing", 65, 58, "Good"),
        ("CT-BI", "Bunaken", "Coral Triangle", "Indonesia", 1.6, 124.8, 890, "Fringing", 55, 48, "Fair"),
        ("CT-WI", "Wakatobi", "Coral Triangle", "Indonesia", -5.5, 123.8, 1390, "Atoll", 52, 44, "Fair"),
        ("CT-KI", "Komodo", "Coral Triangle", "Indonesia", -8.5, 119.5, 1720, "Fringing", 48, 40, "Moderate"),
        ("CT-TP", "Tubbataha", "Coral Triangle", "Philippines", 8.9, 119.9, 970, "Atoll", 58, 52, "Good"),
        ("CT-AP", "Apo Reef", "Coral Triangle", "Philippines", 12.7, 120.5, 340, "Atoll", 45, 38, "Moderate"),
        ("CT-VP", "Verde Island Passage", "Coral Triangle", "Philippines", 13.5, 121.0, 1100, "Fringing", 50, 43, "Fair"),
        ("CT-PNG", "Kimbe Bay", "Coral Triangle", "Papua New Guinea", -5.4, 150.1, 2800, "Fringing", 60, 55, "Good"),
        ("CT-MY", "Sipadan", "Coral Triangle", "Malaysia", 4.1, 118.6, 120, "Fringing", 55, 50, "Good"),
        ("CB-BZ", "Belize Barrier Reef", "Caribbean", "Belize", 17.5, -87.8, 960, "Barrier", 28, 20, "Threatened"),
        ("CB-BN", "Bonaire Reef", "Caribbean", "Bonaire", 12.2, -68.3, 270, "Fringing", 38, 32, "Moderate"),
        ("CB-FK", "Florida Keys", "Caribbean", "USA", 24.6, -81.6, 1430, "Barrier", 18, 12, "Critical"),
        ("CB-CR", "Cozumel", "Caribbean", "Mexico", 20.4, -87.0, 350, "Fringing", 32, 25, "Threatened"),
        ("CB-VI", "US Virgin Islands", "Caribbean", "USA", 18.3, -64.9, 140, "Fringing", 24, 16, "Threatened"),
        ("CB-CY", "Cayman Islands", "Caribbean", "Cayman Islands", 19.3, -81.4, 220, "Fringing", 30, 22, "Threatened"),
        ("CB-JM", "Jamaica North Coast", "Caribbean", "Jamaica", 18.5, -77.8, 180, "Fringing", 15, 10, "Critical"),
        ("CB-CU", "Jardines de la Reina", "Caribbean", "Cuba", 21.5, -79.0, 2170, "Barrier", 52, 48, "Good"),
        ("IO-MV", "Maldives Central Atolls", "Indian Ocean", "Maldives", 4.2, 73.5, 4500, "Atoll", 35, 24, "Threatened"),
        ("IO-SC", "Seychelles Inner Islands", "Indian Ocean", "Seychelles", -4.6, 55.5, 1700, "Granitic", 30, 22, "Threatened"),
        ("IO-LK", "Lakshadweep", "Indian Ocean", "India", 10.6, 72.6, 430, "Atoll", 42, 38, "Moderate"),
        ("IO-MZ", "Mozambique Channel", "Indian Ocean", "Mozambique", -12.5, 40.5, 1900, "Fringing", 38, 32, "Moderate"),
        ("IO-MG", "NE Madagascar", "Indian Ocean", "Madagascar", -13.0, 49.5, 2400, "Fringing", 40, 34, "Moderate"),
        ("IO-RU", "Reunion", "Indian Ocean", "France", -21.1, 55.5, 120, "Fringing", 28, 20, "Threatened"),
        ("IO-CH", "Chagos Archipelago", "Indian Ocean", "BIOT", -6.5, 71.5, 3600, "Atoll", 55, 48, "Fair"),
        ("RS-EG", "Egyptian Red Sea", "Red Sea", "Egypt", 24.5, 35.5, 3800, "Fringing", 55, 52, "Good"),
        ("RS-SA", "Saudi Arabian Reefs", "Red Sea", "Saudi Arabia", 22.0, 38.5, 2600, "Fringing", 50, 47, "Good"),
        ("RS-SD", "Sudanese Reefs", "Red Sea", "Sudan", 19.5, 37.5, 1800, "Fringing", 58, 55, "Good"),
        ("RS-DJ", "Djibouti Gulf", "Red Sea", "Djibouti", 11.5, 43.2, 350, "Fringing", 35, 30, "Moderate"),
        ("CP-HI", "Hawaiian Islands", "Central Pacific", "USA", 21.0, -157.0, 1660, "Fringing", 32, 26, "Threatened"),
        ("CP-FP", "French Polynesia", "Central Pacific", "France", -17.5, -149.5, 6200, "Atoll", 45, 40, "Moderate"),
        ("CP-FJ", "Fiji Great Reef", "Central Pacific", "Fiji", -17.8, 177.0, 3900, "Barrier", 42, 36, "Moderate"),
        ("CP-SM", "Samoa", "Central Pacific", "Samoa", -13.8, -172.0, 490, "Fringing", 38, 32, "Moderate"),
        ("CP-PW", "Palau", "Central Pacific", "Palau", 7.5, 134.5, 1400, "Barrier", 55, 50, "Good"),
        ("CP-NC", "New Caledonia", "Central Pacific", "France", -22.3, 166.5, 4500, "Barrier", 48, 44, "Fair"),
        ("CP-MS", "Marshall Islands", "Central Pacific", "Marshall Islands", 7.1, 171.4, 2100, "Atoll", 40, 34, "Moderate"),
        ("EP-GI", "Galapagos Islands", "Eastern Pacific", "Ecuador", -0.9, -89.6, 280, "Fringing", 20, 15, "Critical"),
        ("EP-CR", "Costa Rica Pacific", "Eastern Pacific", "Costa Rica", 8.7, -83.5, 160, "Fringing", 25, 20, "Threatened"),
        ("EP-PA", "Panama Gulf", "Eastern Pacific", "Panama", 7.5, -78.5, 320, "Fringing", 30, 25, "Threatened"),
    ]
    df = pd.DataFrame(sites, columns=["site_id", "name", "region", "country", "lat", "lon", "area_km2",
        "reef_type", "coral_cover_2015", "coral_cover_2024", "health_status"])
    df["cover_change_pct"] = ((df["coral_cover_2024"] - df["coral_cover_2015"]) / df["coral_cover_2015"] * 100).round(1)
    df["protection_level"] = np.random.choice(
        ["Marine Protected Area", "World Heritage Site", "National Park", "Partial Protection", "Unprotected"],
        size=len(df), p=[0.25, 0.1, 0.15, 0.25, 0.25])
    df.to_csv(os.path.join(DATA_DIR, "reef_sites.csv"), index=False)
    print(f"Created reef_sites.csv ({len(df)} sites)")
    return df


def generate_bleaching_timeseries(reef_df):
    regions = reef_df["region"].unique()
    dates = pd.date_range("2000-01-01", "2025-12-01", freq="MS")
    rows = []
    for region in regions:
        base_sst = {"Great Barrier Reef": 26.5, "Coral Triangle": 28.5, "Caribbean": 27.5,
                     "Indian Ocean": 28.0, "Red Sea": 27.0, "Central Pacific": 27.5, "Eastern Pacific": 26.0}.get(region, 27.0)
        bleaching_threshold = base_sst + 1.5
        for date in dates:
            year, month = date.year, date.month
            if region in ["Great Barrier Reef", "Central Pacific", "Eastern Pacific"]:
                seasonal = 1.8 * np.sin(2 * np.pi * (month - 1) / 12)
            else:
                seasonal = 1.8 * np.sin(2 * np.pi * (month - 7) / 12)
            warming = 0.015 * (year - 2000)
            enso = 0
            if year == 2010 and month in [6, 7, 8, 9, 10]: enso = 0.6
            elif year in [2015, 2016] and month in [1, 2, 3, 4, 5, 11, 12]: enso = 1.0
            elif year in [2023, 2024]: enso = 0.8 + 0.3 * np.sin(2 * np.pi * (month - 3) / 12)
            elif year == 2025: enso = 0.4
            noise = np.random.normal(0, 0.3)
            sst = base_sst + seasonal + warming + enso + noise
            anomaly = sst - base_sst - seasonal
            hotspot = max(0, sst - bleaching_threshold)
            dhw = hotspot * 4 * max(0, 1 + np.random.normal(0, 0.3))
            if dhw >= 8: bleach_pct, alert = min(90, 40 + dhw * 4 + np.random.normal(0, 10)), 2
            elif dhw >= 4: bleach_pct, alert = min(60, 15 + dhw * 5 + np.random.normal(0, 8)), 1
            elif dhw >= 1: bleach_pct, alert = max(0, dhw * 3 + np.random.normal(0, 5)), 0.5
            else: bleach_pct, alert = max(0, np.random.normal(1, 1)), 0
            bleach_pct = max(0, min(100, bleach_pct))
            rows.append({"date": date.strftime("%Y-%m-%d"), "region": region, "sst_celsius": round(sst, 2),
                          "sst_anomaly": round(anomaly, 2), "dhw": round(max(0, dhw), 1),
                          "bleaching_pct": round(bleach_pct, 1), "alert_level": alert, "bleaching_threshold": bleaching_threshold})
    df = pd.DataFrame(rows)
    df.to_csv(os.path.join(DATA_DIR, "bleaching_timeseries.csv"), index=False)
    print(f"Created bleaching_timeseries.csv ({len(df)} rows)")
    return df


def generate_species_data():
    species = [("Great Barrier Reef", 400, 120, 1625, 5000, 48, 8.5), ("Coral Triangle", 605, 180, 2228, 7500, 72, 12.0),
        ("Caribbean", 65, 35, 500, 1400, 38, 22.0), ("Indian Ocean", 310, 100, 1200, 3800, 52, 9.0),
        ("Red Sea", 260, 60, 800, 2200, 18, 15.0), ("Central Pacific", 350, 90, 1100, 3200, 42, 11.0),
        ("Eastern Pacific", 40, 15, 450, 900, 22, 18.0)]
    df = pd.DataFrame(species, columns=["region", "hard_coral_species", "soft_coral_species",
        "reef_fish_species", "invertebrate_species", "threatened_species", "endemic_pct"])
    df["total_species"] = df["hard_coral_species"] + df["soft_coral_species"] + df["reef_fish_species"] + df["invertebrate_species"]
    df.to_csv(os.path.join(DATA_DIR, "species_biodiversity.csv"), index=False)
    print(f"Created species_biodiversity.csv ({len(df)} regions)")


def generate_economic_data():
    econ = [("Australia", "Great Barrier Reef", 34440, 5200, 1800, 3100, 6.4, 0.3),
        ("Indonesia", "Coral Triangle", 51020, 3400, 5200, 4800, 12.0, 1.2),
        ("Philippines", "Coral Triangle", 25060, 1800, 3600, 2900, 8.5, 0.9),
        ("Papua New Guinea", "Coral Triangle", 13840, 420, 1800, 1200, 3.2, 2.8),
        ("Malaysia", "Coral Triangle", 4006, 980, 1200, 1500, 2.1, 0.4),
        ("Belize", "Caribbean", 1400, 650, 280, 420, 0.19, 12.0),
        ("Mexico", "Caribbean", 2800, 2100, 480, 650, 1.5, 0.2),
        ("USA (Florida)", "Caribbean", 6300, 4200, 320, 1800, 0.5, 0.01),
        ("Jamaica", "Caribbean", 900, 680, 340, 280, 0.4, 2.5),
        ("Cuba", "Caribbean", 3020, 450, 520, 380, 0.8, 0.5),
        ("Maldives", "Indian Ocean", 900, 3200, 180, 820, 0.38, 70.0),
        ("Seychelles", "Indian Ocean", 1690, 420, 95, 280, 0.08, 55.0),
        ("Mozambique", "Indian Ocean", 1860, 180, 680, 340, 4.2, 1.8),
        ("Madagascar", "Indian Ocean", 2230, 120, 540, 280, 3.8, 1.2),
        ("India", "Indian Ocean", 5790, 280, 1200, 1800, 6.5, 0.05),
        ("Egypt", "Red Sea", 3800, 2800, 180, 520, 1.2, 0.8),
        ("Saudi Arabia", "Red Sea", 2600, 680, 120, 380, 0.3, 0.02),
        ("Fiji", "Central Pacific", 3900, 580, 380, 450, 0.45, 8.5),
        ("French Polynesia", "Central Pacific", 6200, 420, 120, 280, 0.18, 4.2),
        ("Palau", "Central Pacific", 1400, 180, 45, 320, 0.018, 42.0),
        ("Ecuador", "Eastern Pacific", 280, 85, 42, 120, 0.12, 0.01),
        ("Costa Rica", "Eastern Pacific", 160, 120, 28, 65, 0.08, 0.06),
        ("Panama", "Eastern Pacific", 320, 95, 38, 85, 0.1, 0.04)]
    df = pd.DataFrame(econ, columns=["country", "region", "reef_area_km2", "tourism_revenue_m_usd",
        "fisheries_revenue_m_usd", "coastal_protection_m_usd", "people_dependent_millions", "gdp_reef_pct"])
    df["total_value_m_usd"] = df["tourism_revenue_m_usd"] + df["fisheries_revenue_m_usd"] + df["coastal_protection_m_usd"]
    df.to_csv(os.path.join(DATA_DIR, "economic_impact.csv"), index=False)
    print(f"Created economic_impact.csv ({len(df)} countries)")


def generate_bleaching_events():
    events = [(1998, "1st Global Bleaching Event", "Severe", 16, "Indian Ocean, Pacific, Caribbean", 8, 10),
        (2002, "GBR Mass Bleaching", "Moderate", 5, "Great Barrier Reef", 4, 6),
        (2005, "Caribbean Bleaching", "Severe", 8, "Caribbean", 6, 8),
        (2010, "2nd Global Bleaching Event", "Severe", 12, "Indian Ocean, SE Asia, Caribbean", 7, 8),
        (2014, "3rd Global Bleaching Begins", "Moderate", 10, "Pacific, Indian Ocean", 5, 6),
        (2015, "3rd Global Bleaching Peak 1", "Severe", 38, "Pacific, Indian Ocean, Caribbean", 14, 5),
        (2016, "3rd Global Bleaching Peak 2", "Extreme", 56, "Great Barrier Reef, Pacific, Indian Ocean", 12, 7),
        (2017, "3rd Global Bleaching Final", "Severe", 45, "Great Barrier Reef, Caribbean", 8, 6),
        (2020, "GBR Mass Bleaching 2020", "Moderate", 8, "Great Barrier Reef", 4, 4),
        (2022, "GBR Mass Bleaching 2022", "Severe", 12, "Great Barrier Reef", 5, 4),
        (2023, "4th Global Bleaching Begins", "Extreme", 54, "Global - all ocean basins", 18, 0),
        (2024, "4th Global Bleaching Peak", "Extreme", 62, "Global - worst recorded", 12, 0),
        (2025, "4th Global Bleaching Ongoing", "Severe", 48, "Pacific, Indian Ocean, Caribbean", 0, 0)]
    df = pd.DataFrame(events, columns=["year", "event_name", "severity", "pct_reefs_affected",
        "regions_affected", "duration_months", "est_recovery_years"])
    df.to_csv(os.path.join(DATA_DIR, "bleaching_events.csv"), index=False)
    print(f"Created bleaching_events.csv ({len(df)} events)")


def generate_coral_cover_trends():
    regions = ["Great Barrier Reef", "Coral Triangle", "Caribbean", "Indian Ocean", "Red Sea", "Central Pacific", "Eastern Pacific"]
    years = list(range(1980, 2026)); rows = []
    for region in regions:
        base = {"Great Barrier Reef": 55, "Coral Triangle": 60, "Caribbean": 50, "Indian Ocean": 50,
                "Red Sea": 55, "Central Pacific": 50, "Eastern Pacific": 35}[region]
        cover = base
        for year in years:
            decline = -0.3 + np.random.normal(0, 0.5)
            if year == 1998: decline -= 5 + np.random.normal(0, 2)
            elif year == 2010: decline -= 3 + np.random.normal(0, 1.5)
            elif year in [2015, 2016]: decline -= 6 + np.random.normal(0, 2)
            elif year in [2023, 2024]: decline -= 7 + np.random.normal(0, 2)
            if region == "Caribbean" and year < 2005: decline -= 0.8
            if region == "Red Sea": decline *= 0.5
            if year in [2000, 2001, 2005, 2006, 2012, 2013, 2018, 2019]: decline += 1.5 + np.random.normal(0, 0.5)
            cover = max(5, min(70, cover + decline))
            rows.append({"year": year, "region": region, "coral_cover_pct": round(cover, 1)})
    pd.DataFrame(rows).to_csv(os.path.join(DATA_DIR, "coral_cover_trends.csv"), index=False)
    print(f"Created coral_cover_trends.csv ({len(rows)} rows)")


def generate_risk_scores(reef_df):
    rows = []
    for _, site in reef_df.iterrows():
        cover_loss = site["coral_cover_2015"] - site["coral_cover_2024"]
        thermal_raw = min(100, max(0, cover_loss * 4 + np.random.normal(10, 8)))
        decline_rate = abs(site["cover_change_pct"])
        trajectory_raw = min(100, max(0, decline_rate * 2.5 + np.random.normal(5, 8)))
        cover_risk = min(100, max(0, 100 - site["coral_cover_2024"] * 1.5 + np.random.normal(0, 5)))
        prot_map = {"World Heritage Site": 15, "Marine Protected Area": 25, "National Park": 30, "Partial Protection": 55, "Unprotected": 80}
        protection_raw = min(100, max(0, prot_map.get(site["protection_level"], 50) + np.random.normal(0, 8)))
        region_p = {"Caribbean": 65, "Eastern Pacific": 55, "Great Barrier Reef": 45, "Indian Ocean": 50,
                    "Coral Triangle": 55, "Central Pacific": 40, "Red Sea": 35}
        human_pressure = min(100, max(0, region_p.get(site["region"], 45) + np.random.normal(0, 12)))
        composite = thermal_raw * 0.25 + trajectory_raw * 0.20 + cover_risk * 0.25 + protection_raw * 0.15 + human_pressure * 0.15
        composite = min(100, max(0, composite))
        if composite >= 70: tier = "Critical"
        elif composite >= 55: tier = "High"
        elif composite >= 40: tier = "Elevated"
        elif composite >= 25: tier = "Moderate"
        else: tier = "Low"
        rows.append({"site_id": site["site_id"], "name": site["name"], "region": site["region"], "country": site["country"],
            "lat": site["lat"], "lon": site["lon"], "coral_cover_2024": site["coral_cover_2024"],
            "cover_change_pct": site["cover_change_pct"], "protection_level": site["protection_level"],
            "thermal_stress_score": round(thermal_raw, 1), "trajectory_score": round(trajectory_raw, 1),
            "cover_risk_score": round(cover_risk, 1), "protection_score": round(protection_raw, 1),
            "human_pressure_score": round(human_pressure, 1), "composite_risk_score": round(composite, 1), "risk_tier": tier})
    df = pd.DataFrame(rows)
    df.to_csv(os.path.join(DATA_DIR, "risk_scores.csv"), index=False)
    print(f"Created risk_scores.csv ({len(df)} sites)")


def generate_climate_projections():
    regions = ["Great Barrier Reef", "Coral Triangle", "Caribbean", "Indian Ocean", "Red Sea", "Central Pacific", "Eastern Pacific"]
    scenarios = [("1.5C", 1.5), ("2.0C", 2.0), ("3.0C", 3.0)]
    years = list(range(2025, 2056)); rows = []
    for region in regions:
        base_cover = {"Great Barrier Reef": 26, "Coral Triangle": 48, "Caribbean": 18, "Indian Ocean": 30,
                      "Red Sea": 50, "Central Pacific": 38, "Eastern Pacific": 20}[region]
        sensitivity = {"Great Barrier Reef": 1.0, "Coral Triangle": 0.7, "Caribbean": 1.3, "Indian Ocean": 0.9,
                       "Red Sea": 0.5, "Central Pacific": 0.85, "Eastern Pacific": 1.2}[region]
        for sc_id, wt in scenarios:
            cover = base_cover
            for year in years:
                progress = (year - 2025) / 30
                if wt == 1.5: ti = 1.1 + 0.4 * (1 - np.exp(-3 * progress))
                elif wt == 2.0: ti = 1.1 + 0.9 * progress
                else: ti = 1.1 + 1.9 * progress ** 0.8
                ad = sensitivity * (ti - 1.0) * (0.8 + np.random.normal(0, 0.2))
                bp = min(0.9, 0.1 + (ti - 1.0) * 0.3 * sensitivity)
                if np.random.random() < bp: ad += sensitivity * (ti - 0.8) * np.random.uniform(1.5, 4.0)
                recovery = max(0, (cover / 100) * np.random.uniform(0.3, 1.2))
                cover = max(2, cover - ad + recovery * 0.3)
                bf = min(9, max(0.5, bp * 10))
                elp = max(0, (1 - cover / base_cover) * 100)
                rows.append({"year": year, "region": region, "scenario": sc_id, "warming_c": round(ti, 2),
                    "projected_cover_pct": round(max(2, cover), 1), "bleaching_freq_per_decade": round(bf, 1),
                    "economic_loss_pct": round(min(95, elp), 1)})
    pd.DataFrame(rows).to_csv(os.path.join(DATA_DIR, "climate_projections.csv"), index=False)
    print(f"Created climate_projections.csv ({len(rows)} rows)")


def generate_connectivity_data(reef_df):
    """Generate ocean current-based larval connectivity data between reef sites."""
    # Major ocean current systems that connect reefs
    currents = [
        {"name": "East Australian Current", "region": "Great Barrier Reef",
         "points": [(-12, 144), (-15, 146), (-18, 148), (-22, 152), (-26, 154)],
         "speed_km_day": 80, "direction": "Southward"},
        {"name": "Indonesian Throughflow", "region": "Coral Triangle",
         "points": [(5, 120), (2, 122), (-1, 124), (-4, 126), (-8, 120)],
         "speed_km_day": 45, "direction": "Southward"},
        {"name": "North Equatorial Current", "region": "Coral Triangle",
         "points": [(8, 135), (8, 140), (7, 145), (6, 150)],
         "speed_km_day": 35, "direction": "Westward"},
        {"name": "Caribbean Current", "region": "Caribbean",
         "points": [(12, -68), (14, -72), (16, -76), (18, -80), (20, -84), (22, -86)],
         "speed_km_day": 55, "direction": "Westward/Northward"},
        {"name": "Gulf Stream (origin)", "region": "Caribbean",
         "points": [(22, -86), (24, -83), (25, -80), (26, -79)],
         "speed_km_day": 100, "direction": "Northward"},
        {"name": "South Equatorial Current (Indian)", "region": "Indian Ocean",
         "points": [(-8, 72), (-9, 65), (-10, 58), (-11, 50), (-12, 42)],
         "speed_km_day": 40, "direction": "Westward"},
        {"name": "Somali Current", "region": "Indian Ocean",
         "points": [(-2, 42), (2, 44), (6, 47), (10, 52)],
         "speed_km_day": 60, "direction": "Northward (monsoon)"},
        {"name": "Red Sea Circulation", "region": "Red Sea",
         "points": [(12, 43), (16, 40), (19, 38), (22, 37), (25, 36)],
         "speed_km_day": 20, "direction": "Northward"},
        {"name": "South Equatorial Current (Pacific)", "region": "Central Pacific",
         "points": [(-15, 180), (-15, 170), (-14, 160), (-12, 150), (-10, 140)],
         "speed_km_day": 35, "direction": "Westward"},
        {"name": "Equatorial Undercurrent", "region": "Eastern Pacific",
         "points": [(0, -92), (0, -88), (0, -84), (0, -80)],
         "speed_km_day": 50, "direction": "Eastward"},
    ]

    current_rows = []
    for c in currents:
        for i, (lat, lon) in enumerate(c["points"]):
            current_rows.append({
                "current_name": c["name"], "region": c["region"],
                "point_order": i, "lat": lat, "lon": lon,
                "speed_km_day": c["speed_km_day"], "direction": c["direction"]
            })
    current_df = pd.DataFrame(current_rows)
    current_df.to_csv(os.path.join(DATA_DIR, "ocean_currents.csv"), index=False)
    print(f"Created ocean_currents.csv ({len(current_df)} points)")

    # Generate larval connectivity links between nearby reefs
    connections = []
    sites = reef_df.to_dict("records")
    for i, src in enumerate(sites):
        for j, dst in enumerate(sites):
            if i == j: continue
            if src["region"] != dst["region"]: continue

            # Distance (rough approximation)
            dlat = abs(src["lat"] - dst["lat"])
            dlon = abs(src["lon"] - dst["lon"])
            dist = np.sqrt(dlat**2 + dlon**2) * 111  # rough km

            # Only connect reefs within 1500km in same region
            if dist > 1500: continue

            # Connectivity strength decreases with distance
            strength = max(0, 1 - (dist / 1500)) * np.random.uniform(0.3, 1.0)
            if strength < 0.1: continue

            # Larval duration and survival
            larval_days = int(dist / np.random.uniform(20, 60))
            survival_pct = max(1, 100 * np.exp(-0.15 * larval_days))

            # Source health affects larval supply
            larval_supply = src["coral_cover_2024"] / 100 * strength

            connections.append({
                "source_id": src["site_id"], "source_name": src["name"],
                "target_id": dst["site_id"], "target_name": dst["name"],
                "region": src["region"],
                "source_lat": src["lat"], "source_lon": src["lon"],
                "target_lat": dst["lat"], "target_lon": dst["lon"],
                "distance_km": round(dist, 0),
                "connectivity_strength": round(strength, 3),
                "larval_duration_days": larval_days,
                "larval_survival_pct": round(survival_pct, 1),
                "effective_larval_supply": round(larval_supply, 3),
            })

    conn_df = pd.DataFrame(connections)
    conn_df.to_csv(os.path.join(DATA_DIR, "reef_connectivity.csv"), index=False)
    print(f"Created reef_connectivity.csv ({len(conn_df)} connections)")

    return current_df, conn_df


def generate_sst_heatmap_data():
    """Generate gridded SST anomaly data for animated heatmap visualization."""
    # Create a grid of points across tropical oceans
    lats = np.arange(-30, 31, 2.5)
    lons = np.arange(-180, 181, 5)
    years = [2015, 2016, 2017, 2018, 2019, 2020, 2021, 2022, 2023, 2024]

    rows = []
    for year in years:
        # Global warming trend
        warming = 0.015 * (year - 2000)

        # El Nino years get extra warming
        enso = 0
        if year in [2015, 2016]: enso = 0.8
        elif year in [2023, 2024]: enso = 1.0

        for lat in lats:
            for lon in lons:
                # Base anomaly from warming + ENSO
                base_anom = warming + enso

                # Tropical waters warm more
                lat_factor = max(0, 1 - abs(lat) / 35)
                anom = base_anom * lat_factor

                # Regional hotspots during El Nino
                if enso > 0:
                    # Central Pacific hotspot
                    if -10 < lat < 10 and -170 < lon < -100:
                        anom += enso * 0.6
                    # Indian Ocean
                    if -15 < lat < 15 and 40 < lon < 80:
                        anom += enso * 0.4
                    # Caribbean
                    if 10 < lat < 25 and -90 < lon < -60:
                        anom += enso * 0.5
                    # Coral Triangle
                    if -10 < lat < 10 and 110 < lon < 160:
                        anom += enso * 0.3

                # Add noise
                anom += np.random.normal(0, 0.15)

                # Skip land areas (very rough mask)
                is_ocean = True
                if -60 < lon < -35 and -35 < lat < 10: is_ocean = False  # South America
                if -20 < lon < 55 and -35 < lat < 35: is_ocean = False  # Africa
                if 60 < lon < 140 and 10 < lat < 35: is_ocean = False  # Asia

                if is_ocean and lat_factor > 0.1:
                    rows.append({"year": year, "lat": lat, "lon": lon, "sst_anomaly": round(anom, 3)})

    df = pd.DataFrame(rows)
    df.to_csv(os.path.join(DATA_DIR, "sst_heatmap.csv"), index=False)
    print(f"Created sst_heatmap.csv ({len(df)} grid points)")


if __name__ == "__main__":
    print("=" * 50)
    print("REEF PULSE v3 - Generating Dashboard Data")
    print("=" * 50)
    print()
    reef_df = generate_reef_sites()
    generate_bleaching_timeseries(reef_df)
    generate_species_data()
    generate_economic_data()
    generate_bleaching_events()
    generate_coral_cover_trends()
    generate_risk_scores(reef_df)
    generate_climate_projections()
    generate_connectivity_data(reef_df)
    generate_sst_heatmap_data()
    print()
    print("=" * 50)
    print("All data files created in ./data/")
    print("Optional: Run fetch_noaa.py to download real NOAA data")
    print("Then run: streamlit run app.py")
    print("=" * 50)
