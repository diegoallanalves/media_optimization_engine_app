"""Streamlit portfolio dashboard for the two-tier Media Optimization Engine."""
import numpy as np
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import streamlit as st
from sklearn.cluster import KMeans
from sklearn.preprocessing import StandardScaler

from database import test_connection, load_channel_constraints, load_run_history
from optimization_service import run_full_optimization

st.set_page_config(page_title="Media Optimization Engine", page_icon="🌊", layout="wide")

# Surf-inspired palette: ocean / reef / sand / sunset. Deliberately restrained.
OCEAN = "#0B3954"; DEEP = "#082F49"; REEF = "#087E8B"; FOAM = "#BFD7D5"
SAND = "#F5F1E8"; CORAL = "#FF7F50"; INK = "#18323F"; WHITE = "#FFFFFF"
CHANNEL_COLORS = {"Social": REEF, "Display": "#4D9DE0", "Video": CORAL}

st.markdown(f"""
<style>
/* =========================
   Original surf portfolio look
   with dark-mode/readability fixes
   ========================= */

/* Collapse Streamlit's native top chrome so it does not create the
   empty white strip above the portfolio header.  The app keeps its own
   navigation and controls in the sidebar. */
[data-testid="stHeader"] {{
    height: 0 !important;
    min-height: 0 !important;
    background: transparent !important;
    visibility: hidden !important;
}}
[data-testid="stToolbar"],
[data-testid="stDecoration"],
[data-testid="stStatusWidget"] {{
    display: none !important;
}}

.stApp {{
    background: linear-gradient(180deg, #F8FBFA 0%, {SAND} 100%);
    color: {INK};
}}

.block-container {{
    padding-top: 0.9rem !important;
    max-width: 1500px;
}}

h1, h2, h3 {{
    color: {OCEAN};
    letter-spacing: -0.02em;
}}

[data-testid="stMetric"] {{
    background: rgba(255,255,255,.82);
    border: 1px solid #D9E7E5;
    border-radius: 14px;
    padding: 14px 16px;
    box-shadow: 0 4px 16px rgba(11,57,84,.05);
}}
[data-testid="stMetricLabel"] {{ color:#55727D; }}
[data-testid="stMetricValue"] {{ color:{OCEAN}; }}

.stButton > button {{
    border-radius: 10px;
    border: 0;
    background: {OCEAN};
    color: white;
    font-weight: 650;
}}
.stButton > button:hover {{
    background: {REEF};
    color: white;
}}

.surf-card {{
    background: rgba(255,255,255,.78);
    border: 1px solid #D9E7E5;
    border-radius: 16px;
    padding: 18px 20px;
    margin-bottom: 12px;
    box-shadow: 0 4px 18px rgba(11,57,84,.04);
}}
.small-note {{ color:#607D86; font-size:.92rem; }}
hr {{ border:none; border-top:1px solid #D9E7E5; }}

/* Header: no surrounding white box */
.surf-header {{
    background: transparent !important;
    border: 0 !important;
    box-shadow: none !important;
    padding: 2px 0 8px 0;
    margin: 0;
}}
.surf-header-row {{
    display:flex;
    align-items:flex-start;
    justify-content:space-between;
    gap:24px;
}}
.surf-header-title {{
    margin:0;
    color:{OCEAN};
    font-size:2.25rem;
    font-weight:800;
    letter-spacing:-0.035em;
}}
.surf-header-sub {{
    margin-top:5px;
    color:#375B69;
    font-weight:650;
}}
.surf-header-path {{
    margin-top:9px;
    color:#70858E;
    font-size:.88rem;
}}
.sql-pill {{
    margin-top:8px;
    padding:8px 14px;
    white-space:nowrap;
    border-radius:999px;
    background:#DFF7EC;
    color:#087A53;
    border:1px solid #BCEBD8;
    font-size:.86rem;
}}

/* Tabs */
.stTabs [data-baseweb="tab-list"] {{
    gap: 18px;
}}
.stTabs [data-baseweb="tab"] {{
    background: transparent !important;
}}

/* Native Streamlit popovers / Deploy menu:
   make text readable instead of dark-on-black */
div[data-baseweb="popover"] {{
    color: #E8F7F5 !important;
}}
div[data-baseweb="popover"] * {{
    color: inherit !important;
}}

/* System dark mode.
   Keep the same surf identity, only deepen surfaces and fix text contrast. */
@media (prefers-color-scheme: dark) {{
    .stApp {{
        background: linear-gradient(180deg, #071C28 0%, #0A2731 58%, #102E35 100%) !important;
        color: #EAF8F6 !important;
    }}

    [data-testid="stAppViewContainer"] {{
        background: linear-gradient(180deg, #071C28 0%, #0A2731 58%, #102E35 100%) !important;
    }}

    [data-testid="stHeader"] {{
        background: #071C28 !important;
    }}

    [data-testid="stSidebar"] {{
        background: #071923 !important;
        border-right: 1px solid #21444E !important;
    }}
    [data-testid="stSidebar"] *,
    [data-testid="stSidebar"] p,
    [data-testid="stSidebar"] label,
    [data-testid="stSidebar"] span {{
        color: #E5F3F2 !important;
    }}

    h1,h2,h3,h4,h5,h6,p,label,li,strong,em,small,
    [data-testid="stMarkdownContainer"],
    [data-testid="stMarkdownContainer"] *,
    [data-testid="stCaptionContainer"],
    [data-testid="stCaptionContainer"] * {{
        color:#EAF8F6 !important;
    }}

    [data-testid="stMetric"] {{
        background:#10313C !important;
        border-color:#2A535D !important;
        box-shadow:none !important;
    }}
    [data-testid="stMetric"] * {{
        color:#F0FBF9 !important;
    }}

    .surf-card {{
        background:#0F303A !important;
        border-color:#28515B !important;
        box-shadow:none !important;
    }}
    .small-note {{ color:#A7C1C3 !important; }}

    .surf-header-title {{ color:#F1FBFA !important; }}
    .surf-header-sub {{ color:#C3DDDE !important; }}
    .surf-header-path {{ color:#9DBBC0 !important; }}
    .sql-pill {{
        background:#103C38 !important;
        color:#72E5C6 !important;
        border-color:#28655C !important;
    }}

    .stButton > button {{
        background:#0E7490 !important;
        color:#FFFFFF !important;
        border:1px solid #3191A6 !important;
    }}
    .stButton > button * {{
        color:#FFFFFF !important;
    }}

    [data-testid="stToggle"] *,
    [data-testid="stCheckbox"] * {{
        color:#EAF8F6 !important;
    }}

    .stTabs [data-baseweb="tab"],
    .stTabs [data-baseweb="tab"] * {{
        color:#B4CDCF !important;
    }}
    .stTabs [aria-selected="true"],
    .stTabs [aria-selected="true"] * {{
        color:#5EEAD4 !important;
    }}

    [data-testid="stAlert"] {{
        background:#103B36 !important;
        border-color:#28665A !important;
    }}
    [data-testid="stAlert"] * {{
        color:#D4FAED !important;
    }}

    div[data-testid="stDataFrame"] {{
        border-color:#28515B !important;
    }}

    /* Fix Streamlit three-dot/deploy menu in dark mode */
    div[data-baseweb="popover"] {{
        background:#0D1720 !important;
        color:#F0F8F7 !important;
    }}
    div[data-baseweb="popover"] *,
    div[data-baseweb="menu"] *,
    [role="menu"] *,
    [role="menuitem"] * {{
        color:#F0F8F7 !important;
    }}
}}

/* Portfolio dashboard surface: keeps the surf identity but makes the solved
   analytics look like the presentation mock-up. */
.dashboard-shell {{
    background: linear-gradient(145deg,#071C2B 0%,#082F49 55%,#073B4C 100%);
    border: 1px solid #14566B;
    border-radius: 18px;
    padding: 18px 20px 8px 20px;
    margin: 10px 0 16px 0;
    box-shadow: 0 14px 34px rgba(8,47,73,.16);
}}
.dashboard-shell h2,.dashboard-shell h3,.dashboard-shell p {{ color:#EAF8F6 !important; }}
.dashboard-kicker {{color:#68D5D0;font-size:.78rem;font-weight:700;letter-spacing:.08em;text-transform:uppercase;}}
.dashboard-title {{color:#F7FCFC;font-size:1.35rem;font-weight:800;margin:.15rem 0 .2rem 0;}}
.dashboard-copy {{color:#A9C8CF;font-size:.9rem;margin-bottom:.5rem;}}
/* Solved-state metrics */
div[data-testid="stMetric"] {{ min-height:112px; }}
/* Give Plotly areas a framed, dashboard-like feel without a white box. */
div[data-testid="stPlotlyChart"] {{
    border-radius: 14px;
    overflow: visible;
}}
/* Keep the three overview charts readable without labels colliding. */
[data-testid="stHorizontalBlock"] {{ align-items: stretch; }}
@media (max-width: 1200px) {{
    .dashboard-title {{ font-size:1.2rem; }}
}}
</style>
""", unsafe_allow_html=True)


