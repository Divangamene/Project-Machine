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
            historical operational data.
        </div>

    </div>
    """,
    unsafe_allow_html=True
)


# ============================================================
# LAYOUT PRINCIPAL
# ============================================================

left_column, right_column = st.columns(
    [1.4, 0.8],
    gap="large"
)


# ============================================================
# PARÂMETROS
# ============================================================

with left_column:

    st.markdown(
        """
        <div class="section-title">
            Operational parameters
        </div>
        """,
        unsafe_allow_html=True
    )

    st.markdown(
        """
        <div class="card">

            <div class="card-title">
                Machine operating conditions
            </div>

            <div class="card-description">
                Enter the measurements collected from the machine.
            </div>

        </div>
        """,
        unsafe_allow_html=True
    )

    col1, col2 = st.columns(2)

    with col1:

        air_temperature = st.number_input(
            "Air temperature [K]",
            min_value=250.0,
            max_value=350.0,
            value=298.0,
            step=0.1
        )

        process_temperature = st.number_input(
            "Process temperature [K]",
            min_value=250.0,
            max_value=400.0,
            value=308.0,
            step=0.1
        )

        rotational_speed = st.number_input(
            "Rotational speed [rpm]",
            min_value=0.0,
            max_value=5000.0,
            value=1500.0,
            step=10.0
        )

    with col2:

        torque = st.number_input(
            "Torque [Nm]",
            min_value=0.0,
            max_value=150.0,
            value=40.0,
            step=0.5
        )

        tool_wear = st.number_input(
            "Tool wear [min]",
            min_value=0.0,
            max_value=300.0,
            value=100.0,
            step=1.0
        )

        machine_id = st.number_input(
            "Machine identifier",
            min_value=1,
            max_value=10000,
            value=1,
            step=1
        )

    st.markdown("<br>", unsafe_allow_html=True)

    analisar = st.button(
        "Assess machine condition"
    )


# ============================================================
# INFORMAÇÃO
# ============================================================

with right_column:

    st.markdown(
        """
        <div class="section-title">
            Assessment scope
        </div>
        """,
        unsafe_allow_html=True
    )

    st.markdown(
        """
        <div class="card">

            <div class="card-title">
                Operational assessment
            </div>

            <div class="card-description">
                The assessment considers the main operating
                characteristics associated with machine condition.
            </div>

            <div style="
                border-top: 1px solid #EAECF0;
                padding-top: 0.8rem;
            ">

                <div style="
                    padding: 0.5rem 0;
                    color: #475467;
                    font-size: 0.82rem;
                ">
                    Temperature
                </div>

                <div style="
                    padding: 0.5rem 0;
                    color: #475467;
                    font-size: 0.82rem;
                ">
                    Rotation
                </div>

                <div style="
                    padding: 0.5rem 0;
                    color: #475467;
                    font-size: 0.82rem;
                ">
                    Torque
                </div>

                <div style="
                    padding: 0.5rem 0;
                    color: #475467;
                    font-size: 0.82rem;
                ">
                    Tool wear
                </div>

            </div>

        </div>
        """,
        unsafe_allow_html=True
    )


# ============================================================
# PREVISÃO
# ============================================================

if analisar:

    # --------------------------------------------------------
    # Dados
    # --------------------------------------------------------

    dados = pd.DataFrame(
        [{
            "UDI": machine_id,
            "Air temperature [K]": air_temperature,
            "Process temperature [K]": process_temperature,
            "Rotational speed [rpm]": rotational_speed,
            "Torque [Nm]": torque,
            "Tool wear [min]": tool_wear
        }]
    )


    # --------------------------------------------------------
    # Previsão
    # --------------------------------------------------------

    try:

        previsao = modelo.predict(dados)[0]

    except Exception as error:

        st.error(
            "O modelo não conseguiu processar os dados fornecidos."
        )

        with st.expander("Detalhes técnicos"):

            st.code(
                str(error),
                language="text"
            )

        st.stop()


    # --------------------------------------------------------
    # Probabilidade
    # --------------------------------------------------------

    probabilidade = None

    if hasattr(modelo, "predict_proba"):

        try:

            probabilidade = modelo.predict_proba(
                dados
            )[0][1]

        except Exception:

            probabilidade = None


    # ========================================================
    # RESULTADO
    # ========================================================

    st.markdown(
        "<br>",
        unsafe_allow_html=True
    )

    st.markdown(
        """
        <div class="section-title">
            Assessment result
        </div>
        """,
        unsafe_allow_html=True
    )


    # --------------------------------------------------------
    # Estado
    # --------------------------------------------------------

    if previsao == 1:

        if probabilidade is not None and probabilidade >= 0.70:

            classe = "critical"
            estado = "HIGH RISK"

            descricao = (
                "The current operating conditions indicate "
                "a high estimated likelihood of machine failure."
            )

        else:

            classe = "warning"
            estado = "ATTENTION"

            descricao = (
                "The current operating conditions indicate "
                "an increased estimated likelihood of machine failure."
            )

    else:

        classe = "normal"
        estado = "NORMAL"

        descricao = (
            "The current operating conditions do not indicate "
            "a machine failure."
        )


    st.markdown(
        f"""
        <div class="assessment">

            <div class="assessment-label">
                Current assessment
            </div>

            <div class="assessment-status {classe}">
                {estado}
            </div>

            <div class="assessment-description">
                {descricao}
            </div>

        </div>
        """,
        unsafe_allow_html=True
    )


    # ========================================================
    # PROBABILIDADE
    # ========================================================

    if probabilidade is not None:

        percentagem = max(
            0,
            min(
                probabilidade * 100,
                100
            )
        )

        st.markdown(
            f"""
            <div class="probability-box">

                <div class="assessment-label">
                    Estimated failure probability
                </div>

                <div class="probability-header">

                    <span>
                        Model assessment
                    </span>

                    <span class="probability-value">
                        {percentagem:.1f}%
                    </span>

                </div>

                <div class="progress-background">

                    <div
                        class="progress-fill"
                        style="width:{percentagem}%"
                    ></div>

                </div>

            </div>
            """,
            unsafe_allow_html=True
        )


    # ========================================================
    # INDICADORES
    # ========================================================

    st.markdown(
        "<br>",
        unsafe_allow_html=True
    )

    st.markdown(
        """
        <div class="section-title">
            Current operating values
        </div>
        """,
        unsafe_allow_html=True
    )


    metric1, metric2, metric3 = st.columns(3)


    with metric1:

        st.markdown(
            f"""
            <div class="metric-card">

                <div class="metric-label">
                    Air temperature
                </div>

                <div class="metric-value">
                    {air_temperature:.1f} K
                </div>

            </div>
            """,
            unsafe_allow_html=True
        )


    with metric2:

        st.markdown(
            f"""
            <div class="metric-card">

                <div class="metric-label">
                    Rotational speed
                </div>

                <div class="metric-value">
                    {rotational_speed:,.0f} rpm
                </div>

            </div>
            """,
            unsafe_allow_html=True
        )


    with metric3:

        st.markdown(
            f"""
            <div class="metric-card">

                <div class="metric-label">
                    Tool wear
                </div>

                <div class="metric-value">
                    {tool_wear:.0f} min
                </div>

            </div>
            """,
            unsafe_allow_html=True
        )


    # ========================================================
    # DADOS DA PREVISÃO
    # ========================================================

    st.markdown("<br>", unsafe_allow_html=True)

    with st.expander("View assessment data"):

        st.dataframe(
            dados,
            use_container_width=True,
            hide_index=True
        )


# ============================================================
# FOOTER
# ============================================================

st.markdown(
    """
    <div class="footer">

        <div>
            Machine Condition Assessment
        </div>

        <div>
            Predictive Maintenance · Operational Analytics
        </div>

    </div>
    """,
    unsafe_allow_html=True
)
