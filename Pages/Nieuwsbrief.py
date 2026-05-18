import streamlit as st
import pandas as pd
import plotly.express as px

from datetime import datetime

# =====================================================
# PAGE CONFIG
# =====================================================

st.set_page_config(
    page_title="Nieuwsbrief Dashboard",
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
        "pages/Social_Media.py",
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

# =====================================================
# STYLING
# =====================================================

STYLE = """
<link rel="stylesheet" href="https://use.typekit.net/nap5xax.css">

<style>

html, body, [data-testid="stAppViewContainer"]{
    background:#f6f1e7;
    font-family:'sofia-pro', sans-serif;
}

.block-container{
    padding-top:30px;
    padding-left:55px;
    padding-right:55px;
    padding-bottom:40px;
    max-width:1700px;
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

/* HEADER */

.dashboard-title{
    font-size:58px;
    font-weight:700;
    color:#084422;
}

.dashboard-date{
    font-size:18px;
    color:#084422;
    font-weight:600;
}

/* KPI */

[data-testid="metric-container"]{
    background:#ffffff;
    border-radius:24px;
    padding:22px;
    box-shadow:0 8px 25px rgba(0,0,0,0.04);
    border:none;
}

[data-testid="metric-container"] label{
    color:#8a8a8a !important;
    font-size:14px !important;
}

[data-testid="metric-container"] [data-testid="stMetricValue"]{
    color:#084422;
    font-size:34px;
    font-weight:700;
}

/* GRAPH */

div[data-testid="stPlotlyChart"]{
    background:white;
    padding:15px;
    border-radius:24px;
    box-shadow:0 10px 25px rgba(8,68,34,0.05);
}

/* FILTER */

.stSelectbox label{
    display:none;
}

[data-baseweb="select"]{
    max-width:280px;
}

</style>
"""

st.markdown(STYLE, unsafe_allow_html=True)

# =====================================================
# DATA
# =====================================================

SHEET_ID = "1seQjiFaLzEm7PZ2vTDeylSZKEXGqDl6FHe2l1nVPnfg"

OPEN_SHEET_URL = (
    f"https://docs.google.com/spreadsheets/d/"
    f"{SHEET_ID}/export?format=csv&gid=0"
)

ALL_CAMPAIGNS_LABEL = "Alle campagnes"

NUMERIC_COLUMNS = [
    "sent",
    "opens",
    "clicks",
    "bounces",
    "unsubscribes",
]

# =====================================================
# LOAD DATA
# =====================================================

@st.cache_data(ttl=600)
def load_data() -> pd.DataFrame:

    try:

        df = pd.read_csv(
            OPEN_SHEET_URL
        )

    except Exception as exc:

        st.error(
            f"Kan data niet laden: {exc}"
        )

        return pd.DataFrame()

    # ===== CLEAN COLUMNS =====

    df.columns = (
        df.columns
        .str.strip()
        .str.lower()
        .str.replace(" ", "_", regex=False)
        .str.replace("-", "_", regex=False)
    )

    # ===== NUMERIC COLUMNS =====

    for col in NUMERIC_COLUMNS:

        if col in df.columns:

            df[col] = (
                df[col]
                .astype(str)
                .str.replace("\u00a0", "", regex=False)
                .str.replace(" ", "", regex=False)
                .str.replace(",", ".", regex=False)
                .str.replace("%", "", regex=False)
                .str.strip()
            )

            df[col] = pd.to_numeric(
                df[col],
                errors="coerce"
            ).fillna(0)

    # ===== DATE =====

    if "date" in df.columns:

        df["date"] = pd.to_datetime(
            df["date"],
            errors="coerce"
        )

    return df

# =====================================================
# HELPERS
# =====================================================

def format_number(value) -> str:

    if pd.isna(value):
        return "0"

    return f"{int(value):,}".replace(",", ".")


def format_rate(value) -> str:

    if value is None or pd.isna(value):
        return "0,0%"

    return f"{value:.1f}%".replace(".", ",")

# =====================================================
# HEADER
# =====================================================

col1, col2, col3 = st.columns([2, 2, 1])

with col1:

    st.markdown(
        '<div class="dashboard-title">Nieuwsbrief</div>',
        unsafe_allow_html=True
    )

with col3:

    st.markdown(
        f'<div class="dashboard-date">{datetime.now().strftime("%d %B %Y")}</div>',
        unsafe_allow_html=True
    )

# =====================================================
# LOAD DATAFRAME
# =====================================================

df = load_data()

if df.empty:

    st.error("Geen data gevonden.")

    st.stop()

# =====================================================
# FILTER
# =====================================================

campaigns = [ALL_CAMPAIGNS_LABEL]

if "campaign" in df.columns:

    campaign_order = (
        df.dropna(subset=["campaign"])
        .sort_values(
            "date",
            ascending=False
        )
        .drop_duplicates(
            subset=["campaign"]
        )
    )

    campaigns.extend(
        campaign_order["campaign"]
        .astype(str)
        .tolist()
    )

selected_campaign = st.selectbox(
    "Campagne",
    campaigns
)

if selected_campaign != ALL_CAMPAIGNS_LABEL:

    filtered_df = df[
        df["campaign"]
        == selected_campaign
    ]

else:

    filtered_df = df

if filtered_df.empty:

    st.warning(
        "Geen data beschikbaar voor de geselecteerde campagne."
    )

    st.stop()

# =====================================================
# KPI'S
# =====================================================

st.divider()

total_sent = int(
    filtered_df.get(
        "sent",
        pd.Series(0)
    ).sum()
)

total_opens = int(
    filtered_df.get(
        "opens",
        pd.Series(0)
    ).sum()
)

total_clicks = int(
    filtered_df.get(
        "clicks",
        pd.Series(0)
    ).sum()
)

total_bounces = int(
    filtered_df.get(
        "bounces",
        pd.Series(0)
    ).sum()
)

total_unsubs = int(
    filtered_df.get(
        "unsubscribes",
        pd.Series(0)
    ).sum()
)

open_rate = (
    round(
        (total_opens / total_sent) * 100,
        1
    )
    if total_sent else 0
)

click_rate = (
    round(
        (total_clicks / total_sent) * 100,
        1
    )
    if total_sent else 0
)

bounce_rate = (
    round(
        (total_bounces / total_sent) * 100,
        1
    )
    if total_sent else 0
)

click_to_open = (
    round(
        (total_clicks / total_opens) * 100,
        1
    )
    if total_opens else 0
)

col1, col2, col3, col4, col5, col6 = st.columns(6)

with col1:

    st.metric(
        "Verzonden mails",
        format_number(total_sent)
    )

with col2:

    st.metric(
        "Open rate",
        format_rate(open_rate),
        f"{format_number(total_opens)} geopend"
    )

with col3:

    st.metric(
        "Click rate",
        format_rate(click_rate),
        f"{format_number(total_clicks)} geklikt"
    )

with col4:

    st.metric(
        "Click-to-open",
        format_rate(click_to_open)
    )

with col5:

    st.metric(
        "Bounce rate",
        format_rate(bounce_rate),
        f"{format_number(total_bounces)} bounced"
    )

with col6:

    st.metric(
        "Uitschrijvingen",
        format_number(total_unsubs)
    )

# =====================================================
# CHART
# =====================================================

st.divider()

if len(filtered_df) > 1:

    st.subheader("Click rate trend")

    chart_data = (
        filtered_df
        .dropna(subset=["date"])
        .sort_values("date")
        .copy()
    )

    chart_data["click_rate"] = (
        chart_data["clicks"]
        .astype(float)
        .div(
            chart_data["sent"]
            .replace(0, pd.NA)
        )
        .fillna(0)
        * 100
    )

    fig = px.line(
        chart_data,
        x="date",
        y="click_rate",
        markers=True,
    )

    fig.update_traces(
        line=dict(
            color="#084422",
            width=4,
            shape="spline"
        )
    )

    fig.update_layout(
        height=350,
        showlegend=False,
        xaxis_title="Datum",
        yaxis_title="Click rate (%)",
        plot_bgcolor="white",
        paper_bgcolor="white",
    )

    fig.update_xaxes(
        showgrid=True,
        gridcolor="#ececf3"
    )

    fig.update_yaxes(
        showgrid=True,
        gridcolor="#ececf3"
    )

    st.plotly_chart(
        fig,
        use_container_width=True
    )
