import streamlit as st
import pandas as pd
import numpy as np
import joblib
import plotly.express as px
import plotly.graph_objects as go

# Configuración de la página
st.set_page_config(
    page_title="🚰 Predictor de Potabilidad del Agua",
    page_icon="💧",
    layout="wide"
)

# Carga del modelo
@st.cache_resource
def cargar_modelo():
    modelo = joblib.load('mejor_modelo_xgboost_water.joblib')
    metadata = joblib.load('metadata_modelo.joblib')
    return modelo, metadata

try:
    modelo, metadata = cargar_modelo()
    modelo_cargado = True
except Exception as e:
    modelo_cargado = False
    st.error(f"❌ Error al cargar el modelo: {e}")

# Estilo personalizado
st.markdown("""
<style>
    .main-title {
        font-size: 3rem;
        font-weight: bold;
        background: linear-gradient(90deg, #00b4d8, #0077b6);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        text-align: center;
    }
    .potable {
        background: linear-gradient(135deg, #11998e 0%, #38ef7d 100%);
        padding: 2rem; border-radius: 20px; color: white;
        text-align: center; font-size: 1.5rem; font-weight: bold;
    }
    .no-potable {
        background: linear-gradient(135deg, #eb3349 0%, #f45c43 100%);
        padding: 2rem; border-radius: 20px; color: white;
        text-align: center; font-size: 1.5rem; font-weight: bold;
    }
</style>
""", unsafe_allow_html=True)

st.markdown('<p class="main-title">💧 Predictor de Potabilidad del Agua</p>', 
            unsafe_allow_html=True)

if modelo_cargado:
    tab1, tab2 = st.tabs(["🔬 Predicción Manual", "📁 Carga de CSV"])
    
    with tab1:
        st.header("🔬 Análisis de Muestra de Agua")
        col1, col2, col3 = st.columns(3)
        
        with col1:
            ph = st.slider("pH", 0.0, 14.0, 7.0, 0.1)
            hardness = st.number_input("Hardness (mg/L)", 0.0, 500.0, 150.0)
            solids = st.number_input("Solids (ppm)", 0.0, 100000.0, 20000.0)
        
        with col2:
            chloramines = st.number_input("Chloramines (mg/L)", 0.0, 20.0, 5.0)
            sulfate = st.number_input("Sulfate (mg/L)", 0.0, 500.0, 250.0)
            conductivity = st.number_input("Conductivity (μS/cm)", 0.0, 1000.0, 300.0)
        
        with col3:
            organic_carbon = st.number_input("Organic Carbon (mg/L)", 0.0, 50.0, 10.0)
            trihalomethanes = st.number_input("Trihalomethanes (μg/L)", 0.0, 150.0, 50.0)
            turbidity = st.number_input("Turbidity (NTU)", 0.0, 10.0, 3.0)
        
        if st.button("🔍 Analizar Muestra", type="primary", use_container_width=True):
            datos = pd.DataFrame([{
                'ph': ph, 'Hardness': hardness, 'Solids': solids,
                'Chloramines': chloramines, 'Sulfate': sulfate,
                'Conductivity': conductivity, 'Organic_carbon': organic_carbon,
                'Trihalomethanes': trihalomethanes, 'Turbidity': turbidity
            }])
            
            probabilidad = modelo.predict_proba(datos)[0][1]
            decision = 1 if probabilidad >= metadata['umbral_financiero'] else 0
            
            col_a, col_b, col_c = st.columns(3)
            with col_a:
                st.metric("Probabilidad", f"{probabilidad*100:.2f}%")
            with col_b:
                st.metric("Umbral", f"{metadata['umbral_financiero']:.4f}")
            with col_c:
                if decision == 1:
                    st.markdown('<div class="potable">✅ AGUA POTABLE</div>', 
                               unsafe_allow_html=True)
                else:
                    st.markdown('<div class="no-potable">❌ NO POTABLE</div>', 
                               unsafe_allow_html=True)
            
            fig = go.Figure(go.Indicator(
                mode="gauge+number",
                value=probabilidad * 100,
                title={'text': "Probabilidad de Potabilidad (%)"},
                gauge={
                    'axis': {'range': [0, 100]},
                    'steps': [
                        {'range': [0, 30], 'color': "#f45c43"},
                        {'range': [30, 60], 'color': "#ffd700"},
                        {'range': [60, 100], 'color': "#38ef7d"}
                    ],
                    'threshold': {
                        'line': {'color': "black", 'width': 4},
                        'value': metadata['umbral_financiero'] * 100
                    }
                }
            ))
            st.plotly_chart(fig, use_container_width=True)
    
    with tab2:
        st.header("📁 Análisis Masivo desde CSV")
        uploaded_file = st.file_uploader("Selecciona un archivo CSV", type=['csv'])
        
        if uploaded_file is not None:
            df_upload = pd.read_csv(uploaded_file)
            st.success(f"✅ Archivo cargado: {df_upload.shape[0]} muestras")
            
            if st.button("🚀 Procesar"):
                X_upload = df_upload[metadata['columnas']]
                probabilidades = modelo.predict_proba(X_upload)[:, 1]
                df_upload['Probabilidad'] = probabilidades
                df_upload['Decision'] = (probabilidades >= metadata['umbral_financiero']).astype(int)
                
                st.metric("✅ Potables", (df_upload['Decision'] == 1).sum())
                st.metric("❌ No Potables", (df_upload['Decision'] == 0).sum())
                
                csv = df_upload.to_csv(index=False).encode('utf-8')
                st.download_button("📥 Descargar Resultados", csv, 
                                  "resultados.csv", "text/csv")