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
# SIDEBAR
# =========================

with st.sidebar:

    st.markdown("""
    <div style="padding-bottom:25px;">
        <h1 style="
            color:white;
            font-size:28px;
            font-weight:800;
            margin:0;
        ">
            VDK Dashboard
        </h1>

        <p style="
            color:rgba(255,255,255,0.7);
            margin-top:8px;
            font-size:14px;
        ">
            Marketing & E-commerce
        </p>
    </div>
    """, unsafe_allow_html=True)

    st.page_link(
        "main.py",
        label="main",
        icon="🏠"
    )

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
        "pages/members.py",
        label="Members",
        icon="👥"
    )

# =========================
# GOOGLE SHEETS
# =========================

SHEET_ID = "1L-KVqx5Bg5Y18PiqncQLggX3oKpeMHtqmRnsmJ5Qziw"

INSTAGRAM_GID = "0"
FACEBOOK_GID = "847206611"
FOLLOWERS_GID = "730161295"

def get_sheet_url(gid: str) -> str:
    return (
        f"https://docs.google.com/spreadsheets/d/"
        f"{SHEET_ID}/export?format=csv&gid={gid}"
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

section[data-testid="stSidebar"]{
    background:#084422;
    border-right:none;
}

section[data-testid="stSidebar"] *{
    color:white !important;
}

#MainMenu,
footer,
header{
    visibility:hidden;
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
}

.space{
    height:50px;
}

</style>
"""

st.markdown(STYLE, unsafe_allow_html=True)

# =========================
# HELPERS
# =========================

NUMERIC_COLUMNS = [
    "likes",
    "views",
    "comments",
    "shares",
    "saves",
]

FOLLOWER_COLUMNS = [
    "instagram_followers",
    "facebook_followers",
]

def normalize_columns(df):

    df = df.copy()

    df.columns = (
        df.columns
        .str.strip()
        .str.lower()
        .str.replace(" ", "_")
        .str.replace("-", "_")
    )

    return df

def calculate_engagement_from_columns(df):

    if all(col in df.columns for col in [
        "likes",
        "comments",
        "shares",
        "saves",
        "views"
    ]):

        engagement = (
            (
                df["likes"]
                + df["comments"]
                + df["shares"]
                + df["saves"]
            )
            / df["views"].replace(0, pd.NA)
        ) * 100

        return (
            engagement
            .fillna(0)
            .replace([float("inf"), -float("inf")], 0)
            .round(1)
        )

    return pd.Series(0, index=df.index)

def fetch_sheet(sheet_gid):

    url = get_sheet_url(sheet_gid)

    headers = {
        "User-Agent": "Mozilla/5.0",
        "Accept": "text/csv, */*;q=0.1",
    }

    response = requests.get(
        url,
        headers=headers,
        timeout=20
    )

    response.raise_for_status()

    response.encoding = "utf-8"

    df = pd.read_csv(io.StringIO(response.text))

    return normalize_columns(df)

# =========================
# CLEAN POSTS
# =========================

def clean_posts_data(df):

    if df.empty:
        return df

    df = df.copy()

    for col in NUMERIC_COLUMNS:

        if col in df.columns:

            df[col] = (
                df[col]
                .astype(str)
                .str.replace(",", ".", regex=False)
                .str.replace("%", "", regex=False)
                .str.strip()
            )

            df[col] = pd.to_numeric(
                df[col],
                errors="coerce"
            ).fillna(0)

    if "date" in df.columns:

        df["date"] = pd.to_datetime(
            df["date"],
            format="%Y-%m-%d",
            errors="coerce"
        )

    df["engagement"] = calculate_engagement_from_columns(df)

    return df

# =========================
# CLEAN FOLLOWERS
# =========================

def clean_followers_data(df):

    if df.empty:
        return df

    df = df.copy()

    if "date" in df.columns:

        df["date"] = pd.to_datetime(
            df["date"],
            format="%Y-%m-%d",
            errors="coerce"
        )

    for col in FOLLOWER_COLUMNS:

        if col in df.columns:

            df[col] = pd.to_numeric(
                df[col],
                errors="coerce"
            ).fillna(0)

    df = (
        df
        .dropna(subset=["date"])
        .sort_values("date")
        .reset_index(drop=True)
    )

    return df

# =========================
# LOAD DATA
# =========================

@st.cache_data(ttl=0)
def load_data():

    instagram_df = fetch_sheet(INSTAGRAM_GID)
    instagram_df["channel"] = "Instagram"

    facebook_df = fetch_sheet(FACEBOOK_GID)
    facebook_df["channel"] = "Facebook"

    followers_df = fetch_sheet(FOLLOWERS_GID)

    combined_posts = pd.concat(
        [instagram_df, facebook_df],
        ignore_index=True
    )

    return (
        clean_posts_data(combined_posts),
        clean_followers_data(followers_df)
    )

posts_df, followers_df = load_data()

# =========================
# HEADER
# =========================

h1, h2, h3 = st.columns([2,2,1])

with h1:

    st.markdown(
        '<div class="vdk-main-title">Social Media</div>',
        unsafe_allow_html=True
    )

with h3:

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

k1, k2, k3 = st.columns(3)

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
)

with k1:

    insta_color = "#58a55c" if insta_growth >= 0 else "#d64545"
    insta_arrow = "↑" if insta_growth >= 0 else "↓"

    st.markdown(f"""
    <div class="kpi-wrapper">
        <div class="kpi-label">Volgers Instagram</div>
        <div class="kpi-value">{int(insta_current):,}</div>
        <div class="kpi-growth" style="color:{insta_color};">
            {insta_arrow} {abs(insta_growth):.1f}%
        </div>
    </div>
    """.replace(",", "."), unsafe_allow_html=True)

with k2:

    facebook_color = "#58a55c" if facebook_growth >= 0 else "#d64545"
    facebook_arrow = "↑" if facebook_growth >= 0 else "↓"

    st.markdown(f"""
    <div class="kpi-wrapper">
        <div class="kpi-label">Volgers Facebook</div>
        <div class="kpi-value">{int(facebook_current):,}</div>
        <div class="kpi-growth" style="color:{facebook_color};">
            {facebook_arrow} {abs(facebook_growth):.1f}%
        </div>
    </div>
    """.replace(",", "."), unsafe_allow_html=True)

with k3:

    st.markdown(f"""
    <div class="kpi-wrapper">
        <div class="kpi-label">Gem. Engagement</div>
        <div class="kpi-value">{str(avg_engagement).replace('.', ',')}%</div>
    </div>
    """, unsafe_allow_html=True)

st.markdown('<div class="space"></div>', unsafe_allow_html=True)

# =========================
# CHART
# =========================

trend = (
    posts_df.groupby(["date", "channel"])["views"]
    .sum()
    .reset_index()
)

fig = px.line(
    trend,
    x="date",
    y="views",
    color="channel",
    markers=True,
    title="Views trend"
)

fig.update_layout(
    height=420,
    paper_bgcolor="#ffffff",
    plot_bgcolor="#ffffff",
    border_radius=24
)

st.plotly_chart(fig, width="stretch")

st.markdown('<div class="space"></div>', unsafe_allow_html=True)

# =========================
# TABLE
# =========================

cols = [
    "topic",
    "likes",
    "views",
    "comments",
    "shares",
    "saves",
    "engagement"
]

st.dataframe(
    posts_df[[c for c in cols if c in posts_df.columns]],
    width="stretch",
    hide_index=True,
    height=450
)
