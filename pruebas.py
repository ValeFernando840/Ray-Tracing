import pandas as pd
import numpy as np
import matplotlib.pyplot as plt 



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
# def read_csv_and_print():
#   df = pd.read_csv("dataset/dates2010.csv")
#   print(df.head())
#   return 
# a= read_csv_and_print()
def desfragmentar (data):
  return data["latitudes"], data["longitudes"],data["elevations"]

def transformar_radians(latitudes,longitudes,elevations):
  phi =(np.pi/2) - np.radians(latitudes)
  theta = np.radians(longitudes)
  radio = elevations + 6.371E6
  return phi,theta,radio

def graficar_curvas(phi_or,theta_or,radio_or, ax = None):
  if ax is None:
    fig = plt.figure()
    ax = fig.add_subplot(projection='3d')  
  
  # Convertir a arrays numpy y a radianes
  phi_or = np.radians(phi_or.to_numpy())
  theta_or = np.radians(theta_or.to_numpy())
  radio_or = radio_or.to_numpy()

  # Calcular coordenadas cartesianas
  X = radio_or * np.cos(phi_or) * np.sin(theta_or)
  Y = radio_or * np.sin(phi_or) * np.sin(theta_or)
  Z = radio_or * np.cos(theta_or)


  ax.plot(X, Y, (Z - 6.371E6)/1E3, 'bo-', label="Trayectoria")
  # Gráfica con puntos en lugar de superficie
  # ax.scatter(X, Y, (Z - 6.371E6)/1E3, c='b', marker='o')

  # Marca el punto de transmisión
  ax.scatter(X[0], Y[0], (Z[0] - 6.371E6)/1e3, c='r', marker='o', s=100, label="Tx")
  ax.legend()

  ax.set_zlabel("Altitud (km)")
  ax.set_xlabel("Latitud ($\\degree$)")
  ax.set_ylabel("Longitud ($\\degree$)")
  return ax

# muestra
data = pd.read_csv("dataset/coordenadas.csv")
data_interp = pd.read_csv("dataset/coordenadas_interpoladas.csv")


# Obtenemos las columnas
latitudes,longitudes,elevations = desfragmentar(data) #Se obtienen series
latitudes_interp,longitudes_interp,elevations_interp = desfragmentar(data_interp)

# Transformamos a radians
phi_or,theta_or,radio_or = transformar_radians(latitudes,longitudes,elevations)
phi_int,theta_int,radio_int = transformar_radians(latitudes_interp,longitudes_interp,elevations_interp)

# Graficamos
fig = plt.figure()
ax = fig.add_subplot(projection='3d')

# ax = graficar_curvas(phi_or,theta_or,radio_or, ax=ax)
ax = graficar_curvas(phi_int,theta_int,radio_int, ax=ax )
plt.show()
# muestra
print(data.head())
print(data_interp.head())



