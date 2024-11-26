import pandas as pd
import os
from datetime import time, datetime
from collections import Counter

# Nombre del archivo de entrada
pd.set_option('display.max_columns', None)
pd.set_option('display.max_colwidth', None)
archivo_xlsx = 'Indicadores2.xlsx'  # Reemplaza con el nombre de tu archivo .xlsx

directorio = os.path.dirname(os.path.abspath(archivo_xlsx))
hojas = pd.read_excel(archivo_xlsx, sheet_name=None)

lista = []
mayor = []
letra = []
cadenas = []
cadenas2 = []
resultados = []
allActions = []
# Itera sobre cada hoja y guarda en un archivo .csv en el mismo directorio
cont = 0
for nombre_hoja, df in hojas.items():
    nombre_archivo_csv = os.path.join(directorio, f"{nombre_hoja}.csv")
    lista.append(df)
    cont += 1   
    if cont == 4:
        break

valores_unicos = lista[0]['Grupo'].unique()
grupo = valores_unicos.tolist()
print(grupo)
dfGrupo = pd.DataFrame()

for i in range(len(grupo)):
    mayor.append(time(0 , 0, 0))
    cadena = ""
    for j in range(4):
        tiempo = lista[j][lista[j]["Grupo"] == grupo[i]]['time_end'].max()
        valor_unico = lista[j][lista[j]["Grupo"] == grupo[i]]['gender'].unique()[0]
        letra.append(valor_unico[0])
        #print(type(tiempo))
        if mayor[i] < tiempo:
            mayor[i] = lista[j][lista[j]["Grupo"] == grupo[i]]['time_end'].max()
        #print(lista[j].groupby('Grupo')['time_end'].max().reset_index())
        cadena = cadena + valor_unico[0]
    cadenas.append(cadena.upper())

mayor = [time.strftime('%H:%M:%S') for time in mayor]

def time_to_seconds(t):
    """Convierte un objeto datetime.time a segundos."""
    return t.hour * 3600 + t.minute * 60 + t.second

