import dash
from dash import dcc, html, Input, Output, dash_table, callback_context
import plotly.express as px
import plotly.graph_objects as go
import pandas as pd
import dash_bootstrap_components as dbc
from pathlib import Path
import os

# ==========================================
# 1. CARGA DE DATOS
# ==========================================
data_path = Path(__file__).parent / 'data' / 'water_potability.csv'

try:
    df = pd.read_csv(data_path)
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
# 2. INICIALIZAR APP
# ==========================================
app = dash.Dash(__name__,
                external_stylesheets=[dbc.themes.BOOTSTRAP,
                                     "https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.4.0/css/all.min.css"],
                assets_folder='assets')
app.config.suppress_callback_exceptions = True
server = app.server

# ==========================================
# 3. COMPONENTES REUTILIZABLES
# ==========================================

def create_card(title, content, color='primary', icon=None):
    return dbc.Card([
        dbc.CardHeader([
            html.H4(title, className="mb-0", style={"color": "white"}),
        ], style={"backgroundColor": f"var(--bs-{color})", "borderRadius": "10px 10px 0 0"}),
        dbc.CardBody(content, style={"padding": "25px"})
    ], className="mb-4 shadow-sm", style={"borderRadius": "10px", "border": "none"})

def create_stat_card(title, value, subtitle, icon, color='primary'):
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
    ], md=3, className='mb-4')

# ==========================================
# 4. TEXTOS DEL CONTENIDO
# ==========================================

intro_text_1 = (
    "La calidad del agua es un factor esencial para la salud y el bienestar de las personas. "
    "Evaluar si el agua es apta para el consumo humano requiere analizar diversas "
    "características fisicoquímicas que influyen en su potabilidad."
)

intro_text_2 = (
    "En este proyecto se realiza un análisis exploratorio de datos sobre muestras de agua "
    "con el fin de identificar patrones y relaciones entre las variables. Posteriormente, "
    "se aplicarán técnicas de aprendizaje automático para desarrollar un modelo capaz de "
    "predecir si una muestra de agua es potable o no a partir de sus características."
)

problema_text = (
    "La calidad del agua es un aspecto fundamental para la salud humana, ya que el consumo "
    "de agua contaminada puede generar diversas enfermedades y afectar la calidad de vida "
    "de la población."
)

objetivo_general_text = (
    "Desarrollar un modelo de aprendizaje automático que permita predecir la potabilidad "
    "del agua a partir de sus características fisicoquímicas."
)

alert_carga = (
    "Se carga el conjunto de datos de potabilidad del agua en un DataFrame de Pandas. "
    "Posteriormente, se visualizan las primeras filas con el fin de verificar que la "
    "información haya sido importada correctamente."
)

alert_stats = (
    "Las estadísticas descriptivas permiten conocer el comportamiento general de las "
    "variables numéricas. Se observa que las características presentan diferentes rangos "
    "y niveles de dispersión."
)

alert_potab = (
    "La variable Potability presenta dos categorías: agua no potable y agua potable. "
    "Se observa un desbalance moderado entre las clases."
)

alert_corr = (
    "Ninguna variable presenta una correlación lineal fuerte con la potabilidad. "
    "Las correlaciones son muy bajas y cercanas a cero."
)

alert_matriz = (
    "La matriz de correlación permite visualizar las relaciones lineales entre todas "
    "las variables."
)

# ==========================================
# 5. SECCIONES DE CONTENIDO
# ==========================================

navbar = dbc.NavbarSimple(
    children=[
        dbc.NavItem(dbc.NavLink("📋 Introducción", href="#", id="nav-intro", active=True)),
        dbc.NavItem(dbc.NavLink("🎯 Problema", href="#", id="nav-problema")),
        dbc.NavItem(dbc.NavLink(" Objetivos", href="#", id="nav-objetivos")),
        dbc.NavItem(dbc.NavLink("💡 Justificación", href="#", id="nav-justificacion")),
        dbc.NavItem(dbc.NavLink("📊 Análisis EDA", href="#", id="nav-eda")),
    ],
    brand="🌊 Potabilidad del Agua",
    brand_href="#",
    color="primary",
    dark=True,
    sticky="top",
    className="shadow-sm"
)

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

intro_section = dbc.Container([
    create_card("1. Introducción", [
        html.P(intro_text_1, className="lead"),
        html.P(intro_text_2)
    ], color="primary")
], className="py-4")

