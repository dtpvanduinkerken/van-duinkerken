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
# SIDEBAR
# =====================================================

with st.sidebar:

    st.markdown("## Dashboard")

    st.page_link(
        "pages/social-media.py",
        label="Social Media",
        icon="📱"
    )

    st.page_link(
        "pages/Nieuwsbrief.py",
        label="Nieuwsbrieven",
        icon="✉️"
    )

    st.page_link(
        "pages/Members.py",
        label="Members",
        icon="👥"
    )

    st.page_link(
        "pages/afspraken.py",
        label="Afspraken",
        icon="📅"
    )

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
    background:#084422;
    border-right:none;
}

section[data-testid="stSidebar"] *{
    color:white !important;
}

/* HERO */

.hero{
    background:linear-gradient(135deg,#084422 0%, #0f5f33 100%);
    padding:50px;
    border-radius:34px;
    color:white;
    margin-bottom:40px;
    box-shadow:0 12px 30px rgba(8,68,34,0.15);
}

/* KPI */

[data-testid="stMetric"]{
    background:white;
    padding:28px;
    border-radius:24px;
    border:1px solid rgba(8,68,34,0.05);
    box-shadow:0 10px 25px rgba(8,68,34,0.05);
}

/* BUTTONS */

div.stButton > button{
    width:100%;
    background:white;
    color:#084422;
    border:none;
    border-radius:22px;
    padding:28px 20px;
    text-align:left;
    font-size:20px;
    font-weight:700;
    box-shadow:0 8px 20px rgba(8,68,34,0.05);
    transition:0.2s;
    min-height:120px;
}

div.stButton > button:hover{
    background:#ffffff;
    border:none;
    transform:translateY(-2px);
    box-shadow:0 12px 25px rgba(8,68,34,0.08);
    color:#084422;
}

/* GRAPH */

.graph-card{
    background:white;
    padding:30px;
    border-radius:28px;
    box-shadow:0 10px 25px rgba(8,68,34,0.05);
}

h1,h2,h3{
    color:#084422;
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
# HERO
# =====================================================

st.markdown(f"""
<div class="hero">

<h1 style="
    color:white;
    font-size:62px;
    margin-bottom:14px;
    line-height:1;
">
VDK Marketing Dashboard
</h1>

<p style="
    font-size:20px;
    opacity:0.92;
    max-width:850px;
    line-height:1.7;
">
Centraal overzicht van alle marketing prestaties binnen
social media, members, nieuwsbrieven en afspraken.
</p>

<p style="
    margin-top:30px;
    font-size:17px;
    opacity:0.8;
">
{datetime.now().strftime('%d %B %Y')}
</p>

</div>
""", unsafe_allow_html=True)

# =====================================================
# KPI OVERVIEW
# =====================================================

st.markdown("## KPI overzicht")

st.write("")

col1, col2, col3, col4 = st.columns(4)

with col1:

    st.metric(
        label="Instagram volgers",
        value=f"{instagram_followers}",
        delta=f"{instagram_growth}%"
    )

with col2:

    st.metric(
        label="Facebook volgers",
        value=f"{facebook_followers}",
        delta=f"{facebook_growth}%"
    )

with col3:

    st.metric(
        label="Totale volgers",
        value=f"{instagram_followers + facebook_followers}"
    )

with col4:

    st.metric(
        label="Kanalen",
        value="2"
    )

st.write("")
st.write("")

# =====================================================
# DASHBOARD BUTTONS
# =====================================================

st.markdown("## Dashboard overzicht")

st.write("")

col1, col2 = st.columns(2, gap="large")

with col1:

    if st.button(
        "📱 Social media\n\nInstagram, Facebook en engagement prestaties",
        use_container_width=True
    ):
        st.switch_page("pages/Social_Media.py")

with col2:

    if st.button(
        "👥 Members\n\nGroei, activatie en omzet prestaties",
        use_container_width=True
    ):
        st.switch_page("pages/Members.py")

st.write("")

col3, col4 = st.columns(2, gap="large")

with col3:

    if st.button(
        "✉️ Nieuwsbrief\n\nOpen rates, clicks en campagnes",
        use_container_width=True
    ):
        st.switch_page("pages/Nieuwsbrief.py")

with col4:

    if st.button(
        "📅 Afspraken\n\nPlanning, afspraken en analyses",
        use_container_width=True
    ):
        st.switch_page("pages/afspraken.py")

st.write("")
st.write("")

# =====================================================
# FOLLOWER GRAPH
# =====================================================

if not followers.empty:

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
        template="simple_white"
    )

    fig.update_layout(
        height=450,
        paper_bgcolor="white",
        plot_bgcolor="white",
        margin=dict(
            l=10,
            r=10,
            t=10,
            b=10
        ),
        legend_title="",
        xaxis_title="",
        yaxis_title=""
    )

    st.markdown("## Volgers ontwikkeling")

    with st.container():

        st.markdown(
            '<div class="graph-card">',
            unsafe_allow_html=True
        )

        st.plotly_chart(
            fig,
            use_container_width=True
        )

        st.markdown(
            '</div>',
            unsafe_allow_html=True
        )
