import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from matplotlib import cm

from scipy.interpolate import griddata, splev, splprep
from mpl_toolkits.mplot3d import Axes3D

def simplified_array(elements):
    new_array = elements.reshape(-1)  ###esto ya no será NECESARIO
    # print("New elements with different structure",new_array)
    return new_array


def generate_dataframe(
    latitude_position_tx,
    longitude_position_tx,
    elevation_position_tx,
    fc,
    elev,
    azim,
    anio,
    mmdd,
    UTI,
    hora,
    retardo,
    rango_terrestre,
    rango_slant,
    lat_final,
    lon_final,
    alt_final,
    latitudes,
    longitudes,
    elevations,
):
    latitudes = simplified_array(latitudes)
    longitudes = simplified_array(longitudes)
    elevations = simplified_array(elevations)
    # TENIENDO LAS LATITUDES LONGITUDES Y ELEVACIONES INTERPOLADAS DEBO GUARDAR ESOS NUEVOS VALORES seguramente el nombre
    # de la funcion tenga que cambiarlo
    expander = len(elevations)  # I can use any (latitudes, longitudes,elevations)
    print("Tamaño", expander)
    latitude_position_tx *= np.ones(expander)
    longitude_position_tx *= np.ones(expander)
    elevation_position_tx *= np.ones(expander)
    fc *= np.ones(expander)
    elev *= np.ones(expander)
    azim *= np.ones(expander)
    anio *= np.ones(expander)
    mmdd = np.full(expander, mmdd)
    UTI *= np.ones(expander)
    hora *= np.ones(expander)
    retardo *= np.ones(expander)
    rango_terrestre *= np.ones(expander)
    rango_slant *= np.ones(expander)
    lat_final = np.full(expander, lat_final)
    lon_final = np.full(expander, lon_final)
    alt_final = np.full(expander, alt_final)

    # Create a Data Frame
    data = {
        "latitude_pos_tx": latitude_position_tx,
        "longitude_pos_tx": longitude_position_tx,
        "elevation_pos_tx": elevation_position_tx,
        "fc": fc,
        "elevation": elev,
        "azimuth": azim,
        "year": anio,
        "mmdd": mmdd,
        "UTI": UTI,
        "hour": hora,
        "delay": retardo,
        "terrestrial_range": rango_terrestre,
        "slant_range": rango_slant,
        "final_latitude": lat_final,
        "final_longitude": lon_final,
        "final_elevation": alt_final,
        "latitudes": latitudes,
        "longitudes": longitudes,
        "elevations": elevations,
    }

    df = pd.DataFrame(data)
    # Show Data_Frame
    print("It is a new DataFrame:\n", df)
    return df


def add_to_dataset(df):
    df.to_csv(
        "C:/Users/Alexis/Desktop/FACULTAD/Ray_Tracing-main/dataset/dataset.csv",
        index=False,
        header=True,
        mode="a",
    )
    return


def coordinates_on_map(
    initial_latitude, initial_longitude, final_latitude, final_longitude
):
    # I want only its value, the initial format is a array
    final_latitude = final_latitude[0]
    final_longitude = final_longitude[0]
    url = f"https://www.google.com/maps/dir/?api=1&origin={initial_latitude},{initial_longitude}&destination={final_latitude},{final_longitude}&travelmode=driving"
    print("Open the following URL in your browser:\n", url)
    return


##Pruebas



df = pd.read_csv("./dataset/dataset.csv")

latitudes = df["latitudes"].to_numpy()  # Obtengo la col lat.. y la paso a numpy
longitudes = df["longitudes"].to_numpy()
elevations = df["elevations"].to_numpy()


def interporlate3d(latitudes,longitudes,elevations):
  tck, u = splprep([latitudes, longitudes, elevations], s=0)
  u_new = np.linspace(0, 1, 100)
  lat_interp, long_interp, elev_interp = splev(u_new, tck)
  print("Latitudes Interp:",lat_interp[:10])
  return lat_interp,long_interp,elev_interp

def convert_geo_coord_to_cartesian_coord(lat,long,elev):
  a = 6378137  # Radio ecuatorial de la Tierra en metros
  e = 0.08181919  # Excentricidad de la Tierra

  lat_rad = np.radians(lat)
  long_rad = np.radians(long)

  # Cálculo del radio en la dirección del primer vertical (N)
  N = a / np.sqrt(1 - e**2 * np.sin(lat_rad)**2)
  
  x = (N + elev) * np.cos(lat_rad) * np.cos(long_rad)
  y = (N + elev) * np.cos(lat_rad) * np.sin(long_rad)
  z = -( (1 - e**2) * N + elev ) * np.sin(lat_rad)

  return x,y,z

a,b,c =  interporlate3d(latitudes,longitudes,elevations)


"""
# Paso 2: Crear una malla regular y realizar interpolación
# Crear la malla regular para latitudes y longitudes
x_grid = np.linspace(min(latitudes_interpoladas), max(latitudes_interpoladas), 10)
y_grid = np.linspace(min(longitudes_interpoladas), max(longitudes_interpoladas), 10)
X, Y = np.meshgrid(x_grid, y_grid)

# Convertir las coordenadas interpoladas en una malla para interpolación
points = np.array([latitudes_interpoladas, longitudes_interpoladas]).T
values = elevaciones_interpoladas
grid_z = griddata(points, values, (X, Y), method='linear')

# Visualización
fig = plt.figure(figsize=(14, 7))
ax = fig.add_subplot(121, projection='3d')
ax.scatter(latitudes, longitudes, elevations, color='r', label='Datos Originales')
#ax.scatter(latitudes_interpoladas, longitudes_interpoladas, elevaciones_interpoladas, color='b', label='Datos Interpolados')
ax.set_xlabel('Latitud')
ax.set_ylabel('Longitud')
ax.set_zlabel('Elevación')
ax.legend()

ax2 = fig.add_subplot(122)
contour = ax2.contourf(X, Y, grid_z, levels=20, cmap='viridis')
fig.colorbar(contour, ax=ax2, label='Elevación')
ax2.set_xlabel('Latitud')
ax2.set_ylabel('Longitud')
ax2.set_title('Interpolación en Malla Regular')

plt.show()

# Imprimir los nuevos valores interpolados
print("Latitudes Interpoladas:", latitudes_interpoladas)
print("Longitudes Interpoladas:", longitudes_interpoladas)
print("Alturas Interpoladas:", elevaciones_interpoladas, len(elevaciones_interpoladas))
"""
