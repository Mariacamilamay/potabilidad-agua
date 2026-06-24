import dash
from dash import dcc, html, Input, Output, dash_table, callback_context, State
import plotly.express as px
import plotly.graph_objects as go
import pandas as pd
import dash_bootstrap_components as dbc
import pickle
import numpy as np
from pathlib import Path

# ==========================================
# 1. CARGA DE DATOS
# ==========================================
try:
    df = pd.read_csv('D:\mmay\OneDrive - Triple A\Analisis Potabilidad Agua\water-potability-project\docs\dash-agua\water_potability.csv')
    print("✓ Datos cargados correctamente")
    print(f"Filas: {len(df)}, Columnas: {len(df.columns)}")
except Exception as e:
    print(f"Error al cargar datos: {e}")
    df = pd.DataFrame({
        'ph': [7.0, 6.5, 8.0],
        'Hardness': [200, 150, 250],
        'Solids': [20000, 18000, 22000],
        'Chloramines': [7, 6, 8],
        'Sulfate': [350, 300, 400],
        'Conductivity': [400, 350, 450],
        'Organic_carbon': [14, 12, 16],
        'Trihalomethanes': [65, 55, 75],
        'Turbidity': [4, 3, 5],
        'Potability': [0, 1, 0]
    })

# ==========================================
# 2. CARGA DEL MODELO
# ==========================================
MODEL_PATH = 'modelo.pkl'  # Cambiar por la ruta correcta de tu pickle
model = None
feature_names = None

try:
    with open(MODEL_PATH, 'rb') as f:
        model = pickle.load(f)
    print("✓ Modelo cargado correctamente")
    
    # Inferir nombres de características del dataframe
    feature_names = [col for col in df.columns if col != 'Potability']
    print(f"Características: {feature_names}")
except FileNotFoundError:
    print(f"⚠️ Archivo {MODEL_PATH} no encontrado. El predictor no funcionará.")
    model = None
except Exception as e:
    print(f"⚠️ Error al cargar modelo: {e}")
    model = None

# ==========================================
# 3. INICIALIZAR APP CON BOOTSTRAP
# ==========================================
app = dash.Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])
app.config.suppress_callback_exceptions = True
server = app.server

# ==========================================
# 4. COMPONENTES REUTILIZABLES
# ==========================================

def create_card(title, content, color="primary", icon=None):
    """Crea una card de Bootstrap con estilo"""
    return dbc.Card([
        dbc.CardHeader([
            html.H4(title, className="mb-0", style={"color": "white"}),
        ], style={"backgroundColor": f"var(--bs-{color})", "borderRadius": "10px 10px 0 0"}),
        dbc.CardBody(content, style={"padding": "25px"})
    ], className="mb-4 shadow-sm", style={"borderRadius": "10px", "border": "none"})

def create_stat_card(title, value, subtitle, icon, color="primary"):
    """Crea una card de estadísticas"""
    return dbc.Col([
        dbc.Card([
            dbc.CardBody([
                html.Div([
                    html.I(className=f"fas {icon}", style={"fontSize": "2.5rem", "opacity": 0.3}),
                ], style={"position": "absolute", "top": "20px", "right": "20px"}),
                html.H6(title, className="text-muted mb-2"),
                html.H3(value, className=f"text-{color} mb-2"),
                html.P(subtitle, className="text-muted mb-0", style={"fontSize": "0.9rem"})
            ], style={"position": "relative"})
        ], className="border-0 shadow-sm", style={"borderRadius": "15px", "backgroundColor": "white"})
    ], md=3, className="mb-4")

# ==========================================
# 5. SECCIONES DE CONTENIDO
# ==========================================

# Navbar
navbar = dbc.NavbarSimple(
    children=[
        dbc.NavItem(dbc.NavLink(" Introducción", href="#", id="nav-intro", active=True)),
        dbc.NavItem(dbc.NavLink(" Problema", href="#", id="nav-problema")),
        dbc.NavItem(dbc.NavLink(" Objetivos", href="#", id="nav-objetivos")),
        dbc.NavItem(dbc.NavLink(" Justificación", href="#", id="nav-justificacion")),
        dbc.NavItem(dbc.NavLink(" Análisis EDA", href="#", id="nav-eda")),
        dbc.NavItem(dbc.NavLink("🤖 Predictor", href="#", id="nav-predictor")),  # NUEVO
    ],
    brand="🌊 Potabilidad del Agua",
    brand_href="#",
    color="primary",
    dark=True,
    sticky="top",
    className="shadow-sm"
)

