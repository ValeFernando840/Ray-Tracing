import pandas as pd




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