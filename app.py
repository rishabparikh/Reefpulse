"""
REEF PULSE v3 - Global Coral Reef Intelligence Dashboard
"""

import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
import os

st.set_page_config(page_title="Reef Pulse", page_icon="🪸", layout="wide", initial_sidebar_state="expanded")

st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=EB+Garamond:ital,wght@0,400;0,500;0,600;0,700;0,800;1,400;1,500&display=swap');
    .stApp { background: #ffffff; color: #1a2a3a; font-family: 'EB Garamond', 'Garamond', 'Georgia', serif !important; }
    .stApp > div { font-family: 'EB Garamond', 'Garamond', 'Georgia', serif !important; }
    section[data-testid="stSidebar"] { background: #f5f8fb; border-right: 1px solid #dce6f0; }
    section[data-testid="stSidebar"] .stMarkdown p, section[data-testid="stSidebar"] .stMarkdown li { color: #4a6070; }
    h1, h2, h3 { font-family: 'EB Garamond', serif !important; color: #0f2030 !important; }
    h1 { font-weight: 700 !important; font-size: 2.4rem !important; }
    h3 { font-weight: 600 !important; font-size: 1.4rem !important; }
    div[data-testid="stMetric"] { background: #f5f8fb; border: 1px solid #dce6f0; border-radius: 12px; padding: 16px 20px; }
    div[data-testid="stMetric"] label { color: #5a7080 !important; font-size: 0.85rem !important; text-transform: uppercase; letter-spacing: 1.2px; }
    div[data-testid="stMetric"] div[data-testid="stMetricValue"] { color: #0a8f6e !important; font-weight: 700 !important; font-size: 1.8rem !important; }
    hr { border: none; border-top: 1px solid #e0e8f0; margin: 2rem 0; }
    #MainMenu {visibility: hidden;} footer {visibility: hidden;}
</style>
""", unsafe_allow_html=True)

DATA_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "data")

@st.cache_data
def load_data():
    d = {
        "sites": pd.read_csv(os.path.join(DATA_DIR, "reef_sites.csv")),
        "bleaching": pd.read_csv(os.path.join(DATA_DIR, "bleaching_timeseries.csv")),
        "species": pd.read_csv(os.path.join(DATA_DIR, "species_biodiversity.csv")),
        "economic": pd.read_csv(os.path.join(DATA_DIR, "economic_impact.csv")),
        "events": pd.read_csv(os.path.join(DATA_DIR, "bleaching_events.csv")),
        "cover_trends": pd.read_csv(os.path.join(DATA_DIR, "coral_cover_trends.csv")),
        "risk": pd.read_csv(os.path.join(DATA_DIR, "risk_scores.csv")),
        "projections": pd.read_csv(os.path.join(DATA_DIR, "climate_projections.csv")),
        "currents": pd.read_csv(os.path.join(DATA_DIR, "ocean_currents.csv")),
        "connectivity": pd.read_csv(os.path.join(DATA_DIR, "reef_connectivity.csv")),
        "sst_grid": pd.read_csv(os.path.join(DATA_DIR, "sst_heatmap.csv")),
    }
    # Load real NOAA data if available
    noaa_path = os.path.join(DATA_DIR, "noaa_real_sst.csv")
    if os.path.exists(noaa_path):
        d["noaa_real"] = pd.read_csv(noaa_path)
    return d

data = load_data()

C = {"bg": "#ffffff", "card": "#f5f8fb", "grid": "rgba(0,0,0,0.06)", "teal": "#0a8f6e",
     "coral": "#d94452", "amber": "#d48b00", "blue": "#2b7ab8", "purple": "#7c4dbd",
     "pink": "#c44a8a", "text": "#1a2a3a", "muted": "#5a7080"}
RC = {"Great Barrier Reef": "#0a8f6e", "Coral Triangle": "#2b7ab8", "Caribbean": "#d94452",
      "Indian Ocean": "#7c4dbd", "Red Sea": "#d48b00", "Central Pacific": "#c44a8a", "Eastern Pacific": "#1a9bb5"}
HC = {"Good": "#0a8f6e", "Fair": "#2b7ab8", "Moderate": "#d48b00", "Threatened": "#d94452", "Critical": "#b5182e"}
RKC = {"Low": "#0a8f6e", "Moderate": "#2b7ab8", "Elevated": "#d48b00", "High": "#d94452", "Critical": "#b5182e"}

PL = dict(paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)",
    font=dict(family="EB Garamond, Garamond, Georgia, serif", color="#1a2a3a", size=14),
    margin=dict(l=40, r=20, t=40, b=40), xaxis=dict(gridcolor=C["grid"], zerolinecolor=C["grid"]),
    yaxis=dict(gridcolor=C["grid"], zerolinecolor=C["grid"]), legend=dict(bgcolor="rgba(0,0,0,0)", font=dict(size=13)),
    hoverlabel=dict(bgcolor="#ffffff", font_size=13, font_family="EB Garamond, serif", bordercolor="#dce6f0"))

def AL(fig, **kw):
    fig.update_layout(**{**PL, **kw}); return fig

# SIDEBAR
with st.sidebar:
    st.markdown("## REEF PULSE")
    st.markdown("*Global Coral Reef Intelligence*")
    st.markdown("---")
    page = st.radio("Navigate", ["Overview", "Bleaching & Heat Stress", "Risk Scoring Engine",
        "Climate Projections", "Satellite Thermal View", "Reef Connectivity",
        "Real NOAA Data", "Biodiversity", "Economic Impact"], label_visibility="collapsed")
    st.markdown("---")
    st.markdown("<div style='font-size:0.85rem;color:#6a8299;line-height:1.7;'>Data: NOAA CRW, GCRMN, Allen Coral Atlas, WRI<br><br>Built by <strong style='color:#0a8f6e;'>Rishab Parikh</strong></div>", unsafe_allow_html=True)


# ═══════════════════════════════════════
# OVERVIEW
# ═══════════════════════════════════════
if page == "Overview":
    st.markdown("# Global Reef Overview")
    st.markdown("*Tracking the health of Earth's coral reef ecosystems*")
    sd = data["sites"]; ed = data["economic"]
    c1,c2,c3,c4 = st.columns(4)
    with c1: st.metric("Reef Sites Monitored", f"{len(sd)}")
    with c2:
        a=sd["coral_cover_2024"].mean(); a15=sd["coral_cover_2015"].mean()
        st.metric("Avg Coral Cover", f"{a:.1f}%", delta=f"{a-a15:.1f}% since 2015")
    with c3:
        cr=len(sd[sd["health_status"].isin(["Critical","Threatened"])])
        st.metric("At Risk Sites", f"{cr}/{len(sd)}", delta=f"{cr/len(sd)*100:.0f}% of total", delta_color="inverse")
    with c4: st.metric("Economic Value", f"${ed['total_value_m_usd'].sum()/1000:.0f}B", delta="Annual ecosystem services")
    st.markdown("---")
    st.markdown("### Global Reef Map"); st.markdown("*Size = reef area  |  Color = health status*")
    fig=px.scatter_geo(sd,lat="lat",lon="lon",size="area_km2",color="health_status",color_discrete_map=HC,hover_name="name",
        hover_data={"country":True,"coral_cover_2024":":.1f","cover_change_pct":":.1f","area_km2":":,","health_status":True,"lat":False,"lon":False},
        size_max=30,category_orders={"health_status":["Good","Fair","Moderate","Threatened","Critical"]})
    fig.update_geos(bgcolor="#f5f8fb",landcolor="#e8eff5",oceancolor="#f5f8fb",showocean=True,showland=True,showcoastlines=True,coastlinecolor="#b0c0d0",showframe=False,projection_type="natural earth",lataxis_range=[-35,35],lonaxis_range=[-180,180])
    AL(fig,height=480,margin=dict(l=0,r=0,t=10,b=0)); fig.update_layout(legend=dict(orientation="h",yanchor="bottom",y=-0.05,xanchor="center",x=0.5))
    st.plotly_chart(fig,use_container_width=True)
    st.markdown("---")
    cL,cR=st.columns([3,2])
    with cL:
        st.markdown("### Coral Cover Change by Region (2015 to 2024)")
        cb=sd.groupby("region").agg(c15=("coral_cover_2015","mean"),c24=("coral_cover_2024","mean")).reset_index(); cb["ch"]=cb["c24"]-cb["c15"]; cb=cb.sort_values("ch")
        fig=go.Figure(go.Bar(y=cb["region"],x=cb["ch"],orientation="h",marker_color=[RC.get(r,C["teal"]) for r in cb["region"]],text=[f"{x:+.1f}%" for x in cb["ch"]],textposition="outside",textfont=dict(size=13,color="#1a2a3a")))
        AL(fig,height=350,xaxis_title="Change in Coral Cover (%)",yaxis=dict(gridcolor="rgba(0,0,0,0)")); fig.add_vline(x=0,line_color="rgba(0,0,0,0.1)"); st.plotly_chart(fig,use_container_width=True)
    with cR:
        st.markdown("### Health Status Distribution")
        hc=sd["health_status"].value_counts().reindex(["Good","Fair","Moderate","Threatened","Critical"]).fillna(0)
        fig=go.Figure(go.Pie(labels=hc.index,values=hc.values,marker=dict(colors=[HC[h] for h in hc.index]),hole=0.55,textinfo="percent+label",textfont=dict(size=13,color="#1a2a3a")))
        AL(fig,height=350,margin=dict(l=10,r=10,t=10,b=10),showlegend=False); st.plotly_chart(fig,use_container_width=True)
    st.markdown("---"); st.markdown("### Long-term Coral Cover Decline (1980-2025)")
    fig=px.line(data["cover_trends"],x="year",y="coral_cover_pct",color="region",color_discrete_map=RC); fig.update_traces(line=dict(width=2.5))
    AL(fig,height=400,xaxis_title="",yaxis_title="Coral Cover (%)",legend=dict(orientation="h",yanchor="bottom",y=-0.25,xanchor="center",x=0.5))
    for yr,lb in [(1998,"1st Global\nBleaching"),(2016,"3rd Global\nBleaching"),(2024,"4th Global\nBleaching")]:
        fig.add_vline(x=yr,line_dash="dash",line_color="rgba(217,68,82,0.4)"); fig.add_annotation(x=yr,y=62,text=lb,showarrow=False,font=dict(size=10,color=C["coral"]))
    st.plotly_chart(fig,use_container_width=True)


# ═══════════════════════════════════════
# BLEACHING & HEAT STRESS
# ═══════════════════════════════════════
elif page == "Bleaching & Heat Stress":
    st.markdown("# Bleaching & Heat Stress")
    st.markdown("*Sea surface temperature anomalies and coral bleaching severity*")
    bdf=data["bleaching"].copy(); bdf["date"]=pd.to_datetime(bdf["date"])
    sel=st.multiselect("Select regions",list(RC.keys()),default=["Great Barrier Reef","Caribbean","Indian Ocean"])
    if not sel: st.warning("Select at least one region."); st.stop()
    filt=bdf[bdf["region"].isin(sel)]
    st.markdown("### Sea Surface Temperature Anomaly"); st.markdown("*Positive values = warmer than normal*")
    fig=go.Figure()
    for r in sel:
        rdf=filt[filt["region"]==r].copy().set_index("date"); rq=rdf.select_dtypes(include="number").resample("QS").mean().reset_index()
        fig.add_trace(go.Scatter(x=rq["date"],y=rq["sst_anomaly"],name=r,mode="lines",line=dict(color=RC.get(r),width=2.5)))
    fig.add_hline(y=0,line_color="rgba(0,0,0,0.1)",line_dash="dot")
    fig.add_hline(y=1.0,line_color=C["coral"],line_dash="dash",annotation_text="Bleaching Threshold (+1C)",annotation_position="top right",annotation_font_color=C["coral"],annotation_font_size=11)
    AL(fig,height=400,yaxis_title="SST Anomaly (C)",legend=dict(orientation="h",yanchor="bottom",y=-0.2,xanchor="center",x=0.5)); st.plotly_chart(fig,use_container_width=True)
    st.markdown("---"); c1,c2=st.columns(2)
    with c1:
        st.markdown("### Degree Heating Weeks"); st.markdown("*Above 4 = bleaching, above 8 = mortality*")
        fig=go.Figure()
        for r in sel:
            rdf=filt[filt["region"]==r].copy().set_index("date"); am=rdf["dhw"].resample("YS").max().reset_index()
            fig.add_trace(go.Bar(x=am["date"],y=am["dhw"],name=r,marker_color=RC.get(r),opacity=0.85))
        fig.add_hline(y=4,line_dash="dash",line_color=C["amber"],annotation_text="Bleaching",annotation_font_color=C["amber"],annotation_font_size=10,annotation_position="top right")
        fig.add_hline(y=8,line_dash="dash",line_color=C["coral"],annotation_text="Mortality",annotation_font_color=C["coral"],annotation_font_size=10,annotation_position="top right")
        AL(fig,height=380,yaxis_title="Max DHW (C-weeks)",barmode="group",legend=dict(orientation="h",yanchor="bottom",y=-0.3,xanchor="center",x=0.5)); st.plotly_chart(fig,use_container_width=True)
    with c2:
        st.markdown("### Bleaching Severity Over Time"); st.markdown("*Estimated % of reef area affected*")
        fig=go.Figure()
        for r in sel:
            rdf=filt[filt["region"]==r].copy().set_index("date"); ab=rdf["bleaching_pct"].resample("YS").max().reset_index()
            fig.add_trace(go.Scatter(x=ab["date"],y=ab["bleaching_pct"],name=r,mode="lines+markers",line=dict(color=RC.get(r),width=2.5),marker=dict(size=6)))
        AL(fig,height=380,yaxis_title="Peak Bleaching (%)",legend=dict(orientation="h",yanchor="bottom",y=-0.3,xanchor="center",x=0.5)); st.plotly_chart(fig,use_container_width=True)
    st.markdown("---"); st.markdown("### Major Bleaching Events Timeline")
    edf=data["events"]; sc={"Extreme":"#b5182e","Severe":"#d94452","Moderate":"#d48b00"}
    fig=go.Figure(go.Scatter(x=edf["year"],y=edf["pct_reefs_affected"],mode="markers+text",
        marker=dict(size=edf["pct_reefs_affected"]*0.8+10,color=[sc.get(s,C["teal"]) for s in edf["severity"]],line=dict(color="rgba(0,0,0,0.15)",width=1)),
        text=edf["pct_reefs_affected"].astype(str)+"%",textposition="top center",textfont=dict(size=12,color="#1a2a3a"),
        hovertemplate="<b>%{customdata[0]}</b><br>Severity: %{customdata[1]}<br>Reefs: %{y}%<extra></extra>",customdata=edf[["event_name","severity"]].values))
    AL(fig,height=350,yaxis_title="% of Global Reefs Affected",showlegend=False,xaxis=dict(dtick=2)); st.plotly_chart(fig,use_container_width=True)


# ═══════════════════════════════════════
# RISK SCORING ENGINE
# ═══════════════════════════════════════
elif page == "Risk Scoring Engine":
    st.markdown("# Reef Risk Scoring Engine")
    st.markdown("*Composite risk assessment for 42 monitored reef systems*")
    rk=data["risk"]
    c1,c2,c3,c4=st.columns(4)
    with c1: st.metric("Average Risk Score",f"{rk['composite_risk_score'].mean():.0f}/100")
    with c2: st.metric("Critical Risk Sites",f"{len(rk[rk['risk_tier']=='Critical'])}")
    with c3: st.metric("High Risk Sites",f"{len(rk[rk['risk_tier']=='High'])}")
    with c4: st.metric("Low Risk Sites",f"{len(rk[rk['risk_tier']=='Low'])}")
    st.markdown("---")
    st.markdown("""<div style='background:#f5f8fb;border:1px solid #dce6f0;border-radius:10px;padding:18px 22px;margin-bottom:20px;'>
    <strong style='font-size:1.1rem;'>Scoring Methodology</strong><br><span style='color:#5a7080;font-size:0.95rem;line-height:1.7;'>
    Composite score (0-100) from five weighted factors: <strong>Thermal Stress</strong> (25%), <strong>Cover Risk</strong> (25%), <strong>Trajectory</strong> (20%), <strong>Protection Gap</strong> (15%), <strong>Human Pressure</strong> (15%). Higher = greater risk of collapse.</span></div>""", unsafe_allow_html=True)
    st.markdown("### Global Risk Map"); st.markdown("*Size = reef area  |  Color = risk tier*")
    rm=rk.merge(data["sites"][["site_id","area_km2"]],on="site_id")
    fig=px.scatter_geo(rm,lat="lat",lon="lon",size="area_km2",color="risk_tier",color_discrete_map=RKC,hover_name="name",
        hover_data={"composite_risk_score":":.0f","risk_tier":True,"country":True,"coral_cover_2024":":.1f","lat":False,"lon":False},
        size_max=28,category_orders={"risk_tier":["Low","Moderate","Elevated","High","Critical"]})
    fig.update_geos(bgcolor="#f5f8fb",landcolor="#e8eff5",oceancolor="#f5f8fb",showocean=True,showland=True,showcoastlines=True,coastlinecolor="#b0c0d0",showframe=False,projection_type="natural earth",lataxis_range=[-35,35],lonaxis_range=[-180,180])
    AL(fig,height=450,margin=dict(l=0,r=0,t=10,b=0)); fig.update_layout(legend=dict(orientation="h",yanchor="bottom",y=-0.05,xanchor="center",x=0.5)); st.plotly_chart(fig,use_container_width=True)
    st.markdown("---"); st.markdown("### Highest Risk Reef Systems")
    t15=rk.nlargest(15,"composite_risk_score").sort_values("composite_risk_score")
    fig=go.Figure(go.Bar(y=t15["name"]+" ("+t15["country"]+")",x=t15["composite_risk_score"],orientation="h",
        marker=dict(color=[RKC.get(t,C["teal"]) for t in t15["risk_tier"]]),text=[f"{x:.0f}" for x in t15["composite_risk_score"]],textposition="outside",textfont=dict(size=13,color="#1a2a3a")))
    AL(fig,height=500,xaxis_title="Composite Risk Score (0-100)",xaxis=dict(range=[0,105]),yaxis=dict(gridcolor="rgba(0,0,0,0)"),showlegend=False); st.plotly_chart(fig,use_container_width=True)
    st.markdown("---"); st.markdown("### Risk Factor Breakdown"); st.markdown("*Select a reef to see what drives its risk*")
    ss=st.selectbox("Choose a reef",rk.sort_values("composite_risk_score",ascending=False)["name"].tolist()); sr=rk[rk["name"]==ss].iloc[0]
    c1,c2=st.columns([1,2])
    with c1:
        st.markdown(f"**{sr['name']}**, {sr['country']}"); st.markdown(f"Region: {sr['region']}"); st.markdown(f"Coral Cover: {sr['coral_cover_2024']:.1f}%")
        st.markdown(f"Cover Change: {sr['cover_change_pct']:+.1f}%"); st.markdown(f"Protection: {sr['protection_level']}")
        tc=RKC.get(sr["risk_tier"],"#555")
        st.markdown(f"<div style='margin-top:12px;font-size:2.2rem;font-weight:700;color:{tc};'>{sr['composite_risk_score']:.0f}<span style='font-size:1rem;color:#5a7080;'>/100</span></div><div style='font-size:1.1rem;font-weight:600;color:{tc};'>{sr['risk_tier']} Risk</div>",unsafe_allow_html=True)
    with c2:
        fct=["Thermal Stress","Cover Risk","Trajectory","Protection Gap","Human Pressure"]
        scr=[sr["thermal_stress_score"],sr["cover_risk_score"],sr["trajectory_score"],sr["protection_score"],sr["human_pressure_score"]]
        bc=[C["coral"] if s>=60 else C["amber"] if s>=40 else C["teal"] for s in scr]
        fig=go.Figure(go.Bar(y=fct,x=scr,orientation="h",marker_color=bc,text=[f"{s:.0f}" for s in scr],textposition="outside",textfont=dict(size=14,color="#1a2a3a")))
        AL(fig,height=280,xaxis_title="Factor Score (0-100)",xaxis=dict(range=[0,105]),yaxis=dict(gridcolor="rgba(0,0,0,0)",autorange="reversed"),showlegend=False,margin=dict(l=40,r=20,t=10,b=40)); st.plotly_chart(fig,use_container_width=True)


# ═══════════════════════════════════════
# CLIMATE PROJECTIONS
# ═══════════════════════════════════════
elif page == "Climate Projections":
    st.markdown("# Climate Projection Scenarios")
    st.markdown("*Modeled outcomes under three warming pathways through 2055*")
    pj=data["projections"]
    st.markdown("""<div style='background:#f5f8fb;border:1px solid #dce6f0;border-radius:10px;padding:18px 22px;margin-bottom:10px;'>
    <div style='display:flex;gap:30px;flex-wrap:wrap;'>
    <div><strong style='color:#0a8f6e;'>1.5C Paris Target</strong><br><span style='color:#5a7080;font-size:0.9rem;'>Aggressive cuts. Partial reef survival plausible.</span></div>
    <div><strong style='color:#d48b00;'>2.0C Current Pledges</strong><br><span style='color:#5a7080;font-size:0.9rem;'>Annual bleaching by 2040s in most regions.</span></div>
    <div><strong style='color:#d94452;'>3.0C Insufficient Action</strong><br><span style='color:#5a7080;font-size:0.9rem;'>Near-total reef loss by mid-century.</span></div></div></div>""",unsafe_allow_html=True)
    st.markdown("---")
    scn=st.radio("Select warming scenario",["1.5C","2.0C","3.0C"],horizontal=True)
    sdf=pj[pj["scenario"]==scn]; y50=sdf[sdf["year"]==2050]
    c1,c2,c3,c4=st.columns(4)
    with c1: st.metric("Avg Cover 2050",f"{y50['projected_cover_pct'].mean():.1f}%")
    with c2: st.metric("Avg Warming 2050",f"+{y50['warming_c'].mean():.1f}C")
    with c3: st.metric("Bleaching Frequency",f"{y50['bleaching_freq_per_decade'].mean():.1f}/decade")
    with c4: st.metric("Economic Loss",f"{y50['economic_loss_pct'].mean():.0f}%",delta="of current value",delta_color="inverse")
    st.markdown("---"); st.markdown(f"### Projected Coral Cover Under {scn} Warming")
    fig=px.line(sdf,x="year",y="projected_cover_pct",color="region",color_discrete_map=RC); fig.update_traces(line=dict(width=2.5))
    fig.add_hline(y=10,line_dash="dash",line_color=C["coral"],annotation_text="Functional Extinction (~10%)",annotation_position="top right",annotation_font_color=C["coral"],annotation_font_size=10)
    AL(fig,height=420,yaxis_title="Projected Coral Cover (%)",legend=dict(orientation="h",yanchor="bottom",y=-0.25,xanchor="center",x=0.5)); st.plotly_chart(fig,use_container_width=True)
    st.markdown("---"); st.markdown("### Scenario Comparison by Region")
    rsel=st.selectbox("Choose a region",sorted(pj["region"].unique())); rdf=pj[pj["region"]==rsel]
    c1,c2=st.columns(2)
    sl={"1.5C":dict(color=C["teal"],width=2.5),"2.0C":dict(color=C["amber"],width=2.5,dash="dash"),"3.0C":dict(color=C["coral"],width=2.5,dash="dot")}
    with c1:
        st.markdown(f"#### Coral Cover — {rsel}"); fig=go.Figure()
        for s in ["1.5C","2.0C","3.0C"]: sd2=rdf[rdf["scenario"]==s]; fig.add_trace(go.Scatter(x=sd2["year"],y=sd2["projected_cover_pct"],name=s,mode="lines",line=sl[s]))
        fig.add_hline(y=10,line_dash="dash",line_color="rgba(0,0,0,0.15)")
        AL(fig,height=380,yaxis_title="Coral Cover (%)",legend=dict(orientation="h",yanchor="bottom",y=-0.25,xanchor="center",x=0.5)); st.plotly_chart(fig,use_container_width=True)
    with c2:
        st.markdown(f"#### Economic Loss — {rsel}"); fig=go.Figure()
        for s in ["1.5C","2.0C","3.0C"]: sd2=rdf[rdf["scenario"]==s]; fig.add_trace(go.Scatter(x=sd2["year"],y=sd2["economic_loss_pct"],name=s,mode="lines",line=sl[s]))
        AL(fig,height=380,yaxis_title="% Value Lost",legend=dict(orientation="h",yanchor="bottom",y=-0.25,xanchor="center",x=0.5)); st.plotly_chart(fig,use_container_width=True)
    st.markdown("---"); st.markdown("### Bleaching Frequency Heatmap (2050)")
    hd=pj[pj["year"]==2050].pivot_table(index="region",columns="scenario",values="bleaching_freq_per_decade")[["1.5C","2.0C","3.0C"]]
    fig=go.Figure(go.Heatmap(z=hd.values,x=["1.5C","2.0C","3.0C"],y=hd.index.tolist(),
        colorscale=[[0,"#e0f5ef"],[0.3,"#ffeeba"],[0.6,"#ffb3b3"],[1.0,"#b5182e"]],
        text=np.round(hd.values,1),texttemplate="%{text}",textfont=dict(size=14,color="#1a2a3a"),colorbar=dict(title="Events/Decade")))
    AL(fig,height=380,margin=dict(l=40,r=20,t=10,b=40),xaxis=dict(gridcolor="rgba(0,0,0,0)"),yaxis=dict(gridcolor="rgba(0,0,0,0)")); st.plotly_chart(fig,use_container_width=True)
    st.markdown("""<div style='background:#fff8f0;border-left:4px solid #d48b00;border-radius:6px;padding:16px 20px;margin-top:10px;'>
    <strong>Key Insight:</strong> The difference between 1.5C and 2.0C may determine whether reefs persist as functional ecosystems. Every fraction of a degree matters.</div>""",unsafe_allow_html=True)


# ═══════════════════════════════════════
# SATELLITE THERMAL VIEW
# ═══════════════════════════════════════
elif page == "Satellite Thermal View":
    st.markdown("# Satellite Thermal View")
    st.markdown("*Visualizing sea surface temperature anomalies across tropical oceans, 2015-2024*")

    sst = data["sst_grid"]

    st.markdown("""<div style='background:#f5f8fb;border:1px solid #dce6f0;border-radius:10px;padding:18px 22px;margin-bottom:20px;'>
    <strong>About this view:</strong> Each frame shows annual average SST anomalies across the tropical ocean belt. Warmer colors (red/orange) indicate waters significantly above historical averages — the conditions that trigger coral bleaching. Watch how the warm anomalies intensify and spread between 2015 and 2024, particularly during the El Nino events of 2015-16 and 2023-24.</div>""", unsafe_allow_html=True)

    year_sel = st.select_slider("Select Year", options=sorted(sst["year"].unique()), value=2024)
    yr_data = sst[sst["year"] == year_sel]

    fig = go.Figure(go.Scattergeo(
        lat=yr_data["lat"], lon=yr_data["lon"],
        marker=dict(
            size=6, color=yr_data["sst_anomaly"],
            colorscale=[[0, "#2166ac"], [0.3, "#67a9cf"], [0.45, "#f7f7f7"],
                        [0.55, "#fddbc7"], [0.7, "#ef8a62"], [0.85, "#d6604d"], [1.0, "#b2182b"]],
            cmin=-0.5, cmax=1.5, colorbar=dict(title="SST Anomaly (C)", len=0.6),
            line=dict(width=0),
        ),
        hovertemplate="Lat: %{lat:.1f}<br>Lon: %{lon:.1f}<br>Anomaly: %{marker.color:.2f}C<extra></extra>",
    ))
    fig.update_geos(bgcolor="#f5f8fb", landcolor="#d4dce5", oceancolor="#f5f8fb",
        showocean=True, showland=True, showcoastlines=True, coastlinecolor="#a0b0c0",
        showframe=False, projection_type="natural earth", lataxis_range=[-35, 35], lonaxis_range=[-180, 180])
    AL(fig, height=500, margin=dict(l=0, r=0, t=10, b=0), title=f"Sea Surface Temperature Anomaly — {year_sel}")
    st.plotly_chart(fig, use_container_width=True)

    st.markdown("---")

    # Year-over-year comparison
    st.markdown("### Global Mean SST Anomaly Trend")
    yearly_mean = sst.groupby("year")["sst_anomaly"].mean().reset_index()
    fig = go.Figure(go.Bar(x=yearly_mean["year"], y=yearly_mean["sst_anomaly"],
        marker_color=[C["coral"] if v > 0.4 else C["amber"] if v > 0.2 else C["teal"] for v in yearly_mean["sst_anomaly"]],
        text=[f"{v:.2f}C" for v in yearly_mean["sst_anomaly"]], textposition="outside", textfont=dict(size=12)))
    AL(fig, height=350, yaxis_title="Mean SST Anomaly (C)", xaxis=dict(dtick=1))
    st.plotly_chart(fig, use_container_width=True)

    st.markdown("""<div style='background:#fff0f0;border-left:4px solid #d94452;border-radius:6px;padding:16px 20px;margin-top:10px;'>
    <strong>2023-2024:</strong> The sharpest jump in tropical ocean temperatures in the satellite record. The anomaly in 2024 exceeded the previous El Nino peak of 2016, marking the fourth global mass bleaching event — the most severe ever documented.</div>""", unsafe_allow_html=True)


# ═══════════════════════════════════════
# REEF CONNECTIVITY
# ═══════════════════════════════════════
elif page == "Reef Connectivity":
    st.markdown("# Reef Connectivity & Larval Dispersal")
    st.markdown("*How ocean currents connect reef ecosystems and enable recovery*")

    conn = data["connectivity"]
    curr = data["currents"]
    sites = data["sites"]

    st.markdown("""<div style='background:#f5f8fb;border:1px solid #dce6f0;border-radius:10px;padding:18px 22px;margin-bottom:20px;'>
    <strong>Why connectivity matters:</strong> Coral reefs reproduce by releasing larvae into ocean currents. These larvae can drift for days to weeks before settling on a new reef. Healthy, well-connected reefs act as "source" populations that reseed damaged reefs downstream.
    Understanding these connections is critical for conservation planning — protecting a single well-connected source reef can benefit an entire network of downstream systems.</div>""", unsafe_allow_html=True)

    # Region selector
    reg_sel = st.selectbox("Select a region to explore", sorted(conn["region"].unique()))
    rc = conn[conn["region"] == reg_sel]
    rc_curr = curr[curr["region"] == reg_sel]
    rc_sites = sites[sites["region"] == reg_sel]

    # Connectivity map
    st.markdown(f"### Larval Connectivity — {reg_sel}")
    st.markdown("*Lines show larval dispersal pathways. Thicker lines = stronger connectivity. Dashed blue lines = major ocean currents.*")

    fig = go.Figure()

    # Draw ocean currents
    for cname in rc_curr["current_name"].unique():
        cd = rc_curr[rc_curr["current_name"] == cname].sort_values("point_order")
        fig.add_trace(go.Scattergeo(
            lat=cd["lat"], lon=cd["lon"], mode="lines",
            line=dict(color="#5cb8ff", width=3, dash="dash"),
            name=cname, hovertemplate=f"<b>{cname}</b><br>Speed: {cd['speed_km_day'].iloc[0]} km/day<extra></extra>",
            showlegend=True,
        ))

    # Draw connectivity links
    for _, link in rc.iterrows():
        opacity = min(0.8, link["connectivity_strength"] * 1.5)
        width = max(0.5, link["connectivity_strength"] * 4)
        color = C["teal"] if link["effective_larval_supply"] > 0.15 else C["amber"] if link["effective_larval_supply"] > 0.05 else C["muted"]
        fig.add_trace(go.Scattergeo(
            lat=[link["source_lat"], link["target_lat"]], lon=[link["source_lon"], link["target_lon"]],
            mode="lines", line=dict(color=color, width=width),
            opacity=opacity, showlegend=False,
            hovertemplate=f"<b>{link['source_name']} → {link['target_name']}</b><br>Distance: {link['distance_km']:.0f} km<br>Strength: {link['connectivity_strength']:.2f}<br>Larval transit: {link['larval_duration_days']} days<br>Survival: {link['larval_survival_pct']:.1f}%<extra></extra>",
        ))

    # Draw reef sites
    fig.add_trace(go.Scattergeo(
        lat=rc_sites["lat"], lon=rc_sites["lon"], mode="markers+text",
        marker=dict(size=12, color=[HC.get(h, C["teal"]) for h in rc_sites["health_status"]],
                    line=dict(color="white", width=1.5)),
        text=rc_sites["name"], textposition="top center", textfont=dict(size=11, color="#1a2a3a"),
        showlegend=False,
        hovertemplate="<b>%{text}</b><br>Cover: %{customdata[0]:.1f}%<br>Status: %{customdata[1]}<extra></extra>",
        customdata=rc_sites[["coral_cover_2024", "health_status"]].values,
    ))

    fig.update_geos(bgcolor="#f5f8fb", landcolor="#e8eff5", oceancolor="#f0f5fa",
        showocean=True, showland=True, showcoastlines=True, coastlinecolor="#b0c0d0",
        showframe=False, projection_type="natural earth", fitbounds="locations")
    AL(fig, height=550, margin=dict(l=0, r=0, t=10, b=0),
       legend=dict(orientation="h", yanchor="bottom", y=-0.05, xanchor="center", x=0.5))
    st.plotly_chart(fig, use_container_width=True)

    st.markdown("---")

    # Connectivity table
    st.markdown("### Connectivity Details")
    c1, c2 = st.columns(2)
    with c1:
        st.markdown("#### Strongest Source Reefs")
        st.markdown("*Reefs that supply the most larvae to downstream systems*")
        source_strength = rc.groupby("source_name")["effective_larval_supply"].sum().sort_values(ascending=False).reset_index()
        source_strength.columns = ["Reef", "Total Larval Supply Index"]
        st.dataframe(source_strength.head(10), use_container_width=True, hide_index=True)
    with c2:
        st.markdown("#### Most Connected Pairs")
        st.markdown("*Reef pairs with the strongest larval exchange*")
        top_pairs = rc.nlargest(10, "connectivity_strength")[["source_name", "target_name", "distance_km", "connectivity_strength", "larval_survival_pct"]]
        top_pairs.columns = ["Source", "Target", "Distance (km)", "Strength", "Survival %"]
        st.dataframe(top_pairs, use_container_width=True, hide_index=True)

    st.markdown("""<div style='background:#e8f5ef;border-left:4px solid #0a8f6e;border-radius:6px;padding:16px 20px;margin-top:20px;'>
    <strong>Conservation implication:</strong> Reefs with high source strength are disproportionately valuable for network-level recovery. Protecting these source reefs — even if they appear individually healthy — is essential because their loss would cut off larval supply to downstream systems that depend on resupply for post-bleaching recovery.</div>""", unsafe_allow_html=True)


# ═══════════════════════════════════════
# REAL NOAA DATA
# ═══════════════════════════════════════
elif page == "Real NOAA Data":
    st.markdown("# Real NOAA Satellite Data")
    st.markdown("*Live sea surface temperature data from NOAA Coral Reef Watch via ERDDAP*")

    if "noaa_real" in data:
        noaa = data["noaa_real"].copy()
        noaa["date"] = pd.to_datetime(noaa["date"])
        st.markdown(f"""<div style='background:#e8f5ef;border:1px solid #b8e0d0;border-radius:10px;padding:18px 22px;margin-bottom:20px;'>
        <strong style='color:#0a8f6e;'>Real data loaded.</strong> {len(noaa):,} records from NOAA Coral Reef Watch ERDDAP spanning {noaa['date'].min().strftime('%B %Y')} to {noaa['date'].max().strftime('%B %Y')}.</div>""", unsafe_allow_html=True)

        regions = noaa["region"].unique()
        sel = st.multiselect("Select regions", sorted(regions), default=sorted(regions)[:3])
        if sel:
            filt = noaa[noaa["region"].isin(sel)]
            st.markdown("### Monthly Sea Surface Temperature")
            fig = go.Figure()
            for r in sel:
                rd = filt[filt["region"] == r]
                fig.add_trace(go.Scatter(x=rd["date"], y=rd["sst_celsius"], name=r, mode="lines",
                    line=dict(color=RC.get(r, C["teal"]), width=2)))
            AL(fig, height=400, yaxis_title="SST (C)", legend=dict(orientation="h", yanchor="bottom", y=-0.2, xanchor="center", x=0.5))
            st.plotly_chart(fig, use_container_width=True)

            st.markdown("### Monthly SST Anomaly")
            fig = go.Figure()
            for r in sel:
                rd = filt[filt["region"] == r]
                fig.add_trace(go.Scatter(x=rd["date"], y=rd["sst_anomaly"], name=r, mode="lines",
                    line=dict(color=RC.get(r, C["teal"]), width=2)))
            fig.add_hline(y=0, line_color="rgba(0,0,0,0.1)", line_dash="dot")
            AL(fig, height=400, yaxis_title="Anomaly (C)", legend=dict(orientation="h", yanchor="bottom", y=-0.2, xanchor="center", x=0.5))
            st.plotly_chart(fig, use_container_width=True)
    else:
        st.markdown("""<div style='background:#fff8f0;border:1px solid #f0dcc0;border-radius:10px;padding:22px 26px;'>
        <strong style='font-size:1.2rem;'>No real NOAA data found yet.</strong><br><br>
        <span style='color:#5a7080;font-size:1rem;line-height:1.8;'>
        To download real satellite data from NOAA Coral Reef Watch, run this in your terminal:<br><br>
        <code style='background:#f0f4f8;padding:8px 14px;border-radius:6px;font-family:monospace;'>python fetch_noaa.py</code><br><br>
        This will pull monthly sea surface temperature and anomaly data for all seven reef regions from NOAA's ERDDAP server (2015-2025). The download takes about 5-10 minutes.<br><br>
        Once complete, refresh this page to see the real data.</span></div>""", unsafe_allow_html=True)

        st.markdown("---")
        st.markdown("### What the fetcher downloads")
        st.markdown("""
        The `fetch_noaa.py` script pulls data from NOAA's CoastWatch ERDDAP server for these regions:

        - **Great Barrier Reef** — Australia's northeastern coast
        - **Coral Triangle** — Indonesia, Philippines, PNG, Malaysia
        - **Caribbean** — Belize to Bonaire
        - **Indian Ocean** — Maldives, Seychelles, East Africa
        - **Red Sea** — Egypt to Djibouti
        - **Central Pacific** — Fiji, Palau, French Polynesia
        - **Eastern Pacific** — Galapagos, Costa Rica, Panama

        Variables: Monthly mean SST and SST Anomaly at 5km resolution, spatially averaged per region.
        """)


# ═══════════════════════════════════════
# BIODIVERSITY
# ═══════════════════════════════════════
elif page == "Biodiversity":
    st.markdown("# Marine Biodiversity")
    st.markdown("*Species richness and ecological diversity across reef regions*")
    sp=data["species"]
    c1,c2,c3,c4=st.columns(4)
    with c1: st.metric("Hard Coral Species",f"{sp['hard_coral_species'].sum():,}")
    with c2: st.metric("Reef Fish Species",f"{sp['reef_fish_species'].sum():,}")
    with c3: st.metric("Threatened Species",f"{sp['threatened_species'].sum():,}",delta="Across all regions",delta_color="inverse")
    with c4: st.metric("Total Marine Species",f"{sp['total_species'].sum():,}")
    st.markdown("---"); st.markdown("### Species Composition by Region")
    cats=[("hard_coral_species","Hard Corals",C["teal"]),("soft_coral_species","Soft Corals",C["blue"]),("reef_fish_species","Reef Fish",C["purple"]),("invertebrate_species","Invertebrates",C["pink"])]
    fig=go.Figure()
    for col,lb,clr in cats: fig.add_trace(go.Bar(x=sp["region"],y=sp[col],name=lb,marker_color=clr,opacity=0.9))
    AL(fig,height=450,barmode="stack",yaxis_title="Number of Species",legend=dict(orientation="h",yanchor="bottom",y=-0.25,xanchor="center",x=0.5)); st.plotly_chart(fig,use_container_width=True)
    st.markdown("---"); cL,cR=st.columns(2)
    with cL:
        st.markdown("### Endemism Rate"); ss=sp.sort_values("endemic_pct",ascending=True)
        fig=go.Figure(go.Bar(y=ss["region"],x=ss["endemic_pct"],orientation="h",marker=dict(color=ss["endemic_pct"],colorscale=[[0,C["blue"]],[0.5,C["teal"]],[1,C["coral"]]]),text=[f"{x:.1f}%" for x in ss["endemic_pct"]],textposition="outside",textfont=dict(color="#1a2a3a",size=13)))
        AL(fig,height=350,xaxis_title="Endemic Species (%)",yaxis=dict(gridcolor="rgba(0,0,0,0)"),showlegend=False); st.plotly_chart(fig,use_container_width=True)
    with cR:
        st.markdown("### Threatened Species"); st2=sp.sort_values("threatened_species",ascending=True)
        fig=go.Figure(go.Bar(y=st2["region"],x=st2["threatened_species"],orientation="h",marker_color=C["coral"],text=st2["threatened_species"],textposition="outside",textfont=dict(color="#1a2a3a",size=13)))
        AL(fig,height=350,xaxis_title="Threatened Species",yaxis=dict(gridcolor="rgba(0,0,0,0)"),showlegend=False); st.plotly_chart(fig,use_container_width=True)
    st.markdown("---"); st.markdown("### Biodiversity Profile Comparison")
    comp=st.multiselect("Select regions",sp["region"].tolist(),default=["Coral Triangle","Caribbean","Red Sea"],key="bio")
    if comp:
        rc2=["Hard Corals","Soft Corals","Reef Fish","Invertebrates","Endemic %"]; fig=go.Figure()
        for region in comp:
            row=sp[sp["region"]==region].iloc[0]
            vals=[row["hard_coral_species"]/sp["hard_coral_species"].max()*100,row["soft_coral_species"]/sp["soft_coral_species"].max()*100,
                  row["reef_fish_species"]/sp["reef_fish_species"].max()*100,row["invertebrate_species"]/sp["invertebrate_species"].max()*100,
                  row["endemic_pct"]/sp["endemic_pct"].max()*100]; vals.append(vals[0])
            rc_c=RC.get(region,"#0a8f6e")
            fig.add_trace(go.Scatterpolar(r=vals,theta=rc2+[rc2[0]],name=region,line=dict(color=rc_c,width=2.5),fill="toself",
                fillcolor=f"rgba({int(rc_c[1:3],16)},{int(rc_c[3:5],16)},{int(rc_c[5:7],16)},0.1)"))
        fig.update_layout(polar=dict(bgcolor="rgba(0,0,0,0)",radialaxis=dict(visible=True,range=[0,100],gridcolor=C["grid"],tickfont=dict(size=10,color="#3a4a5a")),
            angularaxis=dict(gridcolor=C["grid"],tickfont=dict(size=13,color="#1a2a3a"))))
        AL(fig,height=450,legend=dict(orientation="h",yanchor="bottom",y=-0.15,xanchor="center",x=0.5)); st.plotly_chart(fig,use_container_width=True)


# ═══════════════════════════════════════
# ECONOMIC IMPACT
# ═══════════════════════════════════════
elif page == "Economic Impact":
    st.markdown("# Economic Impact")
    st.markdown("*The financial value of reef ecosystems*")
    ec=data["economic"]
    c1,c2,c3,c4=st.columns(4)
    with c1: st.metric("Ecosystem Value",f"${ec['total_value_m_usd'].sum()/1000:.1f}B/yr")
    with c2: st.metric("Tourism",f"${ec['tourism_revenue_m_usd'].sum()/1000:.1f}B/yr")
    with c3: st.metric("Fisheries",f"${ec['fisheries_revenue_m_usd'].sum()/1000:.1f}B/yr")
    with c4: st.metric("People Dependent",f"{ec['people_dependent_millions'].sum():.0f}M")
    st.markdown("---"); st.markdown("### Economic Value by Country")
    tc=ec.nlargest(15,"total_value_m_usd").sort_values("total_value_m_usd"); fig=go.Figure()
    for col,lb,clr in [("tourism_revenue_m_usd","Tourism",C["teal"]),("fisheries_revenue_m_usd","Fisheries",C["blue"]),("coastal_protection_m_usd","Coastal Protection",C["purple"])]:
        fig.add_trace(go.Bar(y=tc["country"],x=tc[col],name=lb,orientation="h",marker_color=clr,opacity=0.9))
    AL(fig,height=500,barmode="stack",xaxis_title="Value (Millions USD)",yaxis=dict(gridcolor="rgba(0,0,0,0)"),legend=dict(orientation="h",yanchor="bottom",y=-0.15,xanchor="center",x=0.5)); st.plotly_chart(fig,use_container_width=True)
    st.markdown("---"); cL,cR=st.columns(2)
    with cL:
        st.markdown("### Reef Dependency (% of GDP)"); gdf=ec.nlargest(10,"gdp_reef_pct").sort_values("gdp_reef_pct")
        fig=go.Figure(go.Bar(y=gdf["country"],x=gdf["gdp_reef_pct"],orientation="h",marker=dict(color=gdf["gdp_reef_pct"],colorscale=[[0,C["teal"]],[0.5,C["amber"]],[1,C["coral"]]]),text=[f"{x:.1f}%" for x in gdf["gdp_reef_pct"]],textposition="outside",textfont=dict(color="#1a2a3a",size=13)))
        AL(fig,height=400,xaxis_title="% of GDP",yaxis=dict(gridcolor="rgba(0,0,0,0)"),showlegend=False); st.plotly_chart(fig,use_container_width=True)
    with cR:
        st.markdown("### People Dependent"); pdf=ec.nlargest(10,"people_dependent_millions").sort_values("people_dependent_millions")
        fig=go.Figure(go.Bar(y=pdf["country"],x=pdf["people_dependent_millions"],orientation="h",marker_color=C["purple"],text=[f"{x:.1f}M" for x in pdf["people_dependent_millions"]],textposition="outside",textfont=dict(color="#1a2a3a",size=13)))
        AL(fig,height=400,xaxis_title="People (Millions)",yaxis=dict(gridcolor="rgba(0,0,0,0)"),showlegend=False); st.plotly_chart(fig,use_container_width=True)
    st.markdown("---"); st.markdown("### Ecosystem Value by Region")
    fig=px.treemap(ec,path=["region","country"],values="total_value_m_usd",color="region",color_discrete_map=RC,hover_data={"total_value_m_usd":":,.0f"})
    fig.update_traces(textinfo="label+value",texttemplate="%{label}<br>$%{value:,.0f}M",textfont=dict(size=13))
    AL(fig,height=450,margin=dict(l=5,r=5,t=5,b=5)); st.plotly_chart(fig,use_container_width=True)

# Hot-fix: force dark text on all Streamlit elements
st.markdown("""
<style>
    .stApp, .stApp * { color: #1a2a3a !important; }
    div[data-testid="stMetricValue"] { color: #0a8f6e !important; }
    div[data-testid="stMetricDelta"] { color: inherit !important; }
    .stRadio label, .stMultiSelect label, .stSelectbox label { color: #1a2a3a !important; }
    .stRadio div[role="radiogroup"] label span { color: #1a2a3a !important; }
    section[data-testid="stSidebar"] * { color: #1a2a3a !important; }
    div[data-baseweb="select"] span { color: #1a2a3a !important; }
    div[data-baseweb="tag"] span { color: #ffffff !important; }
</style>
""", unsafe_allow_html=True)