# Hero Section
hero_section = dbc.Container([
    dbc.Row([
        dbc.Col([
            html.H1("Predicción de la Potabilidad del Agua", className="display-4 fw-bold text-white mb-3"),
            html.P("Análisis Exploratorio de Datos y Modelado Predictivo usando Machine Learning", 
                   className="lead text-white-50"),
            dbc.Button("Ver Análisis", id="btn-ver-analisis", color="light", size="lg", className="mt-3"),
        ], className="text-center py-5")
    ], className="py-5")
], className="bg-primary", style={"borderRadius": "0 0 30px 30px", "marginBottom": "40px"})

# Sección Introducción (mantenida igual que antes)
intro_section = dbc.Container([
    create_card("1. Introducción", [
        html.P("""
        La calidad del agua es un factor esencial para la salud y el bienestar de las personas. 
        Evaluar si el agua es apta para el consumo humano requiere analizar diversas características 
        fisicoquímicas que influyen en su potabilidad.
        """, className="lead"),
        html.P("""
        En este proyecto se realiza un análisis exploratorio de datos sobre muestras de agua con el 
        fin de identificar patrones y relaciones entre las variables. Posteriormente, se aplicarán 
        técnicas de aprendizaje automático para desarrollar un modelo capaz de predecir si una 
        muestra de agua es potable o no a partir de sus características.
        """)
    ], color="primary")
], className="py-4")

# Sección Problema (mantenida igual)
problema_section = dbc.Container([
    create_card("2. Planteamiento del Problema", [
        html.P("""
        La calidad del agua es un aspecto fundamental para la salud humana, ya que el consumo de 
        agua contaminada puede generar diversas enfermedades y afectar la calidad de vida de la población.
        """, className="mb-3"),
        dbc.Alert([
            html.H4("Pregunta de Investigación", className="alert-heading"),
            html.P("¿Es posible predecir la potabilidad del agua a partir de sus características fisicoquímicas mediante el uso de modelos de aprendizaje automático?", className="mb-0")
        ], color="warning", className="mt-4")
    ], color="danger")
], className="py-4")

# Sección Objetivos (mantenida igual)
objetivos_section = dbc.Container([
    create_card("3. Objetivos", [
        dbc.Row([
            dbc.Col([
                dbc.Card([
                    dbc.CardHeader(html.H5("Objetivo General", className="text-white mb-0")),
                    dbc.CardBody([
                        html.P("""
                        Desarrollar un modelo de aprendizaje automático que permita predecir la 
                        potabilidad del agua a partir de sus características fisicoquímicas.
                        """, className="mb-0")
                    ])
                ], className="border-0 shadow-sm mb-4")
            ])
        ]),
        html.H5("Objetivos Específicos", className="mb-3"),
        dbc.ListGroup([
            dbc.ListGroupItem(" Realizar un análisis exploratorio de los datos", className="d-flex align-items-center"),
            dbc.ListGroupItem(" Identificar las variables con mayor influencia", className="d-flex align-items-center"),
            dbc.ListGroupItem(" Preparar y transformar los datos", className="d-flex align-items-center"),
            dbc.ListGroupItem(" Entrenar y evaluar modelos de clasificación", className="d-flex align-items-center"),
            dbc.ListGroupItem(" Comparar el desempeño de los modelos", className="d-flex align-items-center"),
        ], flush=True, className="mb-3")
    ], color="success")
], className="py-4")

# Sección Justificación (mantenida igual)
justificacion_section = dbc.Container([
    create_card("4. Justificación", [
        dbc.Row([
            dbc.Col([
                html.Div([
                    html.I(className="fas fa-tint", style={"fontSize": "3rem", "color": "#0d6efd"}),
                    html.H5("Importancia para la Salud", className="mt-3"),
                    html.P("""
                    El acceso a agua potable es fundamental para la salud y la calidad de vida de la población.
                    """)
                ], className="text-center p-3")
            ], md=6),
            dbc.Col([
                html.Div([
                    html.I(className="fas fa-chart-line", style={"fontSize": "3rem", "color": "#198754"}),
                    html.H5("Ciencia de Datos", className="mt-3"),
                    html.P("""
                    Aplicación de técnicas de análisis de datos y aprendizaje automático para la evaluación de calidad.
                    """)
                ], className="text-center p-3")
            ], md=6)
        ])
    ], color="info")
], className="py-4")

