import dash
from dash import dcc, html
import plotly.io as pio

# Crear la aplicación Dash
app = dash.Dash(__name__)

# Leer el contenido de los archivos HTML que contienen gráficos interactivos con la codificación utf-8
with open('homogeneos/timeline_duration_18B-MMMM.html', 'r', encoding='utf-8') as f:
    grafico1 = f.read()

with open('intervalos/Group_18A_Timeline.html', 'r', encoding='utf-8') as f:
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
            html.Img(src='/assets/final18B.png', style={'width': '100%', 'height': '100%'})
        ], style={'flex': '0.6', 'padding': '10px', 'border': '1px solid black'})
        
    ], style={'flex': '1', 'display': 'flex', 'height': '30vh'})  # Reduced height for the second section
])

# Ejecutar la aplicación
if __name__ == '__main__':
    app.run_server(debug=True, port=8071)