problema_section = dbc.Container([
    create_card("2. Planteamiento del Problema", [
        html.P(problema_text, className="mb-3"),
        dbc.Alert([
            html.H4("Pregunta de Investigación", className="alert-heading"),
            html.P("¿Es posible predecir la potabilidad del agua a partir de sus características fisicoquímicas mediante el uso de modelos de aprendizaje automático?", className="mb-0")
        ], color="warning", className="mt-4")
    ], color="danger")
], className="py-4")

objetivos_section = dbc.Container([
    create_card("3. Objetivos", [
        dbc.Row([
            dbc.Col([
                dbc.Card([
                    dbc.CardHeader(html.H5("Objetivo General", className="text-white mb-0")),
                    dbc.CardBody([
                        html.P(objetivo_general_text, className="mb-0")
                    ])
                ], className="border-0 shadow-sm mb-4")
            ])
        ]),
        html.H5("Objetivos Específicos", className="mb-3"),
        dbc.ListGroup([
            dbc.ListGroupItem("📊 Realizar un análisis exploratorio de los datos", className="d-flex align-items-center"),
            dbc.ListGroupItem("🔍 Identificar las variables con mayor influencia", className="d-flex align-items-center"),
            dbc.ListGroupItem("⚙️ Preparar y transformar los datos", className="d-flex align-items-center"),
            dbc.ListGroupItem("🤖 Entrenar y evaluar modelos de clasificación", className="d-flex align-items-center"),
            dbc.ListGroupItem("📈 Comparar el desempeño de los modelos", className="d-flex align-items-center"),
        ], flush=True, className="mb-3")
    ], color="success")
], className="py-4")

justificacion_section = dbc.Container([
    create_card("4. Justificación", [
        dbc.Row([
            dbc.Col([
                html.Div([
                    html.I(className="fas fa-tint", style={"fontSize": "3rem", "color": "#0d6efd"}),
                    html.H5("Importancia para la Salud", className="mt-3"),
                    html.P("El acceso a agua potable es fundamental para la salud y la calidad de vida de la población.")
                ], className="text-center p-3")
            ], md=6),
            dbc.Col([
                html.Div([
                    html.I(className="fas fa-chart-line", style={"fontSize": "3rem", "color": "#198754"}),
                    html.H5("Ciencia de Datos", className="mt-3"),
                    html.P("Aplicación de técnicas de análisis de datos y aprendizaje automático para la evaluación de calidad.")
                ], className="text-center p-3")
            ], md=6)
        ])
    ], color="info")
], className="py-4")