# ==========================================
# 6. NUEVA SECCIÓN: PREDICTOR DEL MODELO
# ==========================================
predictor_section = dbc.Container([
    create_card("5. Predictor de Potabilidad 🤖", [
        dbc.Alert(
            [
                html.I(className="fas fa-info-circle me-2"),
                "Ingresa los valores de las características fisicoquímicas para predecir si el agua es potable"
            ],
            color="info",
            className="mb-4"
        ) if model else dbc.Alert(
            [
                html.I(className="fas fa-exclamation-triangle me-2"),
                "El modelo no está disponible. Asegúrate de que el archivo pickle esté en la ruta correcta."
            ],
            color="danger",
            className="mb-4"
        ),
        
        # Inputs para las características
        dbc.Row([
            dbc.Col([
                html.Label("pH", className="fw-bold"),
                dbc.Input(id="input-ph", type="number", placeholder="7.0", value=7.0, min=0, max=14, step=0.1),
            ], md=4, className="mb-3"),
            dbc.Col([
                html.Label("Dureza (Hardness)", className="fw-bold"),
                dbc.Input(id="input-hardness", type="number", placeholder="200", value=200, min=0, step=1),
            ], md=4, className="mb-3"),
            dbc.Col([
                html.Label("Sólidos (Solids)", className="fw-bold"),
                dbc.Input(id="input-solids", type="number", placeholder="20000", value=20000, min=0, step=100),
            ], md=4, className="mb-3"),
        ]),
        
        dbc.Row([
            dbc.Col([
                html.Label("Cloraminas (Chloramines)", className="fw-bold"),
                dbc.Input(id="input-chloramines", type="number", placeholder="7", value=7, min=0, step=0.1),
            ], md=4, className="mb-3"),
            dbc.Col([
                html.Label("Sulfatos (Sulfate)", className="fw-bold"),
                dbc.Input(id="input-sulfate", type="number", placeholder="350", value=350, min=0, step=1),
            ], md=4, className="mb-3"),
            dbc.Col([
                html.Label("Conductividad (Conductivity)", className="fw-bold"),
                dbc.Input(id="input-conductivity", type="number", placeholder="400", value=400, min=0, step=1),
            ], md=4, className="mb-3"),
        ]),
        
        dbc.Row([
            dbc.Col([
                html.Label("Carbono Orgánico (Organic_carbon)", className="fw-bold"),
                dbc.Input(id="input-organic-carbon", type="number", placeholder="14", value=14, min=0, step=0.1),
            ], md=4, className="mb-3"),
            dbc.Col([
                html.Label("Trihalometanos (Trihalomethanes)", className="fw-bold"),
                dbc.Input(id="input-trihalomethanes", type="number", placeholder="65", value=65, min=0, step=1),
            ], md=4, className="mb-3"),
            dbc.Col([
                html.Label("Turbidez (Turbidity)", className="fw-bold"),
                dbc.Input(id="input-turbidity", type="number", placeholder="4", value=4, min=0, step=0.1),
            ], md=4, className="mb-3"),
        ]),
        
        # Botón de predicción
        dbc.Row([
            dbc.Col([
                dbc.Button(
                    [html.I(className="fas fa-magic me-2"), "Predecir"],
                    id="btn-predecir",
                    color="success",
                    size="lg",
                    className="w-100",
                    disabled=model is None
                )
            ], md=12, className="mb-4")
        ]),
        
        # Resultado de la predicción
        dbc.Row([
            dbc.Col([
                html.Div(id="resultado-prediccion", className="mt-4")
            ])
        ])
        
    ], color="primary")
], className="py-4")