def money(x): return f"R$ {float(x):,.2f}"
def integer(x): return f"{int(x):,}"

def polish(fig, height=440):
    fig.update_layout(height=height, paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(255,255,255,.45)",
        font=dict(family="Arial", color=INK), margin=dict(l=20,r=20,t=55,b=20),
        legend_title_text="", hoverlabel=dict(bgcolor=WHITE))
    fig.update_xaxes(gridcolor="#E4ECEA", zeroline=False)
    fig.update_yaxes(gridcolor="#E4ECEA", zeroline=False)
    return fig


def cluster_markets(tier1, summary):
    x = tier1[["MarketID","MarketName","PriorityScore","PotentialImpressions","AllocatedBudget"]].merge(
        summary[["MarketID","TotalSpend","TotalImpressions"]], on="MarketID", how="left")
    x["BudgetUtilizationPct"] = np.where(x.AllocatedBudget > 0, x.TotalSpend/x.AllocatedBudget*100, 0)
    x["EffectiveCPM"] = np.where(x.TotalImpressions > 0, x.TotalSpend/x.TotalImpressions*1000, 0)
    features = ["PriorityScore","PotentialImpressions","AllocatedBudget","TotalImpressions","EffectiveCPM","BudgetUtilizationPct"]
    n = min(3, len(x))
    if n >= 2:
        z = StandardScaler().fit_transform(x[features].fillna(0))
        x["Cluster"] = KMeans(n_clusters=n, random_state=42, n_init=20).fit_predict(z)
        profile = x.groupby("Cluster")[features].mean()
        order = profile.sort_values(["TotalImpressions","PriorityScore"], ascending=False).index.tolist()
        labels = ["Priority wave", "Efficient break", "Growth set"][:n]
        mapping = {cluster: labels[i] for i, cluster in enumerate(order)}
        x["MarketProfile"] = x.Cluster.map(mapping)
    else:
        x["Cluster"] = 0; x["MarketProfile"] = "Priority wave"
    return x

