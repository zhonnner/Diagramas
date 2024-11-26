import pandas as pd
import holoviews as hv
import networkx as nx
from holoviews import opts

hv.extension('bokeh')

# Cargar todas las hojas del archivo Excel
file_path = 'repeticiones.xlsx'  # Cambia esta ruta por la correcta
excel_data = pd.read_excel(file_path, sheet_name=None)  # Lee todas las hojas

# Definir un mapa de colores para cada speaker
color_mapping = {
    'speaker1': '#1f77b4',  # Azul
    'speaker2': '#ff7f0e',  # Naranja
    'speaker3': '#2ca02c',  # Verde
    'speaker4': '#d62728'   # Rojo
}

# Definir una función para generar el diagrama de cuerdas
def generate_chord_diagram(data, sheet_name):
    # Crear un diccionario para mapear los números de los speakers
    speaker_mapping = {
        '1': 'speaker1',
        '2': 'speaker2',
        '3': 'speaker3',
        '4': 'speaker4'
    }
    
    # Separar los pares y asignar los valores de la columna '3lineas' como pesos
    interaction_matrix = {}
    for _, row in data.iterrows():
        if pd.notnull(row['pares']) and pd.notnull(row['3lineas']):
            pairs = row['pares'].split(',')
            if len(pairs) == 2:
                # Obtener los dos speakers involucrados
                speaker_a = speaker_mapping[pairs[0]]
                speaker_b = speaker_mapping[pairs[1]]
                
                try:
                    # Convertir el valor de '3lineas' a un número
                    weight = float(row['3lineas'])
                    
                    # Solo agregar relaciones con un peso positivo
                    if weight > 0:
                        # Asignar el peso de la interacción entre los speakers
                        if (speaker_a, speaker_b) in interaction_matrix:
                            interaction_matrix[(speaker_a, speaker_b)] += weight
                        elif (speaker_b, speaker_a) in interaction_matrix:
                            interaction_matrix[(speaker_b, speaker_a)] += weight
                        else:
                            interaction_matrix[(speaker_a, speaker_b)] = weight
                except ValueError:
                    # En caso de que '3lineas' no sea un número válido, lo ignoramos
                    continue

    # Crear un grafo con networkx usando los pesos de la columna '3lineas'
    G = nx.Graph()
    for (speaker_a, speaker_b), weight in interaction_matrix.items():
        G.add_edge(speaker_a, speaker_b, weight=weight)
    
    # Agregar colores a los nodos según el color mapping
    for node in G.nodes():
        G.nodes[node]['color'] = color_mapping.get(node, '#333333')  # Color predeterminado si no se encuentra

    # Generar el diagrama de cuerdas con holoviews
    chord = hv.Chord.from_networkx(G, nx.layout.circular_layout(G)).opts(
        opts.Chord(node_color='color', edge_cmap='Category20', labels='name', node_size=20, edge_color='weight')
    )
    
    # Guardar el diagrama como archivo HTML, usando el nombre de la hoja
    hv.save(chord, f'diagrama_cuerdas_{sheet_name}.html', backend='bokeh')
    return chord

# Generar un diagrama de cuerdas para cada hoja en el archivo Excel
for sheet_name, data in excel_data.items():
    print(f'Generando diagrama para la hoja: {sheet_name}')
    generate_chord_diagram(data, sheet_name)