# ==========================================
# 7. SECCIÓN EDA (condensada)
# ==========================================
eda_section = dbc.Container([
    # Estadísticas rápidas
    dbc.Row([
        create_stat_card("Total de Muestras", f"{len(df):,}", "Registros analizados", "fa-database", "primary"),
        create_stat_card("Variables", f"{len(df.columns)}", "Características fisicoquímicas", "fa-sliders-h", "success"),
        create_stat_card("Agua Potable", f"{df['Potability'].sum():,}", f"{100*df['Potability'].mean():.1f}% del total", "fa-check-circle", "success"),
        create_stat_card("Agua No Potable", f"{len(df) - df['Potability'].sum():,}", f"{100*(1-df['Potability'].mean()):.1f}% del total", "fa-times-circle", "danger"),
    ], className="mb-4"),
    
    # Gráficos
    create_card("Distribución de la Potabilidad", [
        dcc.Graph(id='grafico-potabilidad')
    ]),
    
    create_card("Correlación con Potabilidad", [
        dcc.Graph(id='grafico-correlacion-potabilidad')
    ]),
    
    create_card("Matriz de Correlación", [
        dcc.Graph(id='grafico-matriz-correlacion')
    ]),
    
], className="py-4")

# ==========================================
# 8. LAYOUT PRINCIPAL
# ==========================================
app.layout = html.Div([
    navbar,
    hero_section,
    html.Div(id="contenido-principal"),
])

# ==========================================
# 9. CALLBACKS
# ==========================================

@app.callback(
    Output("contenido-principal", "children"),
    [Input("nav-intro", "n_clicks"),
     Input("nav-problema", "n_clicks"),
     Input("nav-objetivos", "n_clicks"),
     Input("nav-justificacion", "n_clicks"),
     Input("nav-eda", "n_clicks"),
     Input("nav-predictor", "n_clicks")],
)
def actualizar_contenido(intro_clicks, problema_clicks, obj_clicks, just_clicks, eda_clicks, pred_clicks):
    ctx = callback_context
    if not ctx.triggered:
        return intro_section
    
    button_id = ctx.triggered[0]["prop_id"].split(".")[0]
    
    if button_id == 'nav-problema':
        return problema_section
    elif button_id == 'nav-objetivos':
        return objetivos_section
    elif button_id == 'nav-justificacion':
        return justificacion_section
    elif button_id == 'nav-eda':
        return eda_section
    elif button_id == 'nav-predictor':
        return predictor_section
    else:
        return intro_section

# ==========================================
# 10. CALLBACK DE PREDICCIÓN
# ==========================================

@app.callback(
    Output("resultado-prediccion", "children"),
    Input("btn-predecir", "n_clicks"),
    [
        State("input-ph", "value"),
        State("input-hardness", "value"),
        State("input-solids", "value"),
        State("input-chloramines", "value"),
        State("input-sulfate", "value"),
        State("input-conductivity", "value"),
        State("input-organic-carbon", "value"),
        State("input-trihalomethanes", "value"),
        State("input-turbidity", "value"),
    ],
    prevent_initial_call=True
)
def hacer_prediccion(n_clicks, ph, hardness, solids, chloramines, sulfate, 
                     conductivity, organic_carbon, trihalomethanes, turbidity):
    
    if model is None:
        return dbc.Alert(
            "Error: El modelo no está disponible",
            color="danger"
        )
    
    try:
        # Crear array con los valores en el orden correcto
        caracteristicas = np.array([[
            ph, hardness, solids, chloramines, sulfate, 
            conductivity, organic_carbon, trihalomethanes, turbidity
        ]])
        
        # Hacer predicción
        prediccion = model.predict(caracteristicas)[0]
        probabilidades = model.predict_proba(caracteristicas)[0]
        
        # Determinar resultado
        es_potable = prediccion == 1
        prob_potable = probabilidades[1]
        prob_no_potable = probabilidades[0]
        
        # Crear visualización del resultado
        resultado_html = dbc.Container([
            dbc.Row([
                dbc.Col([
                    dbc.Card([
                        dbc.CardBody([
                            html.Div([
                                html.I(
                                    className="fas fa-check-circle" if es_potable else "fas fa-times-circle",
                                    style={
                                        "fontSize": "3rem",
                                        "color": "#28a745" if es_potable else "#dc3545"
                                    }
                                ),
                                html.H3(
                                    "✓ AGUA POTABLE" if es_potable else "✗ AGUA NO POTABLE",
                                    className=f"text-{'success' if es_potable else 'danger'} mt-3 fw-bold"
                                ),
                                html.P(
                                    f"Probabilidad: {(prob_potable*100 if es_potable else prob_no_potable*100):.2f}%",
                                    className="lead mt-2"
                                )
                            ], className="text-center")
                        ])
                    ], className="border-0 shadow", style={"borderRadius": "15px"})
                ], md=6),
                
                dbc.Col([
                    dbc.Card([
                        dbc.CardBody([
                            html.H5("Detalles de Probabilidad", className="mb-3"),
                            dbc.Progress([
                                dbc.Progress(
                                    value=prob_potable*100,
                                    color="success",
                                    bar=True,
                                    label=f"Potable: {prob_potable*100:.2f}%",
                                    className="mb-2"
                                ),
                                dbc.Progress(
                                    value=prob_no_potable*100,
                                    color="danger",
                                    bar=True,
                                    label=f"No Potable: {prob_no_potable*100:.2f}%"
                                )
                            ], multi=True)
                        ])
                    ], className="border-0 shadow", style={"borderRadius": "15px"})
                ], md=6)
            ], className="g-3")
        ], fluid=True, className="mt-4")
        
        return resultado_html
        
    except Exception as e:
        return dbc.Alert(
            f"Error en la predicción: {str(e)}",
            color="danger"
        )