# Header — same content, no white container
try:
    db = test_connection()
    sql_badge = f"SQL · {db}"
except Exception as exc:
    st.error("SQL Server unavailable")
    st.exception(exc)
    st.stop()

st.markdown(
    f"""
    <div class="surf-header">
      <div class="surf-header-row">
        <div>
          <div class="surf-header-title">🌊 Media Optimization Engine</div>
          <div class="surf-header-sub">Two-tier decision system for market prioritization and media allocation</div>
          <div class="surf-header-path">SQL Server → heuristic market allocation → Mixed-Integer Programming → validation → analytics</div>
        </div>
        <div class="sql-pill">{sql_badge}</div>
      </div>
    </div>
    """,
    unsafe_allow_html=True,
)

with st.sidebar:
    st.header("Control room")
    st.caption("Run the model against the active campaign and current SQL business rules.")
    save = st.toggle("Save run to SQL Server", value=False)
    run = st.button("Run optimization", type="primary", width="stretch")
    st.divider()
    st.markdown("**Model**")
    st.caption("Tier 1: 60% priority + 40% market opportunity\n\nTier 2: integer optimization in 1,000-impression units")
    st.markdown("**Theme**")
    st.caption("Ocean, reef, sand and sunset — inspired by surf conditions rather than a generic tech dashboard.")