eda_section = dbc.Container([
    dbc.Row([
        create_stat_card("Total de Muestras", f"{len(df):,}", "Registros analizados", "fa-database", "primary"),
        create_stat_card("Variables", f"{len(df.columns)}", "Características fisicoquímicas", "fa-sliders-h", "success"),
        create_stat_card("Agua Potable", f"{df['Potability'].sum():,}", f"{100*df['Potability'].mean():.1f}% del total", "fa-check-circle", "success"),
        create_stat_card("Agua No Potable", f"{len(df) - df['Potability'].sum():,}", f"{100*(1-df['Potability'].mean()):.1f}% del total", "fa-times-circle", "danger"),
    ], className="mb-4"),

    dbc.Row([
        dbc.Col([
            create_card("6.2 Cargue Inicial de los Datos", [
                html.P("Vista previa de las primeras 5 filas del dataset:", className="mb-3"),
                dbc.Table.from_dataframe(df.head(5), striped=True, bordered=True, hover=True, responsive=True),
                dbc.Alert(alert_carga, color="info", className="mt-3")
            ], color="secondary")
        ])
    ], className="mb-4"),

    dbc.Row([
        dbc.Col([
            create_card("6.3 Información General del Dataset", [
                dbc.Row([
                    dbc.Col(html.H6(f"Total de registros: {len(df)}", className="text-primary"), md=6),
                    dbc.Col(html.H6(f"Total de columnas: {len(df.columns)}", className="text-success"), md=6),
                ], className="mb-3"),
                html.P("Detalle de tipos de datos y valores no nulos:", className="mb-3"),
                dbc.Table([
                    html.Thead(html.Tr([html.Th("Columna"), html.Th("Tipo"), html.Th("No-Nulos"), html.Th("Nulos")])),
                    html.Tbody([
                        html.Tr([
                            html.Td(col),
                            html.Td(str(df[col].dtype)),
                            html.Td(df[col].notna().sum()),
                            html.Td(df[col].isna().sum())
                        ]) for col in df.columns
                    ])
                ], striped=True, responsive=True),
            ], color="info")
        ])
    ], className="mb-4"),

    dbc.Row([
        dbc.Col([
            create_card("6.4 Estadísticas Descriptivas", [
                dbc.Table.from_dataframe(
                    df.describe().round(2).T.reset_index().rename(columns={'index': 'Variable'}),
                    striped=True, bordered=True, hover=True, responsive=True
                ),
                dbc.Alert(alert_stats, color="info", className="mt-3")
            ], color="warning")
        ])
    ], className="mb-4"),

    dbc.Row([
        dbc.Col([
            create_card("6.5 Distribución de la Variable Objetivo", [
                dcc.Graph(id='grafico-potabilidad'),
                dbc.Alert(alert_potab, color="info", className="mt-3")
            ], color="primary")
        ])
    ], className="mb-4"),

    dbc.Row([
        dbc.Col([
            create_card("6.6 Correlación con la Potabilidad", [
                dcc.Graph(id='grafico-correlacion-potabilidad'),
                dbc.Alert(alert_corr, color="warning", className="mt-3")
            ], color="secondary")
        ])
    ], className="mb-4"),

    dbc.Row([
        dbc.Col([
            create_card("6.7 Matriz de Correlación Completa", [
                dcc.Graph(id='grafico-matriz-correlacion'),
                dbc.Alert(alert_matriz, color="info", className="mt-3")
            ], color="dark")
        ])
    ], className="mb-4"),

    dbc.Row([
        dbc.Col([
            create_card("🔍 Visualizaciones Interactivas", [
                dbc.Row([
                    dbc.Col([
                        html.Label("Variable para Histograma:", className="fw-bold"),
                        dcc.Dropdown(
                            id='dropdown-histograma',
                            options=[{'label': col, 'value': col} for col in df.columns if col != 'Potability'],
                            value='ph',
                            clearable=False,
                            className="mb-3"
                        )
                    ], md=6),
                    dbc.Col([
                        html.Label("Tipo de Gráfico:", className="fw-bold"),
                        dcc.Dropdown(
                            id='dropdown-tipo-grafico',
                            options=[
                                {'label': '📊 Histograma', 'value': 'histogram'},
                                {'label': '📦 Box Plot', 'value': 'box'},
                                {'label': '🎻 Violin Plot', 'value': 'violin'}
                            ],
                            value='histogram',
                            clearable=False,
                            className="mb-3"
                        )
                    ], md=6)
                ]),
                dcc.Graph(id='grafico-interactivo', className='mb-4'),

                dbc.Row([
                    dbc.Col([
                        html.Label("Variable Eje X:", className="fw-bold"),
                        dcc.Dropdown(
                            id='dropdown-x',
                            options=[{'label': col, 'value': col} for col in df.columns if col != 'Potability'],
                            value='ph',
                            clearable=False,
                            className="mb-3"
                        )
                    ], md=4),
                    dbc.Col([
                        html.Label("Variable Eje Y:", className="fw-bold"),
                        dcc.Dropdown(
                            id='dropdown-y',
                            options=[{'label': col, 'value': col} for col in df.columns if col != 'Potability'],
                            value='Chloramines',
                            clearable=False,
                            className="mb-3"
                        )
                    ], md=4),
                    dbc.Col([
                        html.Label("Tipo de Scatter:", className="fw-bold"),
                        dcc.Dropdown(
                            id='dropdown-scatter-type',
                            options=[
                                {'label': '⚪ Scatter Simple', 'value': 'scatter'},
                                {'label': '📈 Con Línea de Tendencia', 'value': 'scatter+trend'}
                            ],
                            value='scatter',
                            clearable=False,
                            className="mb-3"
                        )
                    ], md=4)
                ]),
                dcc.Graph(id='grafico-scatter-interactivo')
            ], color="primary")
        ])
    ], className="mb-4")
])

footer = dbc.Container([
    html.Hr(className="my-4"),
    dbc.Row([
        dbc.Col([
            html.P("© 2024 Predicción de la Potabilidad del Agua", className="text-muted mb-0"),
            html.P("By Maria May, Andrea Padilla, Alberto Jimenez, Winston Pardo", className="text-muted mb-0")
        ], className="text-center")
    ])
], className="mt-5")

