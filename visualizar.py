
import streamlit as st
import pandas as pd
import joblib


# Configuração
st.set_page_config(
    page_title="Predição de Falha",
    page_icon="⚙️",
    layout="centered"
)


# Carregar modelo
@st.cache_resource
def carregar_modelo():
    return joblib.load("modelo.pkl")


modelo = carregar_modelo()


# Interface
st.title("⚙️ Predição de Falha da Máquina")
st.write("Introduza os parâmetros da máquina para realizar uma previsão.")


col1, col2 = st.columns(2)

with col1:
    udi = st.number_input("UDI", value=1)
    air_temp = st.number_input("Temperatura do ar [K]", value=298.0)
    process_temp = st.number_input("Temperatura do processo [K]", value=308.0)
    torque = st.number_input("Torque [Nm]", value=40.0)
    tool_wear = st.number_input("Desgaste da ferramenta [min]", value=100.0)

with col2:
    twf = st.selectbox("TWF", [0, 1])
    hdf = st.selectbox("HDF", [0, 1])
    pwf = st.selectbox("PWF", [0, 1])
    osf = st.selectbox("OSF", [0, 1])
    rnf = st.selectbox("RNF", [0, 1])


# Previsão
if st.button("🔍 Fazer previsão", use_container_width=True):

    dados = pd.DataFrame([{
        "UDI": udi,
        "Air temperature [K]": air_temp,
        "Process temperature [K]": process_temp,
        "Torque [Nm]": torque,
        "Tool wear [min]": tool_wear,
        "TWF": twf,
        "HDF": hdf,
        "PWF": pwf,
        "OSF": osf,
        "RNF": rnf
    }])

    previsao = modelo.predict(dados)[0]

    st.divider()

    if previsao == 1:
        st.error("⚠️ Falha prevista")
    else:
        st.success("✅ Máquina sem falha prevista")

    # Probabilidade, caso o modelo suporte
    if hasattr(modelo, "predict_proba"):
        probabilidade = modelo.predict_proba(dados)[0][1]
        st.metric(
            "Probabilidade de falha",
            f"{probabilidade:.1%}"
        )