def seconds_to_time(s):
    """Convierte segundos a un objeto datetime.time."""
    return time(hour=s // 3600, minute=(s % 3600) // 60, second=s % 60)

# Define el tiempo inicial y el tiempo final
def update_lists(match, fila, action, match2, fila2, action2, i, tag, pos1, pos2, value):
    match[i] += f'{tag} '
    fila[i] += f'{pos1},{pos2} '
    action[i] += f'{value} '
    match2.append(tag)
    fila2.append(f'{pos1},{pos2}')
    action2.append(value)

def check_and_update(matriz, match, fila, action, match2, fila2, action2, i, j, k, l, m, n, o, p, q):
    checks = [
        ("1,2", matriz[j][0][n], matriz[k][1][o], j, k),
        ("1,3", matriz[j][0][n], matriz[l][2][p], j, l),
        ("1,4", matriz[j][0][n], matriz[m][3][q], j, m),
        ("2,3", matriz[k][1][o], matriz[l][2][p], k, l),
        ("2,4", matriz[k][1][o], matriz[m][3][q], k, m),
        ("3,4", matriz[l][2][p], matriz[m][3][q], l, m)
    ]
    
    for tag, val1, val2, pos1, pos2 in checks:
        if val1 == val2 and val1 != "none":
            if len(fila[i]) == 0 or not any(tag == match2[s] and val1 == action2[s] for s in range(len(match2))):
                update_lists(match, fila, action, match2, fila2, action2, i, tag, pos1, pos2, val1)
def lineas(cantidad):
    match = []
    fila = []
    action = []
    global allActions
    for iii in range(len(matriz)):
      match.append("")
      fila.append("")
      action.append("")
      for jjj in range(len(matriz[iii])):
        #print( matriz[iii][jjj] )
        if isinstance(matriz[iii][jjj], str):
          matriz[iii][jjj] = matriz[iii][jjj].replace(" ", "")
          matriz[iii][jjj] = matriz[iii][jjj].split(",")
        else:
            #print(f"Elemento en matriz[{iii}][{jjj}] ya es una lista: {matriz[iii][jjj]}")
            pass
    for zz in range(cantidad-1):
        if match[zz] == "":
            match[zz] = "N/A"
            action[zz] = "N/A"
    for ii in range(cantidad-1, len(matriz)):
      match2, fila2, action2 = [], [], []
      for jj in range(ii, ii-cantidad, -1):
          for kk in range(ii, ii-cantidad, -1):
              for l in range(ii, ii-cantidad, -1):
                  for m in range(ii, ii-cantidad, -1):
                      for n in range(len(matriz[jj][0])):
                          for o in range(len(matriz[kk][1])):
                              for p in range(len(matriz[l][2])):
                                  for q in range(len(matriz[m][3])):
                                      if any(matriz[x][y][z] == matriz[a][b][c] 
                                            for (x, y, z), (a, b, c) in [
                                                ((jj, 0, n), (kk, 1, o)), ((jj, 0, n), (l, 2, p)), 
                                                ((jj, 0, n), (m, 3, q)), ((kk, 1, o), (l, 2, p)), 
                                                ((kk, 1, o), (m, 3, q)), ((l, 2, p), (m, 3, q))]):
                                          check_and_update(matriz, match, fila, action, match2, fila2, action2, ii, jj, kk, l, m, n, o, p, q)
      if match[ii] == "":
        match[ii] = 0
        action[ii] = "none"
    resultados[var][str(cantidad)+"lineas"]  = match
    #resultados[var]["fila"] = fila
    if cantidad == 3:
      resultados[var]["action"] = action
      allActions = allActions + action

#grupo = ['03C', '06C', '17C', '03D', '06D', '17D']
for var in range(len(grupo)):

#if True:
    #var=2
    tiempo_inicio = time(hour=0, minute=0, second=0)
    tiempo_final = mayor[var]
    tiempo_final = datetime.strptime(tiempo_final, '%H:%M:%S').time()
    incremento = 2  # en segundos

    # Convierte tiempos a segundos
    inicio_segundos = time_to_seconds(tiempo_inicio)
    final_segundos = time_to_seconds(tiempo_final)

    # Crea listas para las columnas
    columna1 = []
    columna2 = []

    # Genera los tiempos para las columnas
    tiempo_actual_segundos = inicio_segundos
    while tiempo_actual_segundos < final_segundos:
        columna1.append(seconds_to_time(tiempo_actual_segundos))
        tiempo_siguiente_segundos = tiempo_actual_segundos + incremento
        if tiempo_siguiente_segundos <= final_segundos:
            columna2.append(seconds_to_time(tiempo_siguiente_segundos))
        else:
            columna2.append(seconds_to_time(final_segundos))  # Ajusta el último valor para que termine en tiempo_final
        tiempo_actual_segundos += incremento

    # Asegúrate de que la última fila tenga los tiempos correctos
    if columna1 and columna2:
        if columna2[-1] != tiempo_final:
            columna2[-1] = tiempo_final

    # Agrega la columna index
    index = list(range(len(columna1)))

        # Crea el DataFrame
    df = pd.DataFrame({
        'index': index,
        'time_start': [str(t) for t in columna1],
        'time_end': [str(t) for t in columna2]
    })

    df['time_start'] = pd.to_datetime(df['time_start'], format='%H:%M:%S').dt.time
    df['time_end'] = pd.to_datetime(df['time_end'], format='%H:%M:%S').dt.time

    tiempo = time(0,0,0)
    columnas = ["speaker1", "speaker2", "speaker3", "speaker4"]
    for i in range(4):
        lista2 = []
        for x in range(len(df)):
            lista2.append("")
        maxi = lista[i][lista[i]["Grupo"] == grupo[var]]["Index"].max()
        for j in range(maxi+1):
            bandera = True
            for k in range(len(df)):
                if bandera and \
                    lista[i][lista[i]["Grupo"] == grupo[var]].iloc[j]['time_start'] >= df.loc[k, "time_start"] and \
                    lista[i][lista[i]["Grupo"] == grupo[var]].iloc[j]['time_start'] < df.loc[k, "time_end"]    :
                    if lista2[k] == "":
                        lista2[k] = lista2[k] + lista[i][lista[i]["Grupo"] == grupo[var]].iloc[j]['action']
                    else:
                        lista2[k] = lista2[k] + ", " + lista[i][lista[i]["Grupo"] == grupo[var]].iloc[j]['action']
                    bandera = False
                    continue
                elif not bandera and lista[i][lista[i]["Grupo"] == grupo[var]].iloc[j]['time_end'] >= df.loc[k, "time_end"] and\
                        lista[i][lista[i]["Grupo"] == grupo[var]].iloc[j]['time_end'] != df.loc[k, "time_start"]:
                    if lista2[k] == "":
                        lista2[k] = lista2[k] + lista[i][lista[i]["Grupo"] == grupo[var]].iloc[j]['action']
                    else:
                        lista2[k] = lista2[k] + ", " + lista[i][lista[i]["Grupo"] == grupo[var]].iloc[j]['action']
                    bandera = False
                    continue
                elif not bandera and lista[i][lista[i]["Grupo"] == grupo[var]].iloc[j]['time_end'] < df.loc[k, "time_end"] and \
                    lista[i][lista[i]["Grupo"] == grupo[var]].iloc[j]['time_end'] > df.loc[k, "time_start"]:
                    if lista2[k] == "":
                        lista2[k] = lista2[k] + lista[i][lista[i]["Grupo"] == grupo[var]].iloc[j]['action']
                    else:
                        lista2[k] = lista2[k] + ", " + lista[i][lista[i]["Grupo"] == grupo[var]].iloc[j]['action']
                    bandera = False
                    continue
        #print("len lista2: ", len(lista2), lista2[0])
        for a in range(len(lista2)):
            if lista2[a] == "":
                lista2[a] = "none"
        df.insert(i+1, columnas[i], lista2)
        #print(i, lista2[i])
    var1 = grupo[var] + "-" + cadenas[var]
    df['Grupo'] = var1
    if var1 not in cadenas2:
        cadenas2.append(var1)
    df = df[['Grupo'] + [col for col in df.columns if col != 'Grupo']]
    def contar_nod_en_columnas(fila):
        return sum(cadena.count('nod') for col, cadena in fila.items() if col in columnas)
    

    # Aplicar la función a cada fila y agregar el resultado como una nueva columna
    df['nod'] = df.apply(contar_nod_en_columnas, axis=1)
    resultados.append(df)
    print("var: ", var, " len resultados: ", len(resultados))
    matriz = resultados[var][columnas].to_numpy()
    print("resultados")
    #print(resultados[i])
    for iiii in range(1, 4):  
      lineas(iiii)
    #lineas(4)

"""with pd.ExcelWriter('dataframes.xlsx') as writer:
    for i in range(len(resultados)):
        resultados[i].to_excel(writer, sheet_name=cadenas[i]+str(i), index=False)"""
face = ["nod", "smile"]

def contar_pares(columna):
    pares_contados = Counter()
    
    for valor in columna:
        if valor != '0':
            pares = str(valor).split()
            pares_contados.update(pares)
    
    return pares_contados



columns_to_adjust = ['speaker1', 'speaker2', "speaker3", "speaker4"]
with pd.ExcelWriter('dataframes5.xlsx') as writer:
    for i in range(len(resultados)):
        resultados[i].to_excel(writer, sheet_name=cadenas2[i], index=False)
        worksheet = writer.sheets[cadenas2[i]]    
      # Aplicamos la función a la columna
        conteo_pares = contar_pares(resultados[i]["1lineas"])
        print(resultados[i]["Grupo"].head(1))
        # Mostramos el resultado
        for par, count in conteo_pares.items():
            print(f"{par}: {count} veces")

elementos_unicos = set(allActions)

# Contar los elementos únicos
cantidad_elementos_unicos = len(elementos_unicos)

print(elementos_unicos)  # Salida: {1, 2, 3, 4, 5, 6}
print(cantidad_elementos_unicos)  # Salida: 6
print(cadenas2)
print("fin")