if run:
    with st.spinner("Reading SQL data and solving both optimization tiers..."):
        st.session_state.result = run_full_optimization(save)

if "result" not in st.session_state:
    # Portfolio mode: show the complete solved dashboard immediately on first load.
    # This does NOT save a run to SQL Server. The sidebar button still lets the
    # viewer rerun the model explicitly and optionally persist that run.
    with st.spinner("Loading the current campaign and building the optimization dashboard..."):
        st.session_state.result = run_full_optimization(False)

r = st.session_state.result
campaign = r["campaign"].iloc[0]
tier1 = r["tier1"].copy()
summary = r["tier2_summary"].copy()
details = r["tier2_details"].copy()
validation = r["validation"].copy()
clusters = cluster_markets(tier1, summary)

budget = float(campaign.TotalBudget); spend = float(summary.TotalSpend.sum()); impressions = int(summary.TotalImpressions.sum())
util = spend/budget*100 if budget else 0
all_optimal = bool((summary.SolverStatus == "Optimal").all())
all_valid = bool(validation.Valid.all())

m1,m2,m3,m4,m5 = st.columns(5)
m1.metric("Campaign budget", money(budget))
m2.metric("Actual spend", money(spend), f"{util:.1f}% utilized")
m3.metric("Optimized impressions", integer(impressions))
m4.metric("Selected markets", f"{len(tier1)}")
m5.metric("Solver", "Optimal" if all_optimal else "Review")

if all_optimal and all_valid:
    st.success("Optimization solved successfully · all configured channel constraints are satisfied.")
else:
    st.warning("The run completed, but at least one solver or business-rule check needs review.")
if r.get("run_id"):
    st.info(f"Saved to SQL Server as RunID {r['run_id']}.")

tabs = st.tabs(["Overview","3D allocation","Market clusters","Channel mix","Rules & validation","Data explorer","How it works","Run history"])

