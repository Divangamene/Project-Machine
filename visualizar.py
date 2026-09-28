```python
from pathlib import Path

import joblib
import pandas as pd
import streamlit as st


# ============================================================
# CONFIGURAÇÃO DOS CAMINHOS
# ============================================================

BASE_DIR = Path(__file__).resolve().parent

DATASET_PATH = BASE_DIR / "data" / "dataset_carro.csv"
MODEL_PATH = BASE_DIR / "modelo.pkl"


# ============================================================
# CONFIGURAÇÃO DA PÁGINA
# ============================================================

st.set_page_config(
    page_title="Machine Condition Assessment",
    page_icon=None,
    layout="wide",
    initial_sidebar_state="collapsed"
)


# ============================================================
# CSS
# ============================================================

st.markdown(
    """
    <style>

    #MainMenu {
        visibility: hidden;
    }

    header {
        visibility: hidden;
    }

    footer {
        visibility: hidden;
    }

    .stApp {
        background-color: #F7F8FA;
        color: #172033;
    }

    .block-container {
        max-width: 1180px;
        padding-top: 2.5rem;
        padding-bottom: 3rem;
    }

    html, body, [class*="css"] {
        font-family:
            Inter,
            -apple-system,
            BlinkMacSystemFont,
            "Segoe UI",
            sans-serif;
    }

    /* --------------------------------------------------------
       TOP BAR
       -------------------------------------------------------- */

    .topbar {
        display: flex;
        justify-content: space-between;
        align-items: center;

        padding-bottom: 1.4rem;
        margin-bottom: 2.2rem;

        border-bottom: 1px solid #E4E7EC;
    }

    .brand {
        color: #172033;

        font-size: 0.78rem;
        font-weight: 700;

        text-transform: uppercase;
        letter-spacing: 0.13em;
    }

    .system-status {
        display: flex;
        align-items: center;
        gap: 8px;

        color: #667085;

        font-size: 0.72rem;
        font-weight: 600;

        text-transform: uppercase;
        letter-spacing: 0.06em;
    }

    .status-dot {
        width: 7px;
        height: 7px;

        border-radius: 50%;

        background-color: #12B76A;
    }

    /* --------------------------------------------------------
       HERO
       -------------------------------------------------------- */

    .hero {
        margin-bottom: 2.5rem;
    }

    .hero-label {
        margin-bottom: 0.65rem;

        color: #667085;

        font-size: 0.7rem;
        font-weight: 700;

        text-transform: uppercase;
        letter-spacing: 0.12em;
    }

    .hero-title {
        margin: 0;

        color: #101828;

        font-size: 2.5rem;
        line-height: 1.1;
        font-weight: 650;

        letter-spacing: -0.035em;
    }

    .hero-description {
        max-width: 700px;

        margin-top: 0.85rem;

        color: #667085;

        font-size: 0.98rem;
        line-height: 1.65;
    }

    /* --------------------------------------------------------
       SECTION
       -------------------------------------------------------- */

    .section-title {
        margin-bottom: 1rem;

        color: #475467;

        font-size: 0.72rem;
        font-weight: 700;

        text-transform: uppercase;
        letter-spacing: 0.1em;
    }

    /* --------------------------------------------------------
       CARDS
       -------------------------------------------------------- */

    .card {
        padding: 1.5rem;

        margin-bottom: 1rem;

        background: #FFFFFF;

        border: 1px solid #E4E7EC;
        border-radius: 12px;
    }

    .card-title {
        margin-bottom: 0.3rem;

        color: #101828;

        font-size: 1rem;
        font-weight: 650;
    }

    .card-description {
        margin-bottom: 1.25rem;

        color: #667085;

        font-size: 0.82rem;
        line-height: 1.5;
    }

    /* --------------------------------------------------------
       RESULT
       -------------------------------------------------------- */

    .assessment {
        padding: 1.8rem;

        margin-top: 1.5rem;

        background: #FFFFFF;

        border: 1px solid #D0D5DD;
        border-radius: 14px;
    }

    .assessment-label {
        color: #667085;

        font-size: 0.7rem;
        font-weight: 700;

        text-transform: uppercase;
        letter-spacing: 0.1em;
    }

    .assessment-status {
        margin-top: 0.45rem;

        font-size: 2rem;
        font-weight: 700;
        letter-spacing: -0.025em;
    }

    .assessment-description {
        color: #667085;

        font-size: 0.88rem;
        line-height: 1.5;
    }

    .normal {
        color: #087443;
    }

    .warning {
        color: #B54708;
    }

    .critical {
        color: #B42318;
    }

    /* --------------------------------------------------------
       PROBABILITY
       -------------------------------------------------------- */

    .probability-box {
        padding: 1.5rem;

        margin-top: 1rem;

        background: #FFFFFF;

        border: 1px solid #E4E7EC;
        border-radius: 12px;
    }

    .probability-header {
        display: flex;
        justify-content: space-between;

        margin-bottom: 0.6rem;

        color: #475467;

        font-size: 0.78rem;
    }

    .probability-value {
        color: #101828;

        font-weight: 700;
    }

    .progress-background {
        width: 100%;
        height: 7px;

        overflow: hidden;

        background: #EAECF0;

        border-radius: 10px;
    }

    .progress-fill {
        height: 100%;

        background: #344054;

        border-radius: 10px;
    }

    /* --------------------------------------------------------
       METRICS
       -------------------------------------------------------- */

    .metric-card {
        padding: 1.25rem;

        background: #FFFFFF;

        border: 1px solid #E4E7EC;
        border-radius: 12px;
    }

    .metric-label {
        color: #667085;

        font-size: 0.68rem;
        font-weight: 700;

        text-transform: uppercase;
        letter-spacing: 0.07em;
    }

    .metric-value {
        margin-top: 0.35rem;

        color: #101828;

        font-size: 1.4rem;
        font-weight: 650;
    }

    /* --------------------------------------------------------
       BUTTON
       -------------------------------------------------------- */

    .stButton > button {
        width: 100%;
        height: 3rem;

        border: 1px solid #172033;
        border-radius: 8px;

        background-color: #172033;
        color: #FFFFFF;

        font-size: 0.84rem;
        font-weight: 650;
    }

    .stButton > button:hover {
        border-color: #273449;
        background-color: #273449;
        color: #FFFFFF;
    }

    /* --------------------------------------------------------
       INPUTS
       -------------------------------------------------------- */

    label {
        color: #344054 !important;

        font-size: 0.76rem !important;
        font-weight: 600 !important;
    }

    /* --------------------------------------------------------
       FOOTER
       -------------------------------------------------------- */

    .footer {
        display: flex;
        justify-content: space-between;

        padding-top: 1.5rem;
        margin-top: 3rem;

        border-top: 1px solid #E4E7EC;

        color: #98A2B3;

        font-size: 0.7rem;
    }

    </style>
    """,
    unsafe_allow_html=True
)


# ============================================================
# CARREGAR DATASET
# ============================================================

@st.cache_data
def carregar_dataset():

    if not DATASET_PATH.exists():
        return None

    return pd.read_csv(DATASET_PATH)


try:

    dataset = carregar_dataset()

except Exception as error:

    st.error(
        f"Não foi possível carregar o dataset: {error}"
    )

    st.stop()


# ============================================================
# CARREGAR MODELO
# ============================================================

@st.cache_resource
def carregar_modelo():

    if not MODEL_PATH.exists():
        return None

    return joblib.load(MODEL_PATH)


try:

    modelo = carregar_modelo()

except Exception as error:

    st.error(
        f"Não foi possível carregar o modelo: {error}"
    )

    st.stop()


# ============================================================
# VERIFICAÇÃO DOS ARQUIVOS
# ============================================================

if dataset is None:

    st.error(
        "Dataset não encontrado."
    )

    st.code(
        str(DATASET_PATH),
        language="text"
    )

    st.info(
        "Verifique se o ficheiro está dentro da pasta "
        "'data' e se o nome é exatamente "
        "'dataset_carro.csv'."
    )

    st.stop()


if modelo is None:

    st.error(
        "Modelo não encontrado."
    )

    st.code(
        str(MODEL_PATH),
        language="text"
    )

    st.info(
        "Verifique se o ficheiro 'modelo.pkl' está "
        "na mesma pasta que o app.py."
    )

    st.stop()


# ============================================================
# TOP BAR
# ============================================================

st.markdown(
    """
    <div class="topbar">

        <div class="brand">
            Machine Condition Assessment
        </div>

        <div class="system-status">

            <span class="status-dot"></span>

            System operational

        </div>

    </div>
    """,
    unsafe_allow_html=True
)


# ============================================================
# HERO
# ============================================================

st.markdown(
    """
    <div class="hero">

        <div class="hero-label">
            Predictive Maintenance
        </div>

        <div class="hero-title">
            Machine condition assessment
        </div>

        <div class="hero-description">
            Evaluate the current operating conditions of a machine
            and estimate the likelihood of a failure using
            historical operati
```