# ==========================================
# 6. LAYOUT PRINCIPAL
# ==========================================
app.layout = html.Div([
    navbar,
    hero_section,
    html.Div(id='page-content', className='pb-5'),
    footer
], style={"backgroundColor": "#f8f9fa", "minHeight": "100vh"})

# ==========================================
# 7. CALLBACKS
# ==========================================

@app.callback(
    Output('page-content', 'children'),
    [Input('nav-intro', 'n_clicks'),
     Input('nav-problema', 'n_clicks'),
     Input('nav-objetivos', 'n_clicks'),
     Input('nav-justificacion', 'n_clicks'),
     Input('nav-eda', 'n_clicks'),
     Input('btn-ver-analisis', 'n_clicks')],
    prevent_initial_call=False
)
def display_page(n_intro, n_problema, n_objetivos, n_justificacion, n_eda, n_btn):
    ctx = callback_context
    if not ctx.triggered:
        return intro_section
    button_id = ctx.triggered[0]['prop_id'].split('.')[0]
    if button_id == 'nav-problema' or button_id == 'btn-ver-analisis':
        return problema_section
    elif button_id == 'nav-objetivos':
        return objetivos_section
    elif button_id == 'nav-justificacion':
        return justificacion_section
    elif button_id == 'nav-eda':
        return eda_section
    else:
        return intro_section

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

@app.callback(
    Output('grafico-interactivo', 'figure'),
    [Input('dropdown-histograma', 'value'),
     Input('dropdown-tipo-grafico', 'value')]
)
def actualizar_grafico_interactivo(variable, tipo_grafico):
    try:
        if tipo_grafico == 'histogram':
            fig = px.histogram(df, x=variable, color='Potability',
                              marginal='box',
                              title=f'Distribución de {variable} según Potabilidad',
                              color_discrete_map={0: '#8B4513', 1: '#4169E1'},
                              barmode='overlay',
                              opacity=0.7)
        elif tipo_grafico == 'box':
            fig = px.box(df, x='Potability', y=variable,
                        title=f'Distribución de {variable} por Potabilidad',
                        color='Potability',
                        color_discrete_map={0: '#8B4513', 1: '#4169E1'},
                        points='outliers')
            fig.update_xaxes(tickvals=[0, 1], ticktext=['No Potable', 'Potable'])
        else:
            fig = px.violin(df, x='Potability', y=variable,
                           title=f'Distribución de {variable} por Potabilidad',
                           color='Potability',
                           color_discrete_map={0: '#8B4513', 1: '#4169E1'},
                           box=True, points='outliers')
            fig.update_xaxes(tickvals=[0, 1], ticktext=['No Potable', 'Potable'])
        fig.update_layout(template='plotly_white', height=500, showlegend=True)
        return fig
    except Exception as e:
        print(f"Error en gráfico interactivo: {e}")
        import traceback
        traceback.print_exc()
        return go.Figure()

@app.callback(
    Output('grafico-scatter-interactivo', 'figure'),
    [Input('dropdown-x', 'value'),
     Input('dropdown-y', 'value'),
     Input('dropdown-scatter-type', 'value')]
)
def actualizar_scatter(col_x, col_y, tipo):
    try:
        df_clean = df[[col_x, col_y, 'Potability']].dropna()
        if tipo == 'scatter+trend':
            fig = px.scatter(df_clean, x=col_x, y=col_y, color='Potability',
                            trendline='ols',
                            title=f'Relación entre {col_x} y {col_y} (con tendencia)',
                            color_discrete_map={0: '#8B4513', 1: '#4169E1'},
                            opacity=0.6,
                            trendline_color_override='red')
        else:
            fig = px.scatter(df_clean, x=col_x, y=col_y, color='Potability',
                            title=f'Relación entre {col_x} y {col_y}',
                            color_discrete_map={0: '#8B4513', 1: '#4169E1'},
                            opacity=0.6)
        fig.update_layout(template='plotly_white', height=500)
        return fig
    except Exception as e:
        print(f"Error en scatter: {e}")
        import traceback
        traceback.print_exc()
        fig = go.Figure()
        fig.add_annotation(text=f"Error: {str(e)}", xref="paper", yref="paper",
                          x=0.5, y=0.5, showarrow=False, font=dict(size=14, color='red'))
        return fig

# ==========================================
# 8. EJECUTAR APP
# ==========================================
if __name__ == '__main__':
    print(" Iniciando servidor Dash con Bootstrap...")
    print(" Abra http://127.0.0.1:8050 en su navegador")
    app.run(debug=True, use_reloader=False)