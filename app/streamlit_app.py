import streamlit as st
import requests
import time

# ── page config ────────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="Tunisia Real Estate Predictor",
    page_icon="🏠",
    layout="centered",
    initial_sidebar_state="collapsed",
)

API_URL = "http://127.0.0.1:8000"

# ── dark mode state ────────────────────────────────────────────────────────────
if "dark" not in st.session_state:
    st.session_state.dark = False

if st.session_state.dark:
    BG             = "#0f1117"
    CARD_BG        = "#1a1d27"
    CARD_SHADOW    = "0 1px 3px rgba(0,0,0,.4), 0 4px 16px rgba(0,0,0,.3)"
    TEXT_H         = "#f0f2f8"
    TEXT_BODY      = "#9ca3af"
    TEXT_LABEL     = "#6b7280"
    BORDER         = "#2d2f3e"
    RADIO_BG       = "#252838"
    RADIO_TEXT     = "#e5e7eb"
    TAG_BG         = "#162032"
    TAG_COLOR      = "#38bdf8"
    COMPARE_SRC    = "#d1d5db"
    COMPARE_PRC    = "#38bdf8"
    COMPARE_BAR_BG = "#2d2f3e"
    WIDGET_TEXT    = "#e5e7eb"
    MODE_ICON      = "☀️"
    MODE_LABEL     = "Light mode"
else:
    BG             = "#f7f8fa"
    CARD_BG        = "#ffffff"
    CARD_SHADOW    = "0 1px 3px rgba(0,0,0,.06), 0 4px 16px rgba(0,0,0,.04)"
    TEXT_H         = "#0d1117"
    TEXT_BODY      = "#6b7280"
    TEXT_LABEL     = "#9ca3af"
    BORDER         = "#f3f4f6"
    RADIO_BG       = "#f1f5f9"
    RADIO_TEXT     = "#374151"
    TAG_BG         = "#e8f4f8"
    TAG_COLOR      = "#0077b6"
    COMPARE_SRC    = "#374151"
    COMPARE_PRC    = "#0077b6"
    COMPARE_BAR_BG = "#e5e7eb"
    WIDGET_TEXT    = "#374151"
    MODE_ICON      = "🌙"
    MODE_LABEL     = "Dark mode"

