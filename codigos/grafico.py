import matplotlib.pyplot as plt
import pandas as pd

# Datos de la primera tabla: Minoría en grupo
data_minoria = {
    "Actividad": ["01A-MMFF", "01B-MMFF", "07A-MFFF", "07B-MFFF", "14A-MMFM", "14B-MMFM", "16A-MMFM", "16B-MMFM", "17C-FMMM", "17D-FMMM"],
    "C1": ["Sí", "No", "No", "No", "Sí", "Sí", "Sí", "Sí", "Sí", "Sí"],
    "C2": ["Sí", "No", "Sí", "No", "No", "Sí", "Sí", "Sí", "Sí", "Sí"],
    "Resultado": ["Ambos", "Ninguno", "Mimetismo", "Ninguno", "Mimetismo", "Ambos", "Ambos", "Ambos", "Ambos", "Ambos"]
}

# Datos de la segunda tabla: Ambos sexos
data_ambos_sexos = {
    "Actividad": ["06C-FMFM", "06D-FMFM", "12A-MMFF", "12B-MMFF"],
    "C1": ["Sí", "No", "No", "No"],
    "C2": ["Sí", "Sí", "No", "Sí"],
    "Resultado": ["Ambos", "Mimetismo", "Ninguno", "Mimetismo"]
}

# Convertir a DataFrames
df_minoria = pd.DataFrame(data_minoria)
df_ambos_sexos = pd.DataFrame(data_ambos_sexos)

# Gráfico para "Minoría en grupo"
fig, ax = plt.subplots(figsize=(8, 4))
resultados_minoria = df_minoria['Resultado'].value_counts()
resultados_minoria.plot(kind='bar', ax=ax, color='skyblue')
ax.set_title('Resultados - Minoría en Grupo')
ax.set_xlabel('Resultado')
ax.set_ylabel('Número de Actividades')
plt.xticks(rotation=0)

# Gráfico para "Ambos sexos"
fig, ax = plt.subplots(figsize=(8, 4))
resultados_ambos_sexos = df_ambos_sexos['Resultado'].value_counts()
resultados_ambos_sexos.plot(kind='bar', ax=ax, color='salmon')
ax.set_title('Resultados - Ambos Sexos')
ax.set_xlabel('Resultado')
ax.set_ylabel('Número de Actividades')
plt.xticks(rotation=0)

plt.show()