with tabs[0]:
    st.markdown("""<div class="dashboard-shell"><div class="dashboard-kicker">Solved media plan</div><div class="dashboard-title">Optimization command view</div><div class="dashboard-copy">One view of the market landscape, channel mix and market-level spend produced by the two-tier engine.</div></div>""", unsafe_allow_html=True)

    c1, c2, c3 = st.columns([1.18, .82, 1.20], gap="large")
    with c1:
        p3 = clusters.copy()
        fig = px.scatter_3d(
            p3, x="PriorityScore", y="AllocatedBudget", z="TotalImpressions",
            size="PotentialImpressions", color="MarketProfile", hover_name="MarketName",
            title="3D optimization landscape",
            labels={"PriorityScore":"Priority","AllocatedBudget":"Budget (R$)","TotalImpressions":"Impressions"},
            color_discrete_sequence=["#28C7C7", "#4D9DE0", CORAL],
        )
        fig.update_traces(marker=dict(opacity=.9, line=dict(width=.6, color="#DDF4F1")))
        fig.update_layout(
            height=390, paper_bgcolor="#082A3A", font=dict(family="Arial", color="#DDF4F1", size=11),
            title=dict(font=dict(size=17), x=0.5, xanchor="center"),
            margin=dict(l=28,r=12,t=55,b=18), legend=dict(bgcolor="rgba(0,0,0,0)",font=dict(size=9), x=.70, y=.98),
            scene=dict(bgcolor="#082A3A",
                xaxis=dict(backgroundcolor="#0B3444",gridcolor="#285D6B",color="#DDF4F1",showbackground=True),
                yaxis=dict(backgroundcolor="#0A3040",gridcolor="#285D6B",color="#DDF4F1",showbackground=True),
                zaxis=dict(backgroundcolor="#0D3948",gridcolor="#285D6B",color="#DDF4F1",showbackground=True),
                camera=dict(eye=dict(x=1.45,y=1.45,z=.95))),
        )
        st.plotly_chart(fig, width="stretch", theme=None)

    channel = details.groupby("Channel",as_index=False).agg(Spend=("Spend","sum"),PurchasedImpressions=("PurchasedImpressions","sum"))
    with c2:
        fig = px.pie(channel, names="Channel", values="Spend", hole=.58, title="Spend by channel",
            color="Channel", color_discrete_map=CHANNEL_COLORS)
        fig.update_traces(textposition="inside", textinfo="percent")
        fig.update_layout(height=390,paper_bgcolor="#082A3A",font=dict(family="Arial",color="#DDF4F1",size=11),
            title=dict(font=dict(size=17), x=0.5, xanchor="center"),
            margin=dict(l=12,r=12,t=55,b=48),legend=dict(orientation="h",y=-.08,x=.5,xanchor="center",bgcolor="rgba(0,0,0,0)",font=dict(size=10)))
        st.plotly_chart(fig,width="stretch",theme=None)

    with c3:
        pivot = details.pivot_table(index="MarketName",columns="Channel",values="Spend",aggfunc="sum",fill_value=0).reset_index()
        order = summary.sort_values("TotalImpressions",ascending=True).MarketName.tolist()
        pivot["MarketName"] = pd.Categorical(pivot["MarketName"], categories=order, ordered=True)
        pivot = pivot.sort_values("MarketName")
        fig = go.Figure()
        for ch in [c for c in ["Social","Display","Video"] if c in pivot.columns]:
            fig.add_bar(name=ch,y=pivot.MarketName,x=pivot[ch],orientation="h",marker_color=CHANNEL_COLORS[ch])
        fig.update_layout(height=390,barmode="stack",title="Channel spend by market",paper_bgcolor="#082A3A",plot_bgcolor="#082A3A",
            font=dict(family="Arial",color="#DDF4F1",size=10),title_font=dict(size=17),title_x=.5,
            margin=dict(l=105,r=16,t=55,b=58),legend=dict(orientation="h",y=-.18,x=.5,xanchor="center",font=dict(size=10)),
            xaxis=dict(gridcolor="#285D6B",title=dict(text="Spend (R$)",standoff=8),tickformat="~s",automargin=True),
            yaxis=dict(gridcolor="#173F4D",title="",automargin=True,tickfont=dict(size=10)))
        st.plotly_chart(fig,width="stretch",theme=None)

    merged = tier1[["MarketID","MarketName","HeuristicScore","AllocatedBudget"]].merge(summary, on=["MarketID","MarketName"])
    merged["BudgetUtilizationPct"] = merged.TotalSpend/merged.AllocatedBudget*100
    st.dataframe(merged[["MarketName","HeuristicScore","AllocatedBudget","TotalSpend","BudgetUtilizationPct","TotalImpressions","SolverStatus"]], width="stretch", hide_index=True)

