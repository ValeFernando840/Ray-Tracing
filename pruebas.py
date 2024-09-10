import pandas as pd
import numpy as np
import os
import matplotlib.pyplot as plt 
from  scipy.interpolate import interp1d
from scipy.interpolate import splprep, splev
from scipy.interpolate import griddata
from scipy.interpolate import PchipInterpolator, RegularGridInterpolator,make_interp_spline



#Recibe un df y los separa en lat lon elevs
def desfragmentar (data):
  return data["latitudes"], data["longitudes"],data["elevations"]

# Pasa la tupla a radianes
def transformar_a_radians(latitudes,longitudes,elevations):
  phi =(np.pi/2) - np.radians(latitudes)
  theta = np.radians(longitudes)
  radio = elevations + 6.371E6
  return phi,theta,radio

def graficar_curvas(phi_or,theta_or,radio_or, ax = None, color = "blue", label = None, marker ='o'):
  if ax is None:
    fig = plt.figure()
    ax = fig.add_subplot(projection='3d')  
  
  # Convertir a arrays numpy y a radianes
  phi_or = np.radians(phi_or) #.to_numpy()
  theta_or = np.radians(theta_or)
  radio_or = radio_or

  # Calcular coordenadas cartesianas
  # phi_or,theta_or = np.meshgrid(phi_or,theta_or)
  X = radio_or * np.cos(phi_or) * np.sin(theta_or)
  Y = radio_or * np.sin(phi_or) * np.sin(theta_or)
  Z = radio_or * np.cos(theta_or)
  
  # Gráfica con puntos en lugar de superficie
  ax.scatter(X, Y, (Z - 6.371E6)/1E3, c=color, marker = marker, label = label)

  # Marca el punto de transmisión
  ax.scatter(X[0], Y[0], (Z[0] - 6.371E6)/1e3, c=color, marker = marker, s=100, label="Tx")
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
phi_or,theta_or,radio_or = transformar_a_radians(latitudes,longitudes,elevations)
phi_int,theta_int,radio_int = transformar_a_radians(latitudes_interp,longitudes_interp,elevations_interp)

#Graficamos
fig = plt.figure()
ax = fig.add_subplot(projection='3d')
ax = graficar_curvas(phi_or,theta_or,radio_or, ax=ax, color = "blue", label = "Sin Interpolar",marker = "o")
ax = graficar_curvas(phi_int,theta_int,radio_int, ax=ax , color = "red", label = "Interpolada", marker = "." )
plt.show()

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
# interpolacion_interp1d(elevations)

# Realiza la Interpolación 1D usando splprep
def interpolacion_splprep(elev):
  posiciones = np.arange(len(elev))
  tck,u = splprep([posiciones,elev], s=0,k=1)
  u_new = np.linspace(0, 1, 100)
  posiciones_int,elevaciones_int = splev(u_new,tck)
  # print(elevaciones_interpoladas, type(elevaciones_interpoladas))
  plt.plot(posiciones, elev, 'o', label='Datos Originales')
  plt.plot(posiciones_int, elevaciones_int, '.', label='Interpolación')
  plt.xlabel('Posiciones')
  plt.ylabel('Elevaciones')
  plt.legend()
  plt.show()
  return 0
# interpolacion_splprep(elevations)

# Interpolacion con Griddata para X,Y,Z
def interpolar_griddata(X,Y,Z):
  X = X.to_numpy()  
  Y = Y.to_numpy()
  Z = Z.to_numpy()
  x_initial = X[0]
  x_end = X[-1]
  y_initial = Y[0]
  y_end = Y[-1]
  numero_muestras=100
  x_new = np.linspace(x_initial,x_end,numero_muestras)
  y_new = np.linspace(y_initial,y_end,numero_muestras)
  z_new = griddata((X,Y),Z,(x_new,y_new),method="linear")

  print(x_new)
  print(y_new)
  print(z_new)
  return x_new,y_new,z_new
# lati_inter,longi_inter,elev_interp = interpolar_griddata(latitudes,longitudes,elevations)
# phi_int,theta_int,radio_int = transformar_radians(lati_inter,longi_inter,elev_interp)
# graficar_curvas(lati_inter,longi_inter,elev_interp  ,ax=None, color = "blue", label = "Interpolada")
# plt.show()

