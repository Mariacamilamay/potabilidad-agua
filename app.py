# ============================================================
# app.py
# Archivo principal del dashboard de Rotación Laboral.
# Orquesta los tabs e inicializa la aplicación Dash.
# ============================================================

import sys
import os
import dash
import dash_bootstrap_components as dbc
from dash import html, dcc, Input, Output

# ── Asegura que las carpetas del proyecto sean importables ───
sys.path.insert(0, os.path.dirname(__file__))

# ── Importa el layout de cada pestaña ────────────────────────
from tabs import contextoproblema, metodologia, eda, metricasmodelo, prediccionmodelo


# ── Inicialización de la aplicación ──────────────────────────
app = dash.Dash(
    __name__,
    external_stylesheets=[
        dbc.themes.BOOTSTRAP,
        "https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap",
    ],
    suppress_callback_exceptions=True,
    title="Employee Attrition Dashboard",
)

# Expone el servidor Flask para despliegue con gunicorn
server = app.server


# ── Estilos de la barra de navegación ────────────────────────
NAVBAR_STYLE = {
    "backgroundColor": "#ffffff",
    "boxShadow": "0 2px 8px rgba(0,0,0,0.08)",
    "borderBottom": "3px solid #A0C4FF",
}

# ── Estilos de las pestañas ───────────────────────────────────
TAB_STYLE = {
    "borderRadius": "10px 10px 0 0",
    "padding": "10px 18px",
    "fontWeight": "500",
    "color": "#636e72",
    "border": "none",
    "backgroundColor": "#f8f9fa",
}

TAB_SELECTED_STYLE = {
    **TAB_STYLE,
    "backgroundColor": "#A0C4FF",
    "color": "#2d3436",
    "fontWeight": "700",
    "borderTop": "3px solid #A0C4FF",
}


# ── Barra de navegación superior ─────────────────────────────
navbar = dbc.Navbar(
    dbc.Container([
        html.Div([
            html.Span("🏢", style={"fontSize": "1.8rem", "marginRight": "10px"}),
            html.Div([
                html.H5("Employee Attrition Analytics",
                        className="mb-0 fw-bold", style={"color": "#2d3436"}),
                html.Small("Predicción de Rotación Laboral · ML Dashboard",
                           className="text-muted"),
            ]),
        ], className="d-flex align-items-center"),

        html.Div(
            dbc.Badge(
                "Regresión Logística · Dash · Bootstrap",
                color="light", text_color="secondary",
                className="border fs-6 fw-normal",
            ),
            className="ms-auto d-none d-md-block",
        ),
    ], fluid=True),
    style=NAVBAR_STYLE,
    className="py-2 mb-0",
)


# ── Layout principal ──────────────────────────────────────────
app.layout = html.Div([
    navbar,

    dbc.Container([
        dcc.Tabs(
            id="tabs-principal",
            value="tab-contexto",
            children=[
                dcc.Tab(label="📋 Contexto",    value="tab-contexto",
                        style=TAB_STYLE, selected_style=TAB_SELECTED_STYLE),
                dcc.Tab(label="🔬 Metodología", value="tab-metodologia",
                        style=TAB_STYLE, selected_style=TAB_SELECTED_STYLE),
                dcc.Tab(label="📊 EDA",          value="tab-eda",
                        style=TAB_STYLE, selected_style=TAB_SELECTED_STYLE),
                dcc.Tab(label="📈 Métricas",     value="tab-metricas",
                        style=TAB_STYLE, selected_style=TAB_SELECTED_STYLE),
                dcc.Tab(label="🔮 Predicción",   value="tab-prediccion",
                        style=TAB_STYLE, selected_style=TAB_SELECTED_STYLE),
            ],
            className="mt-3",
            style={"borderBottom": "none"},
        ),

        # Contenedor dinámico donde se renderiza cada pestaña
        html.Div(id="contenido-tab", className="mt-0"),

    ], fluid=True, style={"maxWidth": "1280px"}),

], style={
    "backgroundColor": "#f4f6f9",
    "minHeight": "100vh",
    "fontFamily": "'Inter', sans-serif",
})


# ── Callback: renderiza el contenido según la pestaña activa ──
@app.callback(
    Output("contenido-tab", "children"),
    Input("tabs-principal", "value"),
)
def render_tab(tab: str) -> html.Div:
    """Carga dinámicamente el layout de la pestaña seleccionada."""
    routing = {
        "tab-contexto":    contextoproblema.layout,
        "tab-metodologia": metodologia.layout,
        "tab-eda":         eda.layout,
        "tab-metricas":    metricasmodelo.layout,
        "tab-prediccion":  prediccionmodelo.layout,
    }
    fn = routing.get(tab, contextoproblema.layout)
    return fn()


# ── Punto de entrada ──────────────────────────────────────────
if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=8050)
