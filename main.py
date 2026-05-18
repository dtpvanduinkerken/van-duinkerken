import streamlit as st

# =========================================
# PAGINA INSTELLINGEN
# =========================================

st.set_page_config(
    page_title="VDK Marketing Dashboard",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded"
)

# =========================================
# STYLING
# =========================================

st.markdown("""
<link rel="stylesheet" href="https://use.typekit.net/nap5xax.css">

<style>

html, body, [class*="css"]{
    font-family:'sofia-pro', Arial, sans-serif;
}

/* Achtergrond */
.stApp{
    background:#f9f3e9;
}

/* Sidebar */
section[data-testid="stSidebar"]{
    background:#084422;
    border-right:none;
}

section[data-testid="stSidebar"] *{
    color:white !important;
}

/* Cards */
.vdk-card{
    background:white;
    border-radius:24px;
    padding:30px;
    box-shadow:0 10px 25px rgba(8,68,34,0.08);
}

/* KPI cards */
.kpi-card{
    background:white;
    border-radius:22px;
    padding:28px;
    box-shadow:0 10px 25px rgba(8,68,34,0.08);
}

.kpi-title{
    font-size:14px;
    color:#6b7280;
    margin-bottom:8px;
}

.kpi-value{
    font-size:42px;
    font-weight:800;
    color:#084422;
    line-height:1;
}

.kpi-growth{
    font-size:15px;
    font-weight:700;
    margin-top:10px;
}

/* Titels */
h1, h2, h3{
    color:#084422;
}

/* Streamlit menu verbergen */
#MainMenu {visibility:hidden;}
footer {visibility:hidden;}
header {visibility:hidden;}

</style>
""", unsafe_allow_html=True)

# =========================================
# SIDEBAR
# =========================================

with st.sidebar:

    st.markdown(
        """
        <div style="padding-top:10px; padding-bottom:25px;">
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
        """,
        unsafe_allow_html=True
    )

    st.page_link(
        "Home.py",
        label="Home",
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

    st.page_link(
        "pages/Webshop.py",
        label="Webshop",
        icon="🛒"
    )

# =========================================
# HEADER
# =========================================

st.markdown("""
<div style="
    background:white;
    padding:35px;
    border-radius:24px;
    box-shadow:0 10px 25px rgba(8,68,34,0.08);
    margin-bottom:25px;
">
    <div style="
        font-size:14px;
        font-weight:700;
        color:#8cbe26;
        letter-spacing:1px;
        margin-bottom:10px;
    ">
        VAN DUINKERKEN
    </div>

    <h1 style="
        margin:0;
        font-size:42px;
        font-weight:800;
        color:#084422;
    ">
        Marketing Dashboard
    </h1>

    <p style="
        margin-top:15px;
        font-size:17px;
        line-height:1.7;
        color:#4b5563;
        max-width:850px;
    ">
        Overzicht van marketing, social media, members, nieuwsbrieven
        en webshop prestaties binnen Van Duinkerken.
    </p>
</div>
""", unsafe_allow_html=True)

# =========================================
# KPI ROW
# =========================================

col1, col2, col3, col4 = st.columns(4)

with col1:
    st.markdown("""
    <div class="kpi-card">
        <div class="kpi-title">Instagram volgers</div>
        <div class="kpi-value">1.624</div>
        <div class="kpi-growth" style="color:#16a34a;">
            ▲ +0,5%
        </div>
    </div>
    """, unsafe_allow_html=True)

with col2:
    st.markdown("""
    <div class="kpi-card">
        <div class="kpi-title">Facebook volgers</div>
        <div class="kpi-value">3.532</div>
        <div class="kpi-growth" style="color:#16a34a;">
            ▲ +0,2%
        </div>
    </div>
    """, unsafe_allow_html=True)

with col3:
    st.markdown("""
    <div class="kpi-card">
        <div class="kpi-title">Nieuwe members</div>
        <div class="kpi-value">128</div>
        <div class="kpi-growth" style="color:#16a34a;">
            ▲ +12%
        </div>
    </div>
    """, unsafe_allow_html=True)

with col4:
    st.markdown("""
    <div class="kpi-card">
        <div class="kpi-title">Nieuwsbrief openrate</div>
        <div class="kpi-value">61%</div>
        <div class="kpi-growth" style="color:#dc2626;">
            ▼ -2%
        </div>
    </div>
    """, unsafe_allow_html=True)

# =========================================
# CONTENT BLOKKEN
# =========================================

col1, col2 = st.columns([2,1])

with col1:

    st.markdown("""
    <div class="vdk-card">

    <h2 style="
        margin-top:0;
        margin-bottom:20px;
        font-size:28px;
        font-weight:800;
    ">
        Marketing overzicht
    </h2>

    <p style="
        font-size:16px;
        line-height:1.8;
        color:#4b5563;
    ">
        Gebruik dit dashboard om inzicht te krijgen in de prestaties van
        social media, nieuwsbrieven, membergroei en webshopactiviteiten.
    </p>

    </div>
    """, unsafe_allow_html=True)

with col2:

    st.markdown("""
    <div class="vdk-card">

    <h3 style="
        margin-top:0;
        margin-bottom:18px;
        font-size:24px;
        font-weight:800;
    ">
        Snelle acties
    </h3>

    <div style="
        display:flex;
        flex-direction:column;
        gap:12px;
    ">

        <div style="
            background:#f9f3e9;
            padding:16px;
            border-radius:14px;
            font-weight:700;
            color:#084422;
        ">
            📧 Nieuwsbrief controleren
        </div>

        <div style="
            background:#f9f3e9;
            padding:16px;
            border-radius:14px;
            font-weight:700;
            color:#084422;
        ">
            📱 Social media bekijken
        </div>

        <div style="
            background:#f9f3e9;
            padding:16px;
            border-radius:14px;
            font-weight:700;
            color:#084422;
        ">
            👥 Members analyseren
        </div>

    </div>

    </div>
    """, unsafe_allow_html=True)
