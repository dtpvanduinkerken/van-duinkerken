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
    page_title="Members",
    layout="wide",
    initial_sidebar_state="expanded"
)

# =====================================================
# SIDEBAR
# =====================================================

with st.sidebar:

    st.markdown("## Dashboard")

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

# =====================================================
# STYLING
# =====================================================

STYLE = """
<link rel="stylesheet" href="https://use.typekit.net/nap5xax.css">

<style>

html, body, [data-testid="stAppViewContainer"]{
    background:#f4efe6;
    font-family:'sofia-pro', sans-serif;
}

.block-container{
    padding-top:35px;
    padding-left:40px;
    padding-right:40px;
    padding-bottom:40px;
    max-width:100%;
}

/* SIDEBAR */

section[data-testid="stSidebar"]{
    background:#084422;
    border-right:none;
}

section[data-testid="stSidebar"] *{
    color:white !important;
}

/* MENU */

#MainMenu,
footer{
    visibility:hidden;
}

/* TITLES */

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

/* KPI */

[data-testid="stMetric"]{
    background:#ffffff;
    border-radius:24px;
    padding:20px;
    box-shadow:0 10px 25px rgba(8,68,34,0.05);
}

/* GRAPH */

div[data-testid="stPlotlyChart"]{
    background:white;
    padding:15px;
    border-radius:24px;
    box-shadow:0 10px 25px rgba(8,68,34,0.05);
}

/* TABLE */

[data-testid="stDataFrame"]{
    border-radius:24px !important;
    overflow:hidden;
}

</style>
"""

st.markdown(STYLE, unsafe_allow_html=True)

# =====================================================
# CONFIG
# =====================================================

MONTH_MAP = {
    1: "Jan",
    2: "Feb",
    3: "Mrt",
    4: "Apr",
    5: "Mei",
    6: "Jun",
    7: "Jul",
    8: "Aug",
    9: "Sep",
    10: "Okt",
    11: "Nov",
    12: "Dec"
}

MONTH_ORDER = [
    "Jan",
    "Feb",
    "Mrt",
    "Apr",
    "Mei",
    "Jun",
    "Jul",
    "Aug",
    "Sep",
    "Okt",
    "Nov",
    "Dec"
]

SHEET_ID = "1snBY34YPGix5KpgOQ45aq4obQpmHirEt9Pg9I8DrE_0"

MEMBER_URL = (
    f"https://docs.google.com/spreadsheets/d/"
    f"{SHEET_ID}/gviz/tq?tqx=out:csv&sheet=Sheet1"
)

DEALS_URL = (
    f"https://docs.google.com/spreadsheets/d/"
    f"{SHEET_ID}/gviz/tq?tqx=out:csv&sheet=MemberDeal"
)

# =====================================================
# HELPERS
# =====================================================

def normalize_columns(df: pd.DataFrame) -> pd.DataFrame:

    if df.empty:
        return df

    df.columns = (
        df.columns
        .str.strip()
        .str.lower()
        .str.replace(" ", "_", regex=False)
        .str.replace("/", "_", regex=False)
    )

    return df


def fetch_sheet(url: str) -> pd.DataFrame:

    try:

        headers = {
            "User-Agent": "Mozilla/5.0",
            "Accept": "text/csv, */*;q=0.1",
        }

        response = requests.get(
            url,
            headers=headers,
            timeout=15
        )

        response.raise_for_status()

        df = pd.read_csv(
            io.StringIO(response.text)
        )

        return normalize_columns(df)

    except Exception as e:

        st.error(f"❌ Kan data niet laden: {e}")

        return pd.DataFrame()


@st.cache_data(ttl=3600)
def load_members():

    return fetch_sheet(MEMBER_URL)


@st.cache_data(ttl=3600)
def load_deals():

    return fetch_sheet(DEALS_URL)

# =====================================================
# LOAD DATA
# =====================================================

members = load_members()
deals = load_deals()

if members.empty:

    st.error("❌ Geen members data beschikbaar")

    st.stop()

members = members.dropna(
    subset=["member_id", "created_at"]
)

if members.empty:

    st.error("❌ Geen geldige members data")

    st.stop()

# =====================================================
# PROCESS MEMBERS
# =====================================================

members["week_label"] = members["created_at"].astype(str)

members["year"] = (
    members["week_label"]
    .str.extract(r'(\d{4})')[0]
    .astype(int)
)

members["week"] = (
    members["week_label"]
    .str.extract(r'week (\d+)')[0]
    .astype(int)
)

weekly = (
    members
    .groupby(["year", "week", "week_label"])
    .size()
    .reset_index(name="Nieuwe members")
)

weekly = weekly.sort_values(
    ["year", "week"]
)

weekly["Groei"] = (
    weekly["Nieuwe members"]
    .diff()
    .fillna(0)
)

weekly["Trend"] = (
    weekly["Nieuwe members"]
    .rolling(3)
    .mean()
)

weekly["Totaal"] = (
    weekly["Nieuwe members"]
    .cumsum()
)

# =====================================================
# KPI
# =====================================================

if len(weekly) >= 2:

    vorige_week = int(
        weekly.iloc[-2]["Nieuwe members"]
    )

    huidige_week = int(
        weekly.iloc[-1]["Nieuwe members"]
    )

    groei_percentage = (
        ((huidige_week - vorige_week) / vorige_week) * 100
        if vorige_week > 0 else 0
    )

