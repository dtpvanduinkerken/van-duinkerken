import io
from datetime import datetime

import pandas as pd
import plotly.express as px
import requests
import streamlit as st

# =========================
# PAGE CONFIG
# =========================

st.set_page_config(
    page_title="Social media dashboard",
    layout="wide",
    initial_sidebar_state="expanded"
)

# =========================
# STYLING
# =========================

STYLE = """
<link rel="stylesheet" href="https://use.typekit.net/nap5xax.css">

<style>

html, body, [data-testid="stAppViewContainer"]{
    background:#f4efe6;
    font-family:'sofia-pro', sans-serif;
}

.stApp{
    background:#f4efe6;
}

.block-container{
    padding-top:35px;
    padding-left:40px;
    padding-right:40px;
    padding-bottom:40px;
    max-width:100%;
}

#MainMenu,
footer{
    visibility:hidden;
}

section[data-testid="stSidebar"]{
    background:#084422;
}

section[data-testid="stSidebar"] *{
    color:white !important;
}

.vdk-main-title{
    font-size:54px;
    font-weight:700;
    color:#084422;
    margin:0;
}

.vdk-date{
    text-align:right;
    color:#084422;
    font-size:18px;
    margin-top:14px;
}

.vdk-divider{
    width:100%;
    height:1px;
    background:rgba(8,68,34,0.12);
    margin-top:30px;
    margin-bottom:50px;
}

.kpi-wrapper{
    background:#ffffff;
    border-radius:24px;
    padding:26px;
    box-shadow:0 10px 25px rgba(8,68,34,0.05);
    min-height:170px;
}

.kpi-label{
    color:#9b9b9b;
    font-size:15px;
    margin-bottom:24px;
}

.kpi-value{
    color:#3d3f4d;
    font-size:48px;
    font-weight:700;
    line-height:1;
}

.kpi-growth{
    margin-top:16px;
    font-size:22px;
    font-weight:700;
}

[data-testid="stDataFrame"]{
    border-radius:24px !important;
    overflow:hidden;
}

div[data-testid="stPlotlyChart"]{
    border-radius:24px !important;
    overflow:hidden;
    background:white;
    padding:15px;
    box-shadow:0 10px 25px rgba(8,68,34,0.05);
}

.space{
    height:50px;
}

</style>
"""

st.markdown(STYLE, unsafe_allow_html=True)

# =========================
# SIDEBAR NAVIGATION
# =========================

with st.sidebar:

    st.markdown("## 📊 VDK Marketing")

    if st.button("🏠 Home", use_container_width=True):
        st.switch_page("main.py")

    if st.button("📱 Social Media", use_container_width=True):
        st.rerun()

    if st.button("👥 Members", use_container_width=True):
        st.switch_page("pages/members.py")

    if st.button("✉️ Nieuwsbrief", use_container_width=True):
        st.switch_page("pages/nieuwsbrief.py")

    if st.button("📅 Afspraken", use_container_width=True):
        st.switch_page("pages/afspraken.py")

# =========================
# GOOGLE SHEETS
# =========================

SHEET_ID = "1L-KVqx5Bg5Y18PiqncQLggX3oKpeMHtqmRnsmJ5Qziw"

INSTAGRAM_GID = "0"
FACEBOOK_GID = "847206611"
FOLLOWERS_GID = "730161295"

# =========================
# HELPERS
# =========================

def get_sheet_url(gid):

    return (
        f"https://docs.google.com/spreadsheets/d/"
        f"{SHEET_ID}/export?format=csv&gid={gid}"
    )

def normalize_columns(df):

    df.columns = (
        df.columns
        .str.strip()
        .str.lower()
        .str.replace(" ", "_")
        .str.replace("-", "_")
    )

    return df

def fetch_sheet(gid):

    try:

        response = requests.get(
            get_sheet_url(gid),
            timeout=20
        )

        response.raise_for_status()

        df = pd.read_csv(
            io.StringIO(response.text)
        )

        return normalize_columns(df)

    except:

        return pd.DataFrame()

# =========================
# LOAD DATA
# =========================