# Ésta funcion es muy buena cuando realizo interpolación 1D para graficas con variaciones oscilantes
# ya que toma mayor puntos donde se produce cambios en la grafica
def interpolacion_pchip(elev):
    posiciones = np.arange(len(elev))
    
    # Crear la interpolación con PchipInterpolator
    f = PchipInterpolator(posiciones, elev)
    
    # Generar nuevas posiciones
    posiciones_int = np.linspace(0, len(elev)-1, 100)
    
    # Obtener los valores interpolados
    elevaciones_int = f(posiciones_int)
    
    # Graficar
    plt.plot(posiciones, elev, 'o', label='Datos Originales')
    plt.plot(posiciones_int, elevaciones_int, '.', label='Interpolación PCHIP')
    plt.xlabel('Posiciones')
    plt.ylabel('Elevaciones')
    plt.legend()
    plt.show()
#interpolacion_pchip(elevations)

## Utilizacion con Griddata
def interpola_elevaciones(latitudes, longitudes, elevaciones):
    # Crear los puntos originales (latitud, longitud) para la interpolación
    latitudes = latitudes.to_numpy() 
    longitudes = longitudes.to_numpy()
    elevaciones = elevaciones.to_numpy()
    print(elevaciones,len(elevaciones))
    # Generar una nueva malla de 100 puntos interpolados
    latitudes_nuevas = np.linspace(latitudes.min(), latitudes.max(), 100)
    longitudes_nuevas = np.linspace(longitudes.min(), longitudes.max(), 100)
    
    # Interpolar las elevaciones en los nuevos puntos
    elevaciones_interpoladas = griddata((latitudes,longitudes), elevaciones, (latitudes_nuevas, longitudes_nuevas), method='linear')


    # Imprimir el conjunto de elevaciones interpoladas
    print("Elevaciones interpoladas:")
    print(elevaciones_interpoladas, len(elevaciones_interpoladas))
    
    return
#interpola_elevaciones(latitudes, longitudes, elevations)


def interpolacion_spline_3d(latitudes, longitudes, elevaciones):
  posiciones = np.linspace(0, len(latitudes) - 1, len(latitudes))  # Crear una secuencia de índices para spline
  
  # Crear splines separados para latitudes, longitudes y elevaciones
  spline_lat = make_interp_spline(posiciones, latitudes, k=3)
  spline_lon = make_interp_spline(posiciones, longitudes, k=3)
  spline_elev = make_interp_spline(posiciones, elevaciones, k=3)
  
  # Generar nuevas posiciones con 100 puntos
  posiciones_nuevas = np.linspace(0, len(latitudes) - 1, 100)
  
  # Generar valores interpolados
  latitudes_int = spline_lat(posiciones_nuevas)
  longitudes_int = spline_lon(posiciones_nuevas)
  elevaciones_int = spline_elev(posiciones_nuevas)
  
  # Graficar la interpolación en 3D
  fig = plt.figure()
  ax = fig.add_subplot(111, projection='3d')
  ax.plot(latitudes_int, longitudes_int, elevaciones_int, label='Trayectoria Interpolada')
  ax.scatter(latitudes, longitudes, elevaciones, color='r', label='Datos Originales')
  ax.set_xlabel('Latitudes')
  ax.set_ylabel('Longitudes')
  ax.set_zlabel('Elevaciones')
  plt.legend()
  plt.show()
  print(elevaciones_int, len(elevaciones_int))
  # ###################### Guardo la interpolación en un csv para graficarlo luego
  data ={
    "latitudes": latitudes_int,
    "longitudes": longitudes_int,
    "elevations": elevaciones_int
  }
  df = pd.DataFrame(data)
  address = os.getcwd()
  new = "dataset"
  new_address = os.path.join(address, new)
  print("Direccion",str(new_address))
  df.to_csv(new_address+"/coordenadas_interpoladas.csv", index=False, header = True) #mode = "a"
# ######################
  return latitudes_int,longitudes_int,elevaciones_int
#lati_inter,longi_inter,elev_interp = interpolacion_spline_3d(latitudes, longitudes, elevations)

