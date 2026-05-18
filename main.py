import io
from datetime import datetime

import pandas as pd
import plotly.express as px
import requests
import streamlit as st

# =====================================================
# PAGE CONFIG
# =====================================================

st.set_page_config(
    page_title="VDK Marketing Dashboard",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded"
)

# =====================================================
# SIDEBAR NAVIGATION
# =====================================================

with st.sidebar:
    
    st.markdown("""
    <style>
    .sidebar-title {
        font-size: 24px;
        font-weight: 700;
        margin-bottom: 30px;
        padding-bottom: 15px;
        border-bottom: 2px solid rgba(255,255,255,0.2);
    }
    .nav-item {
        padding: 12px 16px;
        margin: 8px 0;
        border-radius: 10px;
        text-decoration: none;
        display: block;
        transition: 0.2s;
    }
    .nav-item:hover {
        background: rgba(255,255,255,0.1);
    }
    </style>
    """, unsafe_allow_html=True)
    
    st.markdown('<div class="sidebar-title">📊 Dashboards</div>', unsafe_allow_html=True)
    
    # Dashboard links
    col1, col2 = st.columns(2)
    
    with col1:
        if st.button("🏠 Home", use_container_width=True):
            st.rerun()
    
    with col2:
        if st.button("📱 Social", use_container_width=True):
            pass
    
    col1, col2 = st.columns(2)
    
    with col1:
        if st.button("👥 Members", use_container_width=True):
            pass
    
    with col2:
        if st.button("✉️ Mailbox", use_container_width=True):
            pass
    
    col1, col2 = st.columns(2)
    
    with col1:
        if st.button("📅 Events", use_container_width=True):
            pass
    
    with col2:
        if st.button("📊 Reports", use_container_width=True):
            pass
    
    st.divider()
    
    st.markdown('<div class="sidebar-title">⚙️ Instellingen</div>', unsafe_allow_html=True)
    
    if st.button("🔄 Vernieuwen", use_container_width=True):
        st.cache_data.clear()
        st.rerun()
    
    st.divider()
    
    st.markdown("""
    <div style="font-size: 12px; opacity: 0.7; margin-top: 30px; text-align: center;">
    <p><strong>VDK Marketing</strong></p>
    <p>v1.0 • 2026</p>
    </div>
    """, unsafe_allow_html=True)

# =====================================================
# STYLING
# =====================================================

