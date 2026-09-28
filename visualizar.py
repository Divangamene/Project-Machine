import streamlit as st
import pandas as pd
import joblib


# ============================================================
# CONFIGURAÇÃO DA PÁGINA
# ============================================================

st.set_page_config(
    page_title="Predictive Maintenance | Machine Failure",
    page_icon="⚙️",
    layout="wide",
    initial_sidebar_state="expanded"
)


# ============================================================
# CSS — DESIGN PROFISSIONAL
# ============================================================

st.markdown("""
<style>

    /* Fundo geral */
    .stApp {
        background-color: #f5f7fa;
    }

    /* Header */
    .main-header {
        background: linear-gradient(135deg, #111827, #1f2937);
        padding: 2rem 2.5rem;
        border-radius: 16px;
        margin-bottom: 2rem;
        color: white;
        box-shadow: 0 8px 25px rgba(0,0,0,0.08);
    }

    .main-header h1 {
        margin: 0;
        font-size: 2.2rem;
        font-weight: 700;
    }

    .main-header p {
        margin-top: 0.6rem;
        color: #d1d5db;
        font-size: 1rem;
    }

    /* Cards */
    .info-card {
        background: white;
        padding: 1.4rem;
        border-radius: 14px;
        border: 1px solid #e5e7eb;
        box-shadow: 0 4px 14px rgba(0,0,0,0.04);
        margin-bottom: 1rem;
    }

    .info-card h3 {
        margin-top: 0;
        color: #111827;
    }

    .info-card p {
        color: #6b7280;
        line-height: 1.6;
    }

    /* Resultado */
    .result-success {
        background: #ecfdf5;
        border: 1px solid #a7f3d0;
        padding: 1.5rem;
        border-radius: 14px;
        color: #065f46;
        text-align: center;
        margin-top: 1.5rem;
    }

    .result-danger {
        background: #fef2f2;
        border: 1px solid #fecaca;
        padding: 1.5rem;
        border-radius: 14px;
        color: #991b1b;
        text-align: center;
        margin-top: 1.5rem;
    }

    .result-title {
        font-size: 1.5rem;
        font-weight: 700;
        margin-bottom: 0.5rem;
    }

    .result-description {
        font-size: 1rem;
    }

    /* Secções */
    .section-title {
        font-size: 1.25rem;
        font-weight: 700;
        color: #111827;
        margin-top: 1rem;
        margin-bottom: 0.8rem;
    }

    /* Footer */
    .footer {
        text-align: center;
        color: #9ca3af;
        font-size: 0.85rem;
        padding: 2rem 0 1rem 0;
    }

</style>
""", unsafe_allow_html=True)


# ============================================================
# CARREGAR MODELO
# ============================================================

@st.cache_resource
def carregar_modelo():
    return joblib.load("modelo.pkl")


modelo = carregar_modelo()


# ============================================================
# HEADER
# ============================================================

st.markdown("""
<div class="main-header">

    <h1>⚙️ Predictive Maintenance</h1>

    <p>
        Sistema de previsão de falhas de máquinas baseado
        em parâmetros operacionais e técnicas de Machine Learning.
    </p>

</div>
""", unsafe_allow_html=True)


# ============================================================
# SIDEBAR
# ============================================================

with st.sidebar:

    st.markdown("## ⚙️ Sistema")

    st.markdown("""
    Esta aplicação utiliza um modelo de Machine Learning
    para estimar a possibilidade de ocorrência de uma
    falha durante o funcionamento da máquina.
    """)

    st.divider()

    st.markdown("### 📊 Variáveis analisadas")

    st.markdown("""
    - Identificador da máquina
    - Temperatura do ar
    - Temperatura do processo
    - Velocidade de rotação
    - Torque
    - Desgaste da ferramenta
    """)

    st.divider()

    st.caption("Projeto de Machine Learning")
    st.caption("Predictive Maintenance")


# ============================================================
# INTRODUÇÃO
# ============================================================

st.markdown("""
<div class="info-card">

<h3>🔎 Análise operacional</h3>

<p>
Introduza os parâmetros atuais da máquina.
O modelo irá analisar estas características e determinar
se existe indicação de uma possível falha.
</p>

</div>
""", unsafe_allow_html=True)


# ============================================================
# INPUTS
# ============================================================

st.markdown(
    '<div class="section-title">📋 Parâmetros da máquina</div>',
    unsafe_allow_html=True
)

