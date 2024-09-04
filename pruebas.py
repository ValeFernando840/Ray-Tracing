import pandas as pd
import numpy as np
import matplotlib.pyplot as plt 
from  scipy.interpolate import interp1d
from scipy.interpolate import splprep, splev
def desfragmentar (data):
  return data["latitudes"], data["longitudes"],data["elevations"]

def transformar_radians(latitudes,longitudes,elevations):
  phi =(np.pi/2) - np.radians(latitudes)
  theta = np.radians(longitudes)
  radio = elevations + 6.371E6
  return phi,theta,radio

def graficar_curvas(phi_or,theta_or,radio_or, ax = None, color = "blue", label = None):
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


  ax.plot(X, Y, (Z - 6.371E6)/1E3, 'o-', label = label, color = color)
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

#Graficamos
# fig = plt.figure()
# ax = fig.add_subplot(projection='3d')
# ax = graficar_curvas(phi_or,theta_or,radio_or, ax=ax, color = "blue", label = "Sin Interpolar")
# ax = graficar_curvas(phi_int,theta_int,radio_int, ax=ax , color = "red", label = "Interpolada")
# plt.show()
##################################
# Realizamos Muestra
# print(data.head())
# print(data_interp.head())
##################################
###Interpolacion en 1d usando iterp1d
def interpolacion_interp1d(elev):
  #tomamos las posiciones, serian los index
  posiciones = np.arange(len(elev))
  nuevas_posiciones = np.linspace(posiciones.min(),posiciones.max(),101)
  # Interpolacion usando interp1d
  interpolacion = interp1d(posiciones, elev, kind='cubic')
  elevaciones_interpoladas = interpolacion(nuevas_posiciones)
  
  plt.plot(posiciones, elev, 'o', label='Datos Originales')
  plt.plot(nuevas_posiciones, elevaciones_interpoladas, '.', label='Interpolación')
  plt.xlabel('Posiciones')
  plt.ylabel('Elevaciones')
  plt.legend()
  plt.show()
  return 0

def interpolacion_splprep(elev):
  posiciones = np.arange(len(elev))
  tck,u = splprep([posiciones,elev], s=0,k=1)
  u_new = np.linspace(0, 1, 101)
  posiciones_int,elevaciones_int = splev(u_new,tck)
  # print(elevaciones_interpoladas, type(elevaciones_interpoladas))
  plt.plot(posiciones, elev, 'o', label='Datos Originales')
  plt.plot(posiciones_int, elevaciones_int, '.', label='Interpolación')
  plt.xlabel('Posiciones')
  plt.ylabel('Elevaciones')
  plt.legend()
  plt.show()
  return 0
# interpolacion_interp1d(elevations)
interpolacion_splprep(elevations)