st.markdown("""
<link rel="stylesheet" href="https://use.typekit.net/nap5xax.css">

<style>

html, body, [data-testid="stAppViewContainer"]{
    background:#f4efe6;
    font-family:'sofia-pro', sans-serif;
}

.block-container{
    padding-top:35px;
    padding-left:55px;
    padding-right:55px;
    padding-bottom:55px;
    max-width:1800px;
}

/* MENU */

#MainMenu{
    visibility:hidden;
}

footer{
    visibility:hidden;
}

/* SIDEBAR */

section[data-testid="stSidebar"]{
    background:linear-gradient(180deg,#084422 0%, #063319 100%);
    border-right:2px solid rgba(255,255,255,0.1);
    padding-top:20px;
}

section[data-testid="stSidebar"] * {
    color:white !important;
}

section[data-testid="stSidebar"] button {
    background: rgba(255,255,255,0.1) !important;
    color: white !important;
    border: 1px solid rgba(255,255,255,0.15) !important;
    border-radius: 10px !important;
    font-weight: 600 !important;
}

section[data-testid="stSidebar"] button:hover {
    background: rgba(255,255,255,0.2) !important;
    border: 1px solid rgba(255,255,255,0.3) !important;
}

/* HERO */

.hero{
    background:linear-gradient(135deg,#084422 0%, #0f5f33 100%);
    padding:60px;
    border-radius:34px;
    color:white;
    margin-bottom:50px;
    box-shadow:0 12px 30px rgba(8,68,34,0.15);
}

.hero h1 {
    margin: 0;
    padding: 0;
}

/* KPI */

[data-testid="stMetric"]{
    background:white;
    padding:28px;
    border-radius:24px;
    border:1px solid rgba(8,68,34,0.05);
    box-shadow:0 10px 25px rgba(8,68,34,0.05);
    transition:0.2s;
}

[data-testid="stMetric"]:hover {
    box-shadow:0 15px 35px rgba(8,68,34,0.1);
    transform:translateY(-2px);
}

/* BUTTONS */

div.stButton > button{
    width:100%;
    background:white;
    color:#084422;
    border:2px solid rgba(8,68,34,0.1);
    border-radius:22px;
    padding:28px 20px;
    text-align:left;
    font-size:18px;
    font-weight:700;
    box-shadow:0 8px 20px rgba(8,68,34,0.05);
    transition:0.2s;
    min-height:100px;
}

div.stButton > button:hover{
    background:#084422;
    color:white;
    border:2px solid #084422;
    transform:translateY(-4px);
    box-shadow:0 15px 35px rgba(8,68,34,0.15);
}

/* GRAPH */

.graph-card{
    background:white;
    padding:30px;
    border-radius:28px;
    box-shadow:0 10px 25px rgba(8,68,34,0.05);
    border:1px solid rgba(8,68,34,0.05);
}

.dashboard-section {
    margin-top: 50px;
    margin-bottom: 50px;
}

.section-title {
    font-size: 28px;
    font-weight: 700;
    color: #084422;
    margin-bottom: 25px;
    padding-bottom: 12px;
    border-bottom: 3px solid #084422;
    display: inline-block;
}

.feature-grid {
    display: grid;
    grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
    gap: 20px;
    margin-top: 30px;
}

.feature-card {
    background: white;
    padding: 25px;
    border-radius: 20px;
    box-shadow: 0 8px 20px rgba(8,68,34,0.05);
    border-left: 4px solid #084422;
    transition: 0.2s;
}

.feature-card:hover {
    transform: translateY(-4px);
    box-shadow: 0 12px 30px rgba(8,68,34,0.1);
}

.feature-card h4 {
    color: #084422;
    margin-top: 10px;
}

h1,h2,h3 {
    color:#084422;
}

.divider-line {
    height: 2px;
    background: linear-gradient(90deg, transparent, #084422, transparent);
    margin: 40px 0;
}

.footer-info {
    background: rgba(8,68,34,0.05);
    padding: 25px;
    border-radius: 20px;
    margin-top: 50px;
    text-align: center;
    border-top: 2px solid #084422;
}

.stat-box {
    background: white;
    padding: 20px;
    border-radius: 16px;
    box-shadow: 0 6px 15px rgba(8,68,34,0.05);
    text-align: center;
}

.stat-value {
    font-size: 32px;
    font-weight: 700;
    color: #084422;
}

.stat-label {
    font-size: 14px;
    color: #666;
    margin-top: 8px;
}

</style>
""", unsafe_allow_html=True)

# =====================================================
# FUNCTIONS
# =====================================================

def load_csv(url):

    try:

        headers = {
            "User-Agent": "Mozilla/5.0"
        }

        response = requests.get(
            url,
            headers=headers,
            timeout=20
        )

        response.raise_for_status()

        return pd.read_csv(
            io.StringIO(response.text)
        )

    except:

        return pd.DataFrame()


def calculate_growth(current, previous):

    if previous == 0:
        return 0

    return round(
        ((current - previous) / previous) * 100,
        1
    )

# =====================================================
# SOCIAL DATA
# =====================================================

SOCIAL_SHEET = "1L-KVqx5Bg5Y18PiqncQLggX3oKpeMHtqmRnsmJ5Qziw"
FOLLOWERS_GID = "730161295"

followers_url = (
    f"https://docs.google.com/spreadsheets/d/"
    f"{SOCIAL_SHEET}/export?format=csv&gid={FOLLOWERS_GID}"
)

followers = load_csv(followers_url)

instagram_followers = 0
facebook_followers = 0

instagram_growth = 0
facebook_growth = 0

