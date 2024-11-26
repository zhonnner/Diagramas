import pandas as pd
import os
from collections import Counter

archivo_xlsx = 'dataframes5.xlsx'  # Reemplaza con el nombre de tu archivo .xlsx

directorio = os.path.dirname(os.path.abspath(archivo_xlsx))
hojas = pd.read_excel(archivo_xlsx, sheet_name=None)
hojas2 = pd.ExcelFile(archivo_xlsx)
# Obtener los nombres de las hojas
nombres_hojas = hojas2.sheet_names
print(nombres_hojas)
lista = []

def contar_pares(columna):
    pares_contados = Counter()
    
    for valor in columna:
        if valor != '0':
            pares = str(valor).split()
            pares_contados.update(pares)
    
    return pares_contados
# Itera sobre cada hoja y guarda en un archivo .csv en el mismo directorio
listaPares = ["1,2", "1,3", "1,4", "2,3", "2,4", "3,4"]

resultados = []

for nombre_hoja, df in hojas.items():
    nombre_archivo_csv = os.path.join(directorio, f"{nombre_hoja}.csv")
    cantidad = [0, 0, 0, 0, 0, 0]
    df2 = pd.DataFrame(listaPares, columns=['pares'])
    for i in range(3):
      conteo_pares = contar_pares(df[str(i+1)+"lineas"])
      print(df["Grupo"].head(1))
    # Mostramos el resultado
      for par, count in conteo_pares.items():
          for j in range(6):
              if par == listaPares[j]:
                  cantidad[j] = cantidad[j] + count
          print(f"{par}: {count} veces")
      df2[str(i+1)+"lineas"] = cantidad
    resultados.append(df2)      
    lista.append(df)

with pd.ExcelWriter('repeticiones.xlsx') as writer:
    for i in range(len(resultados)):
        resultados[i].to_excel(writer, sheet_name=nombres_hojas[i], index=False)