# ── custom CSS ─────────────────────────────────────────────────────────────────
st.markdown(f"""
<style>
    /* ── google font ── */
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap');

    html, body, [class*="css"] {{
        font-family: 'Inter', sans-serif;
    }}

    /* ── page background ── */
    .stApp {{
        background-color: {BG} !important;
    }}

    /* ── hide default header/footer ── */
    #MainMenu, footer, header {{ visibility: hidden; }}

    /* ── hero section ── */
    .hero {{
        text-align: center;
        padding: 1rem 1rem 1.5rem;
    }}
    .hero-tag {{
        display: inline-block;
        background: {TAG_BG};
        color: {TAG_COLOR};
        font-size: 0.75rem;
        font-weight: 600;
        letter-spacing: 0.12em;
        text-transform: uppercase;
        padding: 0.35rem 0.9rem;
        border-radius: 99px;
        margin-bottom: 1rem;
    }}
    .hero h1 {{
        font-size: 2.1rem;
        font-weight: 700;
        color: {TEXT_H};
        margin: 0 0 0.5rem;
        line-height: 1.2;
    }}
    .hero p {{
        color: {TEXT_BODY};
        font-size: 1rem;
        margin: 0;
    }}

    /* ── input card ── */
    .card {{
        background: {CARD_BG};
        border-radius: 16px;
        padding: 2rem;
        box-shadow: {CARD_SHADOW};
        margin-bottom: 1.5rem;
    }}
    .card-title {{
        font-size: 0.7rem;
        font-weight: 600;
        letter-spacing: 0.1em;
        text-transform: uppercase;
        color: {TEXT_LABEL};
        margin-bottom: 1.2rem;
    }}

    /* ── result card ── */
    .result-card {{
        background: linear-gradient(135deg, #0077b6 0%, #023e8a 100%);
        border-radius: 16px;
        padding: 2.2rem;
        box-shadow: 0 8px 32px rgba(0, 119, 182, .28);
        margin-bottom: 1.5rem;
        color: #fff;
        text-align: center;
    }}
    .result-label {{
        font-size: 0.72rem;
        font-weight: 600;
        letter-spacing: 0.12em;
        text-transform: uppercase;
        opacity: 0.75;
        margin-bottom: 0.6rem;
    }}
    .result-price {{
        font-size: 3rem;
        font-weight: 700;
        letter-spacing: -0.02em;
        margin-bottom: 0.2rem;
    }}
    .result-currency {{
        font-size: 1.1rem;
        font-weight: 400;
        opacity: 0.8;
    }}
    .result-range {{
        font-size: 0.85rem;
        opacity: 0.7;
        margin-top: 0.8rem;
    }}

    /* ── metric pills ── */
    .metrics-row {{
        display: flex;
        gap: 1rem;
        margin-top: 1rem;
    }}
    .metric-pill {{
        flex: 1;
        background: rgba(255,255,255,0.12);
        border-radius: 10px;
        padding: 0.8rem 1rem;
        text-align: center;
    }}
    .metric-pill .mp-label {{
        font-size: 0.68rem;
        text-transform: uppercase;
        letter-spacing: 0.08em;
        opacity: 0.7;
        margin-bottom: 0.3rem;
    }}
    .metric-pill .mp-value {{
        font-size: 1.15rem;
        font-weight: 600;
    }}

    /* ── compare card ── */
    .compare-card {{
        background: {CARD_BG};
        border-radius: 16px;
        padding: 1.6rem 2rem;
        box-shadow: {CARD_SHADOW};
        margin-bottom: 1.5rem;
    }}
    .compare-row {{
        display: flex;
        justify-content: space-between;
        align-items: center;
        padding: 0.7rem 0;
        border-bottom: 1px solid {BORDER};
    }}
    .compare-row:last-child {{ border: none; }}
    .compare-src {{
        font-size: 0.875rem;
        font-weight: 500;
        color: {COMPARE_SRC};
    }}
    .compare-price {{
        font-size: 1rem;
        font-weight: 700;
        color: {COMPARE_PRC};
    }}
    .compare-bar-wrap {{
        width: 110px;
        height: 6px;
        background: {COMPARE_BAR_BG};
        border-radius: 99px;
        overflow: hidden;
        margin-left: 1rem;
    }}
    .compare-bar {{
        height: 100%;
        background: linear-gradient(90deg, #0077b6, #00b4d8);
        border-radius: 99px;
    }}

    /* ── footer ── */
    .app-footer {{
        text-align: center;
        color: {TEXT_LABEL};
        font-size: 0.78rem;
        padding: 1.5rem 0 2rem;
    }}

    /* ── streamlit widget overrides ── */
    div[data-testid="stSlider"] > label,
    div[data-testid="stSelectbox"] > label,
    div[data-testid="stSelectbox"] * {{
        color: {WIDGET_TEXT} !important;
    }}
    div[data-baseweb="select"] > div,
    div[data-baseweb="input"] > div {{
        background-color: {CARD_BG} !important;
        border-color: {BORDER} !important;
    }}

    /* ── radio buttons ── */
    div[data-testid="stRadio"] > label {{
        font-size: 0.82rem !important;
        font-weight: 500 !important;
        color: {RADIO_TEXT} !important;
    }}
    div[data-testid="stRadio"] div[role="radiogroup"] {{
        background: {RADIO_BG};
        border-radius: 10px;
        padding: 4px;
        display: flex;
        gap: 4px;
    }}
    div[data-testid="stRadio"] label,
    div[data-testid="stRadio"] label span,
    div[data-testid="stRadio"] div[data-testid="stMarkdownContainer"] p {{
        color: {RADIO_TEXT} !important;
        font-size: 0.875rem !important;
        font-weight: 500 !important;
    }}

    /* ── dark mode toggle ── */
    .toggle-btn button {{
        background: {CARD_BG} !important;
        color: {TEXT_H} !important;
        border: 1px solid {BORDER} !important;
        border-radius: 99px !important;
        padding: 0.35rem 0.85rem !important;
        font-size: 1rem !important;
        font-weight: 500 !important;
        width: auto !important;
        margin-top: 0 !important;
        box-shadow: {CARD_SHADOW} !important;
        transition: opacity 0.2s !important;
    }}
    .toggle-btn button:hover {{ opacity: 0.72 !important; }}

    /* ── estimate button ── */
    .stButton > button {{
        width: 100%;
        background: linear-gradient(135deg, #0077b6 0%, #023e8a 100%);
        color: white;
        border: none;
        border-radius: 10px;
        padding: 0.75rem 1rem;
        font-size: 0.95rem;
        font-weight: 600;
        letter-spacing: 0.02em;
        cursor: pointer;
        transition: opacity 0.2s;
        margin-top: 0.5rem;
    }}
    .stButton > button:hover {{ opacity: 0.88; }}
</style>
""", unsafe_allow_html=True)


# ── helpers ───────────────────────────────────────────────────────────────────
@st.cache_data(ttl=300)
def fetch_locations():
    try:
        r = requests.get(f"{API_URL}/locations", timeout=4)
        return r.json()["locations"]
    except Exception:
        return [
            "Ariana", "Autre", "Ben Arous", "Bizerte", "Bizerte Nord",
            "Boumhel Bassatine", "Carthage", "Cité El Khadra", "El Menzah",
            "Hammam El Ghezaz", "Hammamet", "Kairouan Ville", "Kélibia",
            "La Goulette", "La Manouba", "La Marsa", "La Soukra", "Le Kram",
            "Mahdia", "Monastir Ville", "Méégrine", "Nabeul", "Rades",
            "Raoued", "Sfax Ville", "Sousse", "Sousse Riadh", "Tantana",
            "Tunis",
        ]


def call_predict(superficie, chambres, salles_de_bains, location, source):
    payload = {
        "superficie": superficie,
        "chambres": chambres,
        "salles_de_bains": salles_de_bains,
        "location": location,
        "source": source,
    }
    r = requests.post(f"{API_URL}/predict", json=payload, timeout=6)
    r.raise_for_status()
    return r.json()


def fmt(n):
    return f"{n:,.0f}"


# ── dark mode toggle (top-right) ───────────────────────────────────────────────
_, toggle_col = st.columns([7, 1])
with toggle_col:
    st.markdown('<div class="toggle-btn">', unsafe_allow_html=True)
    if st.button(MODE_ICON, help=MODE_LABEL, key="dark_toggle"):
        st.session_state.dark = not st.session_state.dark
        st.rerun()
    st.markdown('</div>', unsafe_allow_html=True)


# ── hero ──────────────────────────────────────────────────────────────────────
st.markdown(f"""
<div class="hero">
    <div class="hero-tag">🇹🇳 Tunisia Real Estate</div>
    <h1>How much is your property worth?</h1>
    <p>Instant ML-powered price estimates based on thousands of real listings.</p>
</div>
""", unsafe_allow_html=True)

# ── input card ────────────────────────────────────────────────────────────────
locations = fetch_locations()

st.markdown('<div class="card"><div class="card-title">Property Details</div>', unsafe_allow_html=True)

col1, col2 = st.columns(2)
with col1:
    superficie = st.slider("Superficie (m²)", min_value=20, max_value=600,
                           value=120, step=5)
    chambres = st.slider("Bedrooms", min_value=0, max_value=10, value=2)
with col2:
    location = st.selectbox("Location", options=locations,
                            index=locations.index("Tunis") if "Tunis" in locations else 0)
    salles_de_bains = st.slider("Bathrooms", min_value=0, max_value=8, value=1)

source = st.radio(
    "Listing platform",
    options=["tayara", "mubawab"],
    horizontal=True,
    help="The data source affects price calibration.",
)

predict_btn = st.button("✦  Estimate Price")
st.markdown('</div>', unsafe_allow_html=True)

# ── prediction ────────────────────────────────────────────────────────────────
if predict_btn:
    with st.spinner(""):
        time.sleep(0.3)
        try:
            res = call_predict(superficie, chambres, salles_de_bains, location, source)
        except Exception as e:
            st.error(f"API error: {e}")
            st.stop()

    p = res["predicted_price"]
    lo = res["price_low"]
    hi = res["price_high"]
    ppsqm = res["price_per_sqm"]

    st.markdown(f"""
    <div class="result-card">
        <div class="result-label">Estimated Market Price</div>
        <div class="result-price">{fmt(p)} <span class="result-currency">DT</span></div>
        <div class="metrics-row">
            <div class="metric-pill">
                <div class="mp-label">Low estimate</div>
                <div class="mp-value">{fmt(lo)} DT</div>
            </div>
            <div class="metric-pill">
                <div class="mp-label">High estimate</div>
                <div class="mp-value">{fmt(hi)} DT</div>
            </div>
            <div class="metric-pill">
                <div class="mp-label">Price / m²</div>
                <div class="mp-value">{fmt(ppsqm)} DT</div>
            </div>
        </div>
        <div class="result-range">Range based on ±25 % model confidence band</div>
    </div>
    """, unsafe_allow_html=True)

    # ── source comparison ───────────────────────────────────────────────────
    other_src = "mubawab" if source == "tayara" else "tayara"
    try:
        res2 = call_predict(superficie, chambres, salles_de_bains, location, other_src)
        p2 = res2["predicted_price"]
        max_p = max(p, p2)
        w1 = round(p / max_p * 100)
        w2 = round(p2 / max_p * 100)
        st.markdown(f"""
        <div class="compare-card">
            <div class="card-title">Platform Comparison</div>
            <div class="compare-row">
                <span class="compare-src">{source.capitalize()}</span>
                <span class="compare-price">{fmt(p)} DT</span>
                <div class="compare-bar-wrap">
                    <div class="compare-bar" style="width:{w1}%"></div>
                </div>
            </div>
            <div class="compare-row">
                <span class="compare-src">{other_src.capitalize()}</span>
                <span class="compare-price">{fmt(p2)} DT</span>
                <div class="compare-bar-wrap">
                    <div class="compare-bar" style="width:{w2}%"></div>
                </div>
            </div>
        </div>
        """, unsafe_allow_html=True)
    except Exception:
        pass

# ── footer ────────────────────────────────────────────────────────────────────
st.markdown(f"""
<div class="app-footer">
    Trained on Tayara &amp; Mubawab listings &middot; XGBoost / Random Forest ensemble
</div>
""", unsafe_allow_html=True)
