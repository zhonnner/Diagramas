import pandas as pd
import plotly.express as px

# Cargar el archivo Excel con todas las hojas
input_file = 'merged_timeline_results.xlsx'  # Cambia esto con la ruta correcta a tu archivo
sheets = pd.read_excel(input_file, sheet_name=None)  # Carga todas las hojas del archivo Excel

# Mapear los números a los nombres de los speakers
speaker_map = {1: 'speaker 1', 2: 'speaker 2', 3: 'speaker 3', 4: 'speaker 4'}

# Procesar cada hoja individualmente
for sheet_name, df in sheets.items():
    # Mapear la columna 'Number' a los nombres de speakers
    df['Number'] = df['Number'].map(speaker_map)
    
    # Filtrar para asegurarse de que solo estén los speakers 1 a 4
    df = df[df['Number'].isin(['speaker 1', 'speaker 2', 'speaker 3', 'speaker 4'])]
    
    # Convertir las columnas 'Time Start' y 'Time End' a formato de duración (Timedelta)
    df['Time Start'] = pd.to_datetime(df['Time Start'], format='%H:%M:%S')
    df['Time End'] = pd.to_datetime(df['Time End'], format='%H:%M:%S')

    # Crear el gráfico de línea de tiempo con plotly.express para la hoja actual
    fig = px.timeline(
        df, 
        x_start="Time Start", 
        x_end="Time End", 
        y="Number", 
        color="Action", 
        title=f"Timeline Duration Graph - {sheet_name}",
        labels={"Number": "Speaker", "Action": "Action"},
        category_orders={"Number": ['speaker 1', 'speaker 2', 'speaker 3', 'speaker 4']}  # Especificar el orden de los speakers
    )

    # Eliminar la etiqueta de "Speaker" en el eje y
    fig.update_layout(yaxis_title="")

    # Guardar el gráfico como archivo HTML
    fig.write_html(f"timelines/timeline_duration_{sheet_name}.html")

    # Opción para mostrar el gráfico en el navegador si lo deseas también
    # fig.show()
