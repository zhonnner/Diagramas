import dash
from dash import dcc, html
import plotly.io as pio

# Crear la aplicación Dash
app = dash.Dash(__name__)

# Leer el contenido de los archivos HTML que contienen gráficos interactivos con la codificación utf-8
with open('isolados/timeline_duration_01B-MMMF.html', 'r', encoding='utf-8') as f:
    grafico1 = f.read()

with open('intervalos/Group_01B_Timeline.html', 'r', encoding='utf-8') as f:
    grafico2 = f.read()

# Definir el diseño de la aplicación
app.layout = html.Div(style={'display': 'flex', 'flex-direction': 'column', 'height': '100vh'}, children=[
    
    #html.H1('Dashboard de Gráficos Interactivos y Piechart'),

    # Primera sección: Gráfico de línea de tiempo (ocupa más espacio)
    html.Div([
        html.Iframe(srcDoc=grafico1, style={'width': '100%', 'height': '100%'})
    ], style={'flex': '1.1', 'padding': '10px', 'border': '1px solid black'}),  # Increased flex value for bigger size

    # Segunda sección: Gráfico interactivo y PNG, más pequeños (50% de la altura disponible)
    html.Div([
        html.Div([
            html.Iframe(srcDoc=grafico2, style={'width': '100%', 'height': '140%'})
        ], style={'flex': '1', 'padding': '10px', 'border': '1px solid black'}),
        
        html.Div([
            html.H4("Diagrama de cuerdas: Sincronizacion y Tiempo de habla en %", style={'text-align': 'center', 'margin-bottom': '10px'}),
            html.P( ["Sincronizacion intervalos entre speakers:", html.Br(), "1-2: 84, 1-3: 38, 1-4: 38, 2-3: 348, 2-4: 135, 3-4: 127"], 
                style={'text-align': 'center', 'margin-bottom': '10px', 'font-style': 'italic'}),
            html.Img(src='/assets/final01B.png', style={'width': '100%', 'height': '100%','margin': '0 auto',                 'display': 'block', 
                 'margin-left': 'auto', 
                 'margin-right': 'auto'})
        ], style={'flex': '0.6', 'padding': '10px', 'border': '1px solid black'})
        
    ], style={'flex': '1', 'display': 'flex', 'height': '30vh'})  # Reduced height for the second section
])

# Ejecutar la aplicación
if __name__ == '__main__':
    app.run_server(debug=True, port=8041)