with tabs[1]:
    st.subheader("The optimization landscape")
    st.caption("Rotate and zoom. X shows business priority, Y shows Tier 1 budget, Z shows Tier 2 delivered impressions; bubble size reflects market opportunity.")
    p3 = clusters.copy()
    fig = px.scatter_3d(p3, x="PriorityScore", y="AllocatedBudget", z="TotalImpressions",
        size="PotentialImpressions", color="MarketProfile", hover_name="MarketName",
        labels={"PriorityScore":"Priority score","AllocatedBudget":"Allocated budget (R$)","TotalImpressions":"Optimized impressions"},
        color_discrete_sequence=[OCEAN, REEF, CORAL])
    fig.update_traces(marker=dict(opacity=.82, line=dict(width=1, color=WHITE)))
    fig.update_layout(
        height=650,
        paper_bgcolor="rgba(0,0,0,0)",
        font=dict(family="Arial", color=INK),
        margin=dict(l=0,r=0,t=20,b=0),
        legend=dict(bgcolor="rgba(0,0,0,0)"),
        scene=dict(
            bgcolor="#0B3040",
            xaxis=dict(
                title="Priority score",
                backgroundcolor="#0E3947",
                gridcolor="#376975",
                zerolinecolor="#5D8991",
                color="#DDF4F1",
                showbackground=True,
            ),
            yaxis=dict(
                title="Allocated budget (R$)",
                backgroundcolor="#103C49",
                gridcolor="#376975",
                zerolinecolor="#5D8991",
                color="#DDF4F1",
                showbackground=True,
            ),
            zaxis=dict(
                title="Optimized impressions",
                backgroundcolor="#123F4B",
                gridcolor="#376975",
                zerolinecolor="#5D8991",
                color="#DDF4F1",
                showbackground=True,
            ),
            camera=dict(eye=dict(x=1.45, y=1.45, z=.95)),
            aspectmode="cube",
        ),
    )
    st.plotly_chart(fig, width="stretch", theme=None)

with tabs[2]:
    st.subheader("Market clustering")
    st.caption("K-Means groups solved markets using standardized priority, opportunity, budget, delivered impressions, effective CPM and budget utilization. Clusters are descriptive portfolio segments — they do not change the optimizer.")
    c1,c2 = st.columns([1.1,1])
    with c1:
        fig = px.scatter(clusters, x="PriorityScore", y="TotalImpressions", size="AllocatedBudget",
            color="MarketProfile", hover_name="MarketName", title="Priority vs delivered impressions",
            color_discrete_sequence=[OCEAN, REEF, CORAL])
        st.plotly_chart(polish(fig), width="stretch")
    with c2:
        fig = px.scatter(clusters, x="EffectiveCPM", y="BudgetUtilizationPct", size="PotentialImpressions",
            color="MarketProfile", hover_name="MarketName", title="Efficiency vs budget utilization",
            labels={"EffectiveCPM":"Effective CPM (R$)","BudgetUtilizationPct":"Budget utilization (%)"},
            color_discrete_sequence=[OCEAN, REEF, CORAL])
        st.plotly_chart(polish(fig), width="stretch")
    st.dataframe(clusters[["MarketName","MarketProfile","PriorityScore","PotentialImpressions","AllocatedBudget","TotalImpressions","EffectiveCPM","BudgetUtilizationPct"]], width="stretch", hide_index=True)

with tabs[3]:
    channel = details.groupby("Channel",as_index=False).agg(Spend=("Spend","sum"),PurchasedImpressions=("PurchasedImpressions","sum"))
    ch1,ch2 = st.columns(2)
    with ch1:
        fig = px.pie(channel, names="Channel", values="Spend", hole=.55, title="Spend by channel",
            color="Channel", color_discrete_map=CHANNEL_COLORS)
        fig.update_layout(height=430, paper_bgcolor="rgba(0,0,0,0)", font=dict(family="Arial",color=INK))
        st.plotly_chart(fig, width="stretch")
    with ch2:
        pivot = details.pivot_table(index="MarketName",columns="Channel",values="Spend",aggfunc="sum",fill_value=0).reset_index()
        fig = go.Figure()
        for ch in [c for c in ["Social","Display","Video"] if c in pivot.columns]:
            fig.add_bar(name=ch, y=pivot.MarketName, x=pivot[ch], orientation="h", marker_color=CHANNEL_COLORS[ch])
        fig.update_layout(barmode="stack", title="Channel spend inside each market")
        st.plotly_chart(polish(fig), width="stretch")
    st.dataframe(channel, width="stretch", hide_index=True)

with tabs[4]:
    rules = load_channel_constraints().copy()
    rules["Minimum"] = (rules.MinBudgetPercent*100).round(1)
    rules["Maximum"] = (rules.MaxBudgetPercent*100).round(1)
    st.subheader("Business rules loaded from SQL Server")
    st.dataframe(rules[["Channel","Minimum","Maximum"]], width="stretch", hide_index=True)
    valid_plot = validation.copy()
    valid_plot["Status"] = np.where(valid_plot.Valid, "Within rule", "Review")
    fig = px.scatter(valid_plot, x="BudgetSharePct", y="MarketName", color="Channel", symbol="Status",
        hover_data=["RequiredMinPct","RequiredMaxPct","Spend"], title="Actual channel share by market",
        labels={"BudgetSharePct":"Share of market budget (%)","MarketName":""}, color_discrete_map=CHANNEL_COLORS)
    st.plotly_chart(polish(fig, 500), width="stretch")
    if all_valid: st.success("All constraints satisfied.")
    else: st.warning("One or more constraints require review.")
    st.dataframe(validation, width="stretch", hide_index=True)

with tabs[5]:
    st.subheader("Allocation explorer")
    markets = sorted(details.MarketName.unique().tolist()); channels = sorted(details.Channel.unique().tolist())
    f1,f2 = st.columns(2)
    chosen_markets = f1.multiselect("Markets", markets, default=markets)
    chosen_channels = f2.multiselect("Channels", channels, default=channels)
    view = details[details.MarketName.isin(chosen_markets) & details.Channel.isin(chosen_channels)].copy()
    st.dataframe(view, width="stretch", hide_index=True)
    st.download_button("Download allocation CSV", view.to_csv(index=False).encode("utf-8"), "media_allocation.csv", "text/csv")

with tabs[6]:
    st.subheader("How the engine makes the decision")
    st.markdown("""
<div class='surf-card'><b>1 · SQL Server is the source of truth</b><br><span class='small-note'>Markets, campaign budget, inventory, CPM, minimum purchases and channel rules are read from the database rather than embedded in the dashboard.</span></div>
<div class='surf-card'><b>2 · Tier 1 narrows the search</b><br><span class='small-note'>Markets are scored from business priority (60%) and potential impressions (40%). The heuristic selects markets and allocates the campaign budget while respecting each market's minimum and maximum budget.</span></div>
<div class='surf-card'><b>3 · Tier 2 solves the media plan</b><br><span class='small-note'>A Mixed-Integer Programming model buys inventory in 1,000-impression units. Binary variables activate inventory lines, integer variables determine quantity, and the objective maximizes delivered impressions.</span></div>
<div class='surf-card'><b>4 · Constraints keep the answer usable</b><br><span class='small-note'>The model respects available inventory, minimum purchase quantities, market budgets, and SQL-driven minimum/maximum channel shares.</span></div>
<div class='surf-card'><b>5 · Validation and persistence close the loop</b><br><span class='small-note'>Solver status and channel shares are checked after optimization. A run can then be persisted to SQL Server for auditability and comparison.</span></div>
""", unsafe_allow_html=True)
    st.code("SQL Server  →  Tier 1 Heuristic  →  Tier 2 MIP  →  Validation  →  SQL Results + Streamlit", language=None)

with tabs[7]:
    st.subheader("Saved optimization runs")
    history = load_run_history()
    if history.empty:
        st.info("No saved run history is available yet, or the result tables have not been created.")
    else:
        st.dataframe(history, width="stretch", hide_index=True)
        h = history.sort_values("RunID")
        fig = px.line(h, x="RunID", y="TotalImpressions", markers=True, title="Delivered impressions across saved runs",
            color_discrete_sequence=[REEF])
        st.plotly_chart(polish(fig), width="stretch")