else:

    huidige_week = 0
    groei_percentage = 0

# =====================================================
# HEADER
# =====================================================

col1, col2, col3 = st.columns([2, 2, 1])

with col1:

    st.markdown(
        '<div class="vdk-main-title">Members</div>',
        unsafe_allow_html=True
    )

with col3:

    st.markdown(
        f'<div class="vdk-date">{datetime.now().strftime("%d %B %Y")}</div>',
        unsafe_allow_html=True
    )

st.markdown(
    '<div class="vdk-divider"></div>',
    unsafe_allow_html=True
)

# =====================================================
# KPI ROW
# =====================================================

total_members = int(
    weekly["Nieuwe members"].sum()
)

latest_growth = int(
    weekly["Groei"].iloc[-1]
) if len(weekly) > 0 else 0

total_cumulative = int(
    weekly["Totaal"].iloc[-1]
) if len(weekly) > 0 else 0

col1, col2, col3 = st.columns(3)

with col1:

    st.metric(
        "Nieuwe members totaal",
        f"{total_members:,}"
    )

with col2:

    st.metric(
        "Nieuwe members laatste week",
        f"{huidige_week:,}",
        delta=f"{groei_percentage:.1f}%"
    )

with col3:

    st.metric(
        "Totaal cumulatief",
        f"{total_cumulative:,}"
    )

st.divider()

# =====================================================
# MEMBERS CHARTS
# =====================================================

col1, col2 = st.columns(2)

with col1:

    st.subheader(
        "Inkomende leden en weektrend"
    )

    fig = px.line(
        weekly,
        x="week_label",
        y=["Nieuwe members", "Trend"],
        markers=True,
    )

    fig.update_layout(
        height=400,
        showlegend=True,
        xaxis_title="Week",
        yaxis_title="Aantal members",
        paper_bgcolor="#ffffff",
        plot_bgcolor="#ffffff"
    )

    st.plotly_chart(
        fig,
        use_container_width=True
    )

with col2:

    st.subheader(
        "Wekelijkse groei"
    )

    growth_df = weekly.copy()

    growth_df["kleur"] = growth_df["Groei"].apply(
        lambda x: "Groei" if x >= 0 else "Daling"
    )

    fig = px.bar(
        growth_df,
        x="week_label",
        y="Groei",
        color="kleur",
        color_discrete_map={
            "Groei": "#8cbe26",
            "Daling": "#c0392b"
        }
    )

    fig.add_hline(
        y=0,
        line_dash="dash",
        line_color="#084422"
    )

    fig.update_layout(
        height=400,
        showlegend=False,
        xaxis_title="Week",
        yaxis_title="Groei",
        paper_bgcolor="#ffffff",
        plot_bgcolor="#ffffff"
    )

    st.plotly_chart(
        fig,
        use_container_width=True
    )

st.divider()

# =====================================================
# DEALS
# =====================================================

if not deals.empty:

    deals["datum"] = pd.to_datetime(
        deals["datum"],
        errors="coerce"
    )

    deals["omzet"] = pd.to_numeric(
        deals["omzet"]
        .astype(str)
        .str.replace(",", "."),
        errors="coerce"
    ).fillna(0)

    deals["maand"] = (
        deals["datum"]
        .dt.month
        .map(MONTH_MAP)
    )

    deals["maand_nummer"] = (
        deals["datum"]
        .dt.month
    )

    if (
        "member_deal" in deals.columns
        and "omzet" in deals.columns
    ):

        total_per_deal = (
            deals
            .groupby("member_deal")["omzet"]
            .agg(["sum", "count", "mean"])
            .reset_index()
            .rename(columns={
                "sum": "totale_omzet",
                "count": "aantal_transacties",
                "mean": "gemiddelde_omzet"
            })
            .sort_values(
                "totale_omzet",
                ascending=False
            )
        )

        total_per_deal = total_per_deal[
            total_per_deal["totale_omzet"] > 0
        ]

        if not total_per_deal.empty:

            st.subheader(
                "Omzet per member deal"
            )

            fig = px.bar(
                total_per_deal,
                x="member_deal",
                y="totale_omzet",
                text_auto=".2s",
                color="totale_omzet",
                color_continuous_scale="Greens",
            )

            fig.update_layout(
                height=400,
                xaxis_title="Member deal",
                yaxis_title="Totale omzet (€)",
                showlegend=False,
                paper_bgcolor="#ffffff",
                plot_bgcolor="#ffffff"
            )

            st.plotly_chart(
                fig,
                use_container_width=True
            )

            st.subheader(
                "Performance per member deal"
            )

            display_df = total_per_deal.copy()

            display_df["totale_omzet"] = (
                display_df["totale_omzet"]
                .apply(lambda x: f"€{x:,.0f}")
            )

            display_df["gemiddelde_omzet"] = (
                display_df["gemiddelde_omzet"]
                .apply(lambda x: f"€{x:,.0f}")
            )

            display_df = display_df.rename(columns={
                "member_deal": "Member Deal",
                "totale_omzet": "Totale Omzet",
                "aantal_transacties": "Aantal Transacties",
                "gemiddelde_omzet": "Gemiddelde per Transactie"
            })

            st.dataframe(
                display_df,
                use_container_width=True,
                hide_index=True
            )

else:

    st.info(
        "ℹ️ Geen deals data beschikbaar"
    )
