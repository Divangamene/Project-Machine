import streamlit as st

import pandas as pd

from sklearn.model_selection import train_test_split

from sklearn.linear_model import LogisticRegression



# 1. Configuração da Página

st.set_page_config(

    page_title="Previsão de Falha do Veículo",

    page_icon="🚗",

    layout="centered"

)



# 2. Função com cache para treinar e manter o modelo em memória

@st.cache_resource

def carregar_e_treinar_modelo():

    base_dados = pd.read_csv("dataset_carro.csv", keep_default_na=False)

   

    features = [

        'SoC', 'SoH', 'Battery_Voltage', 'Battery_Temperature',

        'Motor_Temperature', 'Motor_Vibration', 'Driving_Speed'

    ]

    X = base_dados[features]

    y = base_dados['Failure_Probability']

   

    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

    model = LogisticRegression(max_iter=1000)

    model.fit(X_train, y_train)

   

    return model



# Carregamento seguro do modelo

try:

    model = carregar_e_treinar_modelo()

except FileNotFoundError:

    st.error("❌ O arquivo 'dataset_carro.csv' não foi encontrado na mesma pasta do código.")

    st.stop()

except Exception as e:

    st.error(f"❌ Erro ao processar os dados: {e}")

    st.stop()



# 3. Interface Gráfica

st.title("🚗 Previsão de Falha de Componentes")

st.write("Insira os parâmetros de telemetria do veículo para prever o risco de falha.")



st.subheader("📊 Dados de Telemetria")



col1, col2 = st.columns(2)



with col1:

    soc = st.slider("Estado de Carga (SoC)", 0.0, 1.0, 0.80, step=0.01)

    soh = st.slider("Estado de Saúde da Bateria (SoH)", 0.0, 1.0, 0.90, step=0.01)

    battery_voltage = st.number_input("Tensão da Bateria (V)", value=350.0, step=1.0)

    battery_temp = st.number_input("Temperatura da Bateria (°C)", value=30.0, step=0.5)



with col2:

    motor_temp = st.number_input("Temperatura do Motor (°C)", value=50.0, step=0.5)

    motor_vibration = st.number_input("Vibração do Motor", value=0.5, step=0.1)

    speed = st.number_input("Velocidade (km/h)", value=60.0, step=1.0)



st.markdown("---")



# 4. Execução da Previsão

if st.button("🔮 Prever Risco de Falha", use_container_width=True):

    input_data = pd.DataFrame([[

        soc, soh, battery_voltage, battery_temp,

        motor_temp, motor_vibration, speed

    ]], columns=[

        'SoC', 'SoH', 'Battery_Voltage', 'Battery_Temperature',

        'Motor_Temperature', 'Motor_Vibration', 'Driving_Speed'

    ])

   

    prediction = model.predict(input_data)[0]

    probabilities = model.predict_proba(input_data)[0]

    prob_failure = probabilities[1] * 100



    st.subheader("📌 Resultado da Análise")

   

    if prediction == 1:

        st.error(f"⚠️ **Atenção:** Alto Risco de Falha! (Probabilidade: {prob_failure:.1f}%)")

    else:

        st.success(f"✅ **Estado Normal:** Baixo Risco de Falha (Probabilidade de Falha: {prob_failure:.1f}%)")



    st.progress(int(prob_failure))
