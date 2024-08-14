import pandas as pd 
import numpy as np
import matplotlib.pyplot as plt
from matplotlib import cm

def simplified_array(elements):
    new_array = elements.reshape(-1) ###esto ya no será NECESARIO
    #print("New elements with different structure",new_array)
    return new_array

def generate_dataframe(latitude_position_tx, longitude_position_tx,
        elevation_position_tx,fc, elev, azim, anio, mmdd, UTI, hora,  
        retardo, rango_terrestre, rango_slant, lat_final,lon_final, 
        alt_final, latitudes,longitudes,elevations
        ):
    
    latitudes = simplified_array(latitudes)
    longitudes = simplified_array(longitudes)
    elevations = simplified_array(elevations) 
    #TENIENDO LAS LATITUDES LONGITUDES Y ELEVACIONES INTERPOLADAS DEBO GUARDAR ESOS NUEVOS VALORES seguramente el nombre 
    #de la funcion tenga que cambiarlo
    expander = len(elevations)  # I can use any (latitudes, longitudes,elevations)
    print("Tamaño" , expander)
    latitude_position_tx *= np.ones(expander)
    longitude_position_tx *= np.ones(expander)
    elevation_position_tx *= np.ones(expander)
    fc *= np.ones(expander)
    elev *= np.ones(expander)
    azim *= np.ones(expander)
    anio *= np.ones(expander)
    mmdd = np.full(expander,mmdd)
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
        'latitude_pos_tx' : latitude_position_tx,
        'longitude_pos_tx' : longitude_position_tx,
        'elevation_pos_tx': elevation_position_tx,
        'fc' : fc,
        'elevation' : elev,
        'azimuth' : azim,
        'year' : anio,
        'mmdd' : mmdd,
        'UTI' : UTI,
        'hour' : hora,
        'delay' : retardo,
        'terrestrial_range' : rango_terrestre,
        'slant_range': rango_slant,
        'final_latitude': lat_final,
        'final_longitude': lon_final,
        'final_elevation': alt_final,
        'latitudes': latitudes,
        'longitudes' : longitudes,
        'elevations' : elevations
    }

    df = pd.DataFrame(data)
    # Show Data_Frame
    print("It is a new DataFrame:\n",df)
    return df
def add_to_dataset(df):
    df.to_csv('C:/Users/Alexis/Desktop/FACULTAD/Ray_Tracing-main/dataset/dataset.csv', index = False, header = True, mode = 'a')
    return

def coordinates_on_map(initial_latitude,initial_longitude,final_latitude,final_longitude):
    # I want only its value, the initial format is a array 
    final_latitude = final_latitude[0]
    final_longitude = final_longitude[0]
    url = f"https://www.google.com/maps/dir/?api=1&origin={initial_latitude},{initial_longitude}&destination={final_latitude},{final_longitude}&travelmode=driving"
    print("Open the following URL in your browser:\n",url)
    return

##Pruebas 

import numpy as np
from scipy.interpolate import griddata , splev, splprep
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D

df = pd.read_csv("./dataset/dataset.csv")

latitudes = df['latitudes'].to_numpy() #Obtengo la col lat.. y la paso a numpy 
longitudes = df['longitudes'].to_numpy()
elevations = df['elevations'].to_numpy()

# print("Latitudes originales: ",latitudes)
# print("Longitudes Originales: ",longitudes)
# print("elevaciones originales",elevations)

# Paso 1: Interpolación spline
tck, u = splprep([latitudes, longitudes, elevations], s=0)
u_new = np.linspace(0, 1, 100)
latitudes_interpoladas, longitudes_interpoladas, elevaciones_interpoladas = splev(u_new, tck)


R = 6.371E6  # Radio ecuatorial en metros
# f = 1/298.257223563  # Achatamiento de la Tierra
# e = np.sqrt(f * (2 - f))  # Excentricidad de la Tierra

# # Conversión de grados a radianes
# def deg_to_rad(degrees):
#     return np.deg2rad(degrees)


def geodetic_to_cartesian(latitudes, longitudes, elevaciones):
    latitudes_rad = np.deg2rad(latitudes)
    longitudes_rad = np.deg2rad(longitudes)
    
    x = (R + elevaciones) * np.cos(latitudes_rad) * np.sin(longitudes_rad)
    y = (R + elevaciones) * np.sin(latitudes_rad) * np.sin(longitudes_rad)
    z = (R + elevaciones) * np.cos(latitudes_rad)
    
    return x, y, z

x,y,z = geodetic_to_cartesian(latitudes_interpoladas,longitudes_interpoladas,elevaciones_interpoladas)
print(z[:10])

fig = plt.figure()
ax = fig.add_subplot(projection='3d')
ax.plot_surface(x,y, (z- 6.371E6)/1E3, rstride=1, cstride=1, cmap=cm.jet,
                linewidth=0, antialiased=False)
ax.scatter(x, y, z)

ax.set_xlabel('X')
ax.set_ylabel('Y')
ax.set_zlabel('Z')

plt.show()
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
