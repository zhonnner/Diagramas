import pandas as pd
import matplotlib.pyplot as plt
import os

# Cargar los datos desde el archivo Excel
file_path = 'ResultsGPT.xlsx'
data = pd.read_excel(file_path)

# Crear una carpeta para guardar los gráficos
output_folder = 'piecharts'
os.makedirs(output_folder, exist_ok=True)

# Mapear los nombres de los speakers
speaker_mapping = {
    'SPEAKER_00': 'speaker1',
    'SPEAKER_01': 'speaker2',
    'SPEAKER_02': 'speaker3',
    'SPEAKER_03': 'speaker4'
}

# Reemplazar los nombres de los speakers en la columna 'speaker'
data['speaker'] = data['speaker'].map(speaker_mapping)
print(data.dtypes)

# Convertir start_time y end_time a timedelta
data['start_time'] = pd.to_timedelta(data['start_time'].astype(str))
data['end_time'] = pd.to_timedelta(data['end_time'].astype(str))

# Calcular la duración del tiempo hablado
data['duration'] = (data['end_time'] - data['start_time']).dt.total_seconds()

# Renombrar speakers
speaker_mapping = {
    'SPEAKER_00': 'speaker1',
    'SPEAKER_01': 'speaker2',
    'SPEAKER_02': 'speaker3',
    'SPEAKER_03': 'speaker4'
}
data['speaker'] = data['speaker'].replace(speaker_mapping)

# Agrupar por 'Grupo' y 'speaker' y sumar las duraciones
grouped_data = data.groupby(['Grupo', 'speaker'])['duration'].sum().reset_index()

# Función para crear un gráfico de pastel por grupo
def plot_pie_chart(group):
    group_data = grouped_data[grouped_data['Grupo'] == group]
    plt.figure(figsize=(6, 6))
    plt.pie(group_data['duration'], labels=group_data['speaker'], autopct='%1.1f%%', startangle=90)
    plt.title(f'Tiempo hablado por speaker en el grupo {group}')
    plt.axis('equal')  # Para asegurar que el gráfico sea un círculo
    plt.show()

valores_unicos = data['Grupo'].unique()

# Convertir a lista (opcional)
lista_valores_unicos = valores_unicos.tolist()

# Generar gráficos para cada grupo
for group in lista_valores_unicos:
    plot_pie_chart(group)