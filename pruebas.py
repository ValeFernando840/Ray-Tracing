import pandas as pd


# # Agregar primer elemento al archivo csv
# first_element = [1,2,3,4,5,6,7,8,9,10]
# df = pd.DataFrame([first_element])
# # Guardar el DataFrame vacío como un archivo .csv
# df.to_csv('dataset/dataset.csv', index = False, header = True)

# # Agregar de varios elementos sin eliminar elementos
# second_element = [1,2,3,4,5,6,7,8,9]
# df = pd.DataFrame([second_element])
# df.to_csv('dataset/dataset.csv', index = False, header = False, mode = "a")

# third_element = [1,2,3,4,5,6,7,8]
# df = pd.DataFrame([third_element])
# df.to_csv('dataset/dataset.csv', index = False, header = False, mode = "a")

# fourth_element = [1,2,3,4,5,6,7]
# df = pd.DataFrame([fourth_element])
# df.to_csv('dataset/dataset.csv', index = False, header = False, mode = "a")

# # Eliminar una fila del .csv 
# # Eliminamos la fila 2
# df = pd.read_csv('dataset/dataset.csv')
# #Mostramos su contenido
# print(df,"\n")

# index_to_delete = 2 #recordar que el indice comienza desde el 0, 1, 2, ...

# df = df.drop(index_to_delete)

# print("DataFrame:\n\n",df)
# #Tener en cuenta que aquí el header viene del .csv
# # Ahora procedemos a modificar el nuevo DataFrame
# df.to_csv('dataset/dataset.csv', index = False, header = True)



# # Datos de entrada (parámetros iniciales)
# Posicion_Tx_Latitud = [34.05] * 5
# Posicion_Tx_Longitud = [-118.24] * 5
# Posicion_Tx_Altitud = [100] * 5
# fc = [2.4] * 5
# elev = [10] * 5
# azim = [45] * 5
# Anio = [2021] * 5
# mmdd = ['0101'] * 5
# UTI = [12.5] * 5
# Hora = ['12:00'] * 5

# # Datos resultantes
# Latitudes = [34.06, 34.07, 34.08, 34.09, 34.10]
# Longitudes = [-118.25, -118.26, -118.27, -118.28, -118.29]
# Alturas = [110, 120, 130, 140, 150]

# # Crear un DataFrame
# data = {
#   'Posicion_Tx.Latitud': Posicion_Tx_Latitud,
#   'Posicion_Tx.Longitud': Posicion_Tx_Longitud,
#   'Posicion_Tx.Altitud': Posicion_Tx_Altitud,
#   'fc': fc,
#   'elev': elev,
#   'azim': azim,
#   'Anio': Anio,
#   'mmdd': mmdd,
#   'UTI': UTI,
#   'Hora': Hora,
#   'Latitudes': Latitudes,
#   'Longitudes': Longitudes,
#   'Alturas': Alturas
# }
# df = pd.DataFrame(data)

# # Mostrar el DataFrame
# print("DataFrame:")
# print(df)

# # Guardar el DataFrame en un archivo CSV
# output_directory = 'dataset'
# output_file = f'{output_directory}/dataset.csv'

# # Crear la carpeta 'dataset' si no existe
# import os
# if not os.path.exists(output_directory):
#   os.makedirs(output_directory)

# df.to_csv(output_file, index=False)

#recorrer el dataframe de fechas y hacerles print las primeras 50
def read_csv_and_print():
  df = pd.read_csv("dataset/dates2010.csv")
  print(df.head())
  return 
a= read_csv_and_print()