if not followers.empty:

    followers.columns = (
        followers.columns
        .str.lower()
        .str.strip()
    )

    followers["instagram_followers"] = pd.to_numeric(
        followers["instagram_followers"],
        errors="coerce"
    )

    followers["facebook_followers"] = pd.to_numeric(
        followers["facebook_followers"],
        errors="coerce"
    )

    followers = followers.dropna()

    if len(followers) >= 2:

        current = followers.iloc[-1]
        previous = followers.iloc[-2]

        instagram_followers = int(
            current["instagram_followers"]
        )

        facebook_followers = int(
            current["facebook_followers"]
        )

        instagram_growth = calculate_growth(
            instagram_followers,
            int(previous["instagram_followers"])
        )

        facebook_growth = calculate_growth(
            facebook_followers,
            int(previous["facebook_followers"])
        )

# =====================================================
# HERO SECTION
# =====================================================

st.markdown(f"""
<div class="hero">

<h1 style="
    color:white;
    font-size:64px;
    margin-bottom:16px;
    line-height:1.1;
">
📊 VDK Marketing Dashboard
</h1>

<p style="
    font-size:20px;
    opacity:0.95;
    max-width:900px;
    line-height:1.8;
">
Centraal overzicht van alle marketing prestaties binnen social media, members, nieuwsbrieven en afspraken. Real-time data en automatische actualisering.
</p>

<p style="
    margin-top:30px;
    font-size:16px;
    opacity:0.85;
    display:flex;
    gap:30px;
">
    <span>📅 {datetime.now().strftime('%d %B %Y')}</span>
    <span>🔄 Live update</span>
</p>

</div>
""", unsafe_allow_html=True)

st.write("")

# =====================================================
# KPI OVERVIEW SECTION
# =====================================================

st.markdown('<div class="section-title">📈 Snelle statistieken</div>', unsafe_allow_html=True)

st.write("")

col1, col2, col3, col4 = st.columns(4, gap="medium")

with col1:
    st.metric(
        label="Instagram volgers",
        value=f"{instagram_followers:,}".replace(",", "."),
        delta=f"{instagram_growth:+.1f}%"
    )

with col2:
    st.metric(
        label="Facebook volgers",
        value=f"{facebook_followers:,}".replace(",", "."),
        delta=f"{facebook_growth:+.1f}%"
    )

with col3:
    st.metric(
        label="Totale volgers",
        value=f"{(instagram_followers + facebook_followers):,}".replace(",", "."),
        delta="Gecombineerd"
    )

with col4:
    st.metric(
        label="Kanalen actief",
        value="2",
        delta="Instagram + Facebook"
    )

st.write("")

st.write("")

# =====================================================
# DASHBOARD NAVIGATION SECTION
# =====================================================

st.markdown('<div class="section-title">🎯 Dashboards</div>', unsafe_allow_html=True)

st.markdown("""
Selecteer een dashboard om meer gedetailleerde informatie en analysen te bekijken.
""")

st.write("")

col1, col2 = st.columns(2, gap="large")

with col1:
    st.button(
        "📱 Social Media\n\nInstagram • Facebook\nVolgers • Engagement • Posts",
        use_container_width=True,
        key="btn_social"
    )

with col2:
    st.button(
        "👥 Members\n\nLidmaatschappen • Groei\nActivatie • Omzet • Trends",
        use_container_width=True,
        key="btn_members"
    )

st.write("")

col3, col4 = st.columns(2, gap="large")

with col3:
    st.button(
        "✉️ Nieuwsbrief\n\nCampagnes • Open rates\nClicks • Bounces • Unsubscribes",
        use_container_width=True,
        key="btn_newsletter"
    )

with col4:
    st.button(
        "📅 Afspraken\n\nPlanning • Kalender\nEvents • Analyses • Rapportages",
        use_container_width=True,
        key="btn_events"
    )

# =====================================================
# FOLLOWER GRAPH SECTION
# =====================================================