@st.cache_data(ttl=300)
def load_data():

    instagram = fetch_sheet(INSTAGRAM_GID)
    facebook = fetch_sheet(FACEBOOK_GID)
    followers = fetch_sheet(FOLLOWERS_GID)

    if not instagram.empty:
        instagram["channel"] = "Instagram"

    if not facebook.empty:
        facebook["channel"] = "Facebook"

    posts = pd.concat(
        [instagram, facebook],
        ignore_index=True
    )

    numeric_cols = [
        "likes",
        "views",
        "comments",
        "shares",
        "saves"
    ]

    for col in numeric_cols:

        if col in posts.columns:

            posts[col] = pd.to_numeric(
                posts[col],
                errors="coerce"
            ).fillna(0)

    if "date" in posts.columns:

        posts["date"] = pd.to_datetime(
            posts["date"],
            errors="coerce"
        )

    if all(
        col in posts.columns
        for col in ["likes", "comments", "shares", "saves", "views"]
    ):

        posts["engagement"] = (
            (
                posts["likes"]
                + posts["comments"]
                + posts["shares"]
                + posts["saves"]
            )
            / posts["views"].replace(0, pd.NA)
        ) * 100

        posts["engagement"] = (
            posts["engagement"]
            .fillna(0)
            .round(1)
        )

    else:

        posts["engagement"] = 0

    if not followers.empty:

        if "date" in followers.columns:

            followers["date"] = pd.to_datetime(
                followers["date"],
                errors="coerce"
            )

        for col in [
            "instagram_followers",
            "facebook_followers"
        ]:

            if col in followers.columns:

                followers[col] = pd.to_numeric(
                    followers[col],
                    errors="coerce"
                ).fillna(0)

        followers = followers.sort_values("date")

    return posts, followers

posts_df, followers_df = load_data()

# =========================
# HEADER
# =========================

col1, col2 = st.columns([5,1])

with col1:

    st.markdown(
        '<div class="vdk-main-title">Social Media</div>',
        unsafe_allow_html=True
    )

with col2:

    st.markdown(
        f'<div class="vdk-date">{datetime.now().strftime("%d %B %Y")}</div>',
        unsafe_allow_html=True
    )

st.markdown(
    '<div class="vdk-divider"></div>',
    unsafe_allow_html=True
)

# =========================
# KPI'S
# =========================

insta_current = 0
insta_previous = 0

facebook_current = 0
facebook_previous = 0

if len(followers_df) >= 2:

    insta_current = followers_df["instagram_followers"].iloc[-1]
    insta_previous = followers_df["instagram_followers"].iloc[-2]

    facebook_current = followers_df["facebook_followers"].iloc[-1]
    facebook_previous = followers_df["facebook_followers"].iloc[-2]

insta_growth = (
    ((insta_current - insta_previous) / insta_previous) * 100
    if insta_previous > 0 else 0
)

facebook_growth = (
    ((facebook_current - facebook_previous) / facebook_previous) * 100
    if facebook_previous > 0 else 0
)

avg_engagement = round(
    posts_df["engagement"].mean(),
    1
) if not posts_df.empty else 0

k1, k2, k3 = st.columns(3)

with k1:

    color = "#58a55c" if insta_growth >= 0 else "#d64545"
    arrow = "↑" if insta_growth >= 0 else "↓"

    st.markdown(f"""
    <div class="kpi-wrapper">
        <div class="kpi-label">Volgers Instagram</div>
        <div class="kpi-value">{int(insta_current):,}</div>
        <div class="kpi-growth" style="color:{color};">
            {arrow} {abs(insta_growth):.1f}%
        </div>
    </div>
    """.replace(",", "."), unsafe_allow_html=True)

with k2:

    color = "#58a55c" if facebook_growth >= 0 else "#d64545"
    arrow = "↑" if facebook_growth >= 0 else "↓"

    st.markdown(f"""
    <div class="kpi-wrapper">
        <div class="kpi-label">Volgers Facebook</div>
        <div class="kpi-value">{int(facebook_current):,}</div>
        <div class="kpi-growth" style="color:{color};">
            {arrow} {abs(facebook_growth):.1f}%
        </div>
    </div>
    """.replace(",", "."), unsafe_allow_html=True)

with k3:

    st.markdown(f"""
    <div class="kpi-wrapper">
        <div class="kpi-label">Gem. Engagement</div>
        <div class="kpi-value">{avg_engagement}%</div>
    </div>
    """, unsafe_allow_html=True)

# =========================
# CHART
# =========================

st.markdown('<div class="space"></div>', unsafe_allow_html=True)

if not posts_df.empty and "date" in posts_df.columns:

    trend = (
        posts_df
        .groupby(["date", "channel"])["views"]
        .sum()
        .reset_index()
    )

    fig = px.line(
        trend,
        x="date",
        y="views",
        color="channel",
        markers=True
    )

    fig.update_layout(
        height=420,
        paper_bgcolor="#ffffff",
        plot_bgcolor="#ffffff",
        xaxis_title="Datum",
        yaxis_title="Views"
    )

    st.plotly_chart(
        fig,
        use_container_width=True
    )

# =========================
# TABLE
# =========================

st.markdown('<div class="space"></div>', unsafe_allow_html=True)

cols = [
    "topic",
    "channel",
    "likes",
    "views",
    "comments",
    "shares",
    "saves",
    "engagement"
]

available_cols = [
    c for c in cols
    if c in posts_df.columns
]

if available_cols:

    st.dataframe(
        posts_df[available_cols],
        use_container_width=True,
        hide_index=True,
        height=500
    )
