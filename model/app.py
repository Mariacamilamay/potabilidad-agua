
import streamlit as st
import joblib
import numpy as np
import pandas as pd
import os

# Configuración de la página
st.set_page_config(
    page_title="Potabilidad del Agua",
    page_icon="💧",
    layout="wide"
)

st.title("💧 Predicción de Potabilidad del Agua")
st.markdown("""
Sistema de clasificación basado en Machine Learning que determina si una muestra
de agua es **potable (1)** o **no potable (0)** según 9 parámetros químicos y físicos.
""")

# Cargar modelo y metadata
@st.cache_resource
def cargar_modelo():
    modelo = joblib.load('mejor_modelo_{}_water.joblib'.format(
        'random_forest'.replace(' ', '_')  # placeholder, se reemplaza abajo
    ))
    return modelo

@st.cache_resource
def cargar_metadata():
    return joblib.load('metadata_modelo.joblib')

try:
    meta = cargar_metadata()
    modelo = cargar_modelo()
    st.success(f"✅ Modelo cargado: **{meta['mejor_modelo']}** (ROC AUC: {meta['roc_auc_test']:.4f})")
except Exception as e:
    st.error(f"Error al cargar el modelo: {e}")
    st.stop()

# Sidebar con información
st.sidebar.header("ℹ️ Información")
st.sidebar.markdown(f"""
- **Modelo:** {meta['mejor_modelo']}
- **ROC AUC:** {meta['roc_auc_test']:.4f}
- **Umbral Youden:** {meta['umbral_youden']:.4f}
- **Umbral Financiero:** {meta['umbral_financiero']:.4f}
""")

st.sidebar.markdown("---")
umbral_seleccionado = st.sidebar.selectbox(
    "Seleccionar umbral de decisión",
    ["Youden (balance)", "Financiero (utilidad)", "0.5 (por defecto)"],
    index=0
)

if umbral_seleccionado == "Youden (balance)":
    umbral = meta['umbral_youden']
elif umbral_seleccionado == "Financiero (utilidad)":
    umbral = meta['umbral_financiero']
else:
    umbral = 0.5

st.sidebar.info(f"Umbral activo: **{umbral:.4f}**")

# Formulario de entrada
st.header("🧪 Ingrese los parámetros de la muestra")

col1, col2, col3 = st.columns(3)

with col1:
    ph = st.number_input("pH", min_value=0.0, max_value=14.0, value=7.0, step=0.1)
    hardness = st.number_input("Hardness (mg/L)", min_value=0.0, value=200.0, step=10.0)
    solids = st.number_input("Solids (ppm)", min_value=0.0, value=20000.0, step=1000.0)

with col2:
    chloramines = st.number_input("Chloramines (ppm)", min_value=0.0, value=7.0, step=0.5)
    sulfate = st.number_input("Sulfate (mg/L)", min_value=0.0, value=250.0, step=10.0)
    conductivity = st.number_input("Conductivity (μS/cm)", min_value=0.0, value=400.0, step=10.0)

with col3:
    organic_carbon = st.number_input("Organic Carbon (ppm)", min_value=0.0, value=15.0, step=1.0)
    trihalomethanes = st.number_input("Trihalomethanes (μg/L)", min_value=0.0, value=70.0, step=5.0)
    turbidity = st.number_input("Turbidity (NTU)", min_value=0.0, value=5.0, step=0.5)

# Botón de predicción
if st.button("🔬 Predecir Potabilidad", type="primary", use_container_width=True):
    datos = pd.DataFrame([{
        'ph': ph,
        'Hardness': hardness,
        'Solids': solids,
        'Chloramines': chloramines,
        'Sulfate': sulfate,
        'Conductivity': conductivity,
        'Organic_carbon': organic_carbon,
        'Trihalomethanes': trihalomethanes,
        'Turbidity': turbidity
    }])

    prob = modelo.predict_proba(datos)[0, 1]
    decision = prob >= umbral

    st.markdown("---")
    st.subheader("📊 Resultado de la Predicción")

    col_a, col_b, col_c = st.columns(3)

    with col_a:
        st.metric("Probabilidad de ser Potable", f"{prob:.2%}")

    with col_b:
        st.metric("Umbral Aplicado", f"{umbral:.4f}")

    with col_c:
        if decision:
            st.success("✅ AGUA POTABLE")
        else:
            st.error("❌ AGUA NO POTABLE")

    # Barra de progreso visual
    st.progress(float(prob))