# ==========================================
# 11. CALLBACKS DE GRÁFICOS
# ==========================================

@app.callback(
    Output('grafico-potabilidad', 'figure'),
    Input('nav-eda', 'n_clicks')
)
def actualizar_potabilidad(n_clicks):
    conteos = df['Potability'].value_counts().sort_index()
    total = len(df)
    
    fig = go.Figure(data=[
        go.Bar(
            x=['No Potable', 'Potable'],
            y=conteos.values,
            marker_color=['#8B4513', '#4169E1'],
            text=[f'{count}<br>({100*count/total:.1f}%)' for count in conteos.values],
            textposition='outside',
            hovertemplate='Categoría: %{x}<br>Cantidad: %{y}<extra></extra>'
        )
    ])
    
    fig.update_layout(
        title='Distribución de la Potabilidad del Agua',
        xaxis_title='Potabilidad',
        yaxis_title='Cantidad de muestras',
        showlegend=False,
        template='plotly_white',
        height=400
    )
    
    return fig

@app.callback(
    Output('grafico-correlacion-potabilidad', 'figure'),
    Input('nav-eda', 'n_clicks')
)
def actualizar_correlacion_potabilidad(n_clicks):
    corr_potability = df.corr(numeric_only=True)['Potability'].drop('Potability').sort_values()
    colors_corr = ['firebrick' if x < 0 else 'forestgreen' for x in corr_potability]
    
    fig = go.Figure(data=[
        go.Bar(
            x=corr_potability.values,
            y=corr_potability.index,
            marker_color=colors_corr,
            orientation='h',
            text=[f'{x:.3f}' for x in corr_potability.values],
            textposition='outside',
            hovertemplate='Variable: %{y}<br>Correlación: %{x:.3f}<extra></extra>'
        )
    ])
    
    fig.update_layout(
        title='Correlación de las Variables con la Potabilidad',
        xaxis_title='Correlación',
        yaxis_title='Variables',
        showlegend=False,
        template='plotly_white',
        height=400
    )
    
    return fig

@app.callback(
    Output('grafico-matriz-correlacion', 'figure'),
    Input('nav-eda', 'n_clicks')
)
def actualizar_matriz_correlacion(n_clicks):
    corr_matrix = df.corr(numeric_only=True)
    
    fig = go.Figure(data=go.Heatmap(
        z=corr_matrix.values,
        x=corr_matrix.columns,
        y=corr_matrix.columns,
        colorscale='RdBu_r',
        zmid=0,
        text=[[f'{corr_matrix.iloc[i, j]:.2f}' for j in range(len(corr_matrix.columns))] 
              for i in range(len(corr_matrix.columns))],
        texttemplate='%{text}',
        textfont={"size": 9},
        hovertemplate='X: %{x}<br>Y: %{y}<br>Correlación: %{z:.2f}<extra></extra>'
    ))
    
    fig.update_layout(
        title='Matriz de Correlación',
        template='plotly_white',
        height=600
    )
    
    return fig

# ==========================================
# 12. EJECUTAR APP
# ==========================================
if __name__ == '__main__':
    print("🚀 Iniciando servidor Dash con Bootstrap...")
    print("📱 Abra http://127.0.0.1:8050 en su navegador")
    app.run(debug=True, use_reloader=False)