if not followers.empty:

    st.markdown('<div class="divider-line"></div>', unsafe_allow_html=True)
    
    st.markdown('<div class="section-title">📊 Volgers ontwikkeling</div>', unsafe_allow_html=True)
    
    st.markdown("""
    Historische trend van je Instagram en Facebook volgers over tijd.
    """)

    st.write("")

    chart_df = followers.copy()

    chart_df["date"] = pd.to_datetime(
        chart_df["date"],
        errors="coerce"
    )

    chart_df = chart_df.sort_values("date")

    fig = px.line(
        chart_df,
        x="date",
        y=[
            "instagram_followers",
            "facebook_followers"
        ],
        template="simple_white",
        labels={
            "date": "Datum",
            "value": "Volgers",
            "variable": "Platform"
        }
    )

    fig.update_layout(
        height=500,
        paper_bgcolor="white",
        plot_bgcolor="#f9f9f9",
        margin=dict(l=10, r=10, t=10, b=10),
        legend=dict(
            orientation="h",
            yanchor="bottom",
            y=1.02,
            xanchor="right",
            x=1
        ),
        xaxis_title="",
        yaxis_title="Aantal volgers",
        hovermode="x unified"
    )

    fig.update_traces(
        line=dict(width=3),
        mode='lines+markers'
    )

    with st.container():
        st.markdown(
            '<div class="graph-card">',
            unsafe_allow_html=True
        )

        st.plotly_chart(
            fig,
            use_container_width=True,
            config={"displayModeBar": True, "displaylogo": False}
        )

        st.markdown(
            '</div>',
            unsafe_allow_html=True
        )

# =====================================================
# FEATURES SECTION
# =====================================================

st.markdown('<div class="divider-line"></div>', unsafe_allow_html=True)

st.markdown('<div class="section-title">✨ Functies</div>', unsafe_allow_html=True)

col1, col2, col3 = st.columns(3, gap="medium")

with col1:
    st.markdown("""
    <div class="feature-card">
        <div style="font-size: 36px;">⚡</div>
        <h4>Real-time Data</h4>
        <p>Automatische updates van je Google Sheets integratties</p>
    </div>
    """, unsafe_allow_html=True)

with col2:
    st.markdown("""
    <div class="feature-card">
        <div style="font-size: 36px;">📈</div>
        <h4>Interactieve Grafieken</h4>
        <p>Plotly grafieken met hover, zoom en export functies</p>
    </div>
    """, unsafe_allow_html=True)

with col3:
    st.markdown("""
    <div class="feature-card">
        <div style="font-size: 36px;">🎨</div>
        <h4>Modern Design</h4>
        <p>Responsieve layout met professionele styling</p>
    </div>
    """, unsafe_allow_html=True)

col1, col2, col3 = st.columns(3, gap="medium")

with col1:
    st.markdown("""
    <div class="feature-card">
        <div style="font-size: 36px;">📊</div>
        <h4>KPI Metrics</h4>
        <p>Snelle overzichten van je belangijkste indicatoren</p>
    </div>
    """, unsafe_allow_html=True)

with col2:
    st.markdown("""
    <div class="feature-card">
        <div style="font-size: 36px;">🔄</div>
        <h4>Sincronisatie</h4>
        <p>Gesynchroniseerde data uit meerdere bronnen</p>
    </div>
    """, unsafe_allow_html=True)

with col3:
    st.markdown("""
    <div class="feature-card">
        <div style="font-size: 36px;">🛡️</div>
        <h4>Betrouwbaar</h4>
        <p>Gegevens rechtstreeks van Google Sheets</p>
    </div>
    """, unsafe_allow_html=True)

# =====================================================
# FOOTER
# =====================================================

st.markdown('<div class="divider-line"></div>', unsafe_allow_html=True)

st.markdown(f"""
<div class="footer-info">
    <h3>📋 Dashboard Informatie</h3>
    <p><strong>Databronnen:</strong> Google Sheets API</p>
    <p><strong>Actualisering:</strong> Elk uur automatisch</p>
    <p><strong>Vertraging:</strong> ~15 seconden bij laden</p>
    <p style="margin-top: 20px; font-size: 14px; opacity: 0.7;">
        Laatst bijgewerkt: {datetime.now().strftime('%d %B %Y om %H:%M')} • VDK Marketing © 2026
    </p>
</div>
""", unsafe_allow_html=True)