col1, col2 = st.columns(2)


# ------------------------------------------------------------
# COLUNA 1
# ------------------------------------------------------------

with col1:

    udi = st.number_input(
        "Identificador da máquina",
        min_value=1,
        max_value=10000,
        value=1,
        step=1,
        help="Identificador único utilizado para distinguir cada registo."
    )

    air_temp = st.number_input(
        "Temperatura do ar [K]",
        min_value=250.0,
        max_value=350.0,
        value=298.0,
        step=0.1,
        help="Temperatura ambiente medida em Kelvin."
    )

    process_temp = st.number_input(
        "Temperatura do processo [K]",
        min_value=250.0,
        max_value=400.0,
        value=308.0,
        step=0.1,
        help="Temperatura registada durante o processo."
    )


# ------------------------------------------------------------
# COLUNA 2
# ------------------------------------------------------------

with col2:

    rotational_speed = st.number_input(
        "Velocidade de rotação [rpm]",
        min_value=0.0,
        max_value=5000.0,
        value=1500.0,
        step=10.0,
        help="Velocidade de rotação da ferramenta em rotações por minuto."
    )

    torque = st.number_input(
        "Torque [Nm]",
        min_value=0.0,
        max_value=150.0,
        value=40.0,
        step=0.5,
        help="Torque aplicado durante o funcionamento."
    )

    tool_wear = st.number_input(
        "Desgaste da ferramenta [min]",
        min_value=0.0,
        max_value=300.0,
        value=100.0,
        step=1.0,
        help="Tempo acumulado de utilização da ferramenta."
    )


# ============================================================
# PREVISÃO
# ============================================================

st.markdown("---")

if st.button(
    "🔍 Analisar estado da máquina",
    use_container_width=True,
    type="primary"
):

    # --------------------------------------------------------
    # Dados para o modelo
    # --------------------------------------------------------

    dados = pd.DataFrame([{
        "UDI": udi,
        "Air temperature [K]": air_temp,
        "Process temperature [K]": process_temp,
        "Rotational speed [rpm]": rotational_speed,
        "Torque [Nm]": torque,
        "Tool wear [min]": tool_wear
    }])


    # --------------------------------------------------------
    # Previsão
    # --------------------------------------------------------

    previsao = modelo.predict(dados)[0]


    # --------------------------------------------------------
    # Resultado
    # --------------------------------------------------------

    st.markdown("## 📊 Resultado da análise")


    if previsao == 1:

        st.markdown("""
        <div class="result-danger">

            <div class="result-title">
                ⚠️ Possível falha detetada
            </div>

            <div class="result-description">
                O modelo identificou condições compatíveis
                com uma possível falha da máquina.
                Recomenda-se a análise dos parâmetros
                operacionais e a realização de manutenção preventiva.
            </div>

        </div>
        """, unsafe_allow_html=True)

    else:

        st.markdown("""
        <div class="result-success">

            <div class="result-title">
                ✅ Funcionamento normal
            </div>

            <div class="result-description">
                O modelo não identificou indícios suficientes
                de falha nas condições analisadas.
            </div>

        </div>
        """, unsafe_allow_html=True)


    # --------------------------------------------------------
    # Probabilidade
    # --------------------------------------------------------

    if hasattr(modelo, "predict_proba"):

        probabilidade = modelo.predict_proba(dados)[0][1]

        st.markdown("### 📈 Probabilidade estimada")

        col_a, col_b, col_c = st.columns(3)

        with col_a:
            st.metric(
                "Probabilidade de falha",
                f"{probabilidade:.1%}"
            )

        with col_b:
            st.metric(
                "Temperatura do ar",
                f"{air_temp:.1f} K"
            )

        with col_c:
            st.metric(
                "Desgaste da ferramenta",
                f"{tool_wear:.0f} min"
            )


    # --------------------------------------------------------
    # Dados utilizados
    # --------------------------------------------------------

    with st.expander("🔎 Ver dados utilizados na previsão"):

        st.dataframe(
            dados,
            use_container_width=True,
            hide_index=True
        )


# ============================================================
# RODAPÉ
# ============================================================

st.markdown("""
<div class="footer">

    Predictive Maintenance · Machine Learning Project<br>
    Sistema desenvolvido para análise e previsão de falhas industriais

</div>
""", unsafe_allow_html=True)
