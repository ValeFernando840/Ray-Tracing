from email import header
import os
import pandas as pd
import numpy as np

from scipy.interpolate import make_interp_spline
from mpl_toolkits.mplot3d import Axes3D


def generate_dataframe( latitude_position_tx, longitude_position_tx,elevation_position_tx,
  fc,elev,azim,anio,mmdd,UTI,hora,retardo,rango_terrestre,rango_slant,
  lat_final,lon_final,alt_final,latitudes,longitudes,elevations):
    latitudes = latitudes.flatten()
    longitudes = longitudes.flatten()
    elevations = elevations.flatten()

    lat_filt, long_filt, elev_filt = filter_on_elevations(latitudes,longitudes,elevations)
    latitudes ,longitudes,elevations = filter_unique_coordinates(lat_filt,long_filt,elev_filt)
    lat_interp, long_interp, elev_interp = interpolate3d(latitudes,longitudes,elevations)

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
        "final_elevation": alt_final
    }
    #expand arrays in columns sepatare
    for i in range(len(lat_interp)):
      data[f'lat_{i+1}'] = lat_interp[i]
    for i in range(len(long_interp)):
      data[f'long_{i+1}'] = long_interp[i]
    for i in range(len(elev_interp)):
      data[f'elev_{i+1}'] = elev_interp[i]
    df = pd.DataFrame(data)
    # Show Data_Frame
    #print("It is a new DataFrame:\n", df)
    return df
# La funcion agrega al dataset una nueva linea
def add_to_dataset(df):
    address = os.getcwd()
    new = "dataset"
    new_address = os.path.join(address, new)
    df.to_csv(new_address+"/dataset.csv", index=False, header = False, mode = "a")
    return

# La función genera un link con las ubicaciones en el mapa de los 2 puntos
# proporcionados
def coordinates_on_map( initial_latitude, initial_longitude, 
                      final_latitude, final_longitude):
    
    final_latitude = final_latitude[0]
    final_longitude = final_longitude[0]
    url = f"https://www.google.com/maps/dir/?api=1&origin={initial_latitude},{initial_longitude}&destination={final_latitude},{final_longitude}&travelmode=driving"
    print("Open the following URL in your browser:\n", url)
    return

# Esta Función recibirá un conjunto de Lat, Long, y elevs
# y devuelve con conjunto de 100 muestras fijas.
def interpolate3d(latitudes,longitudes,elevations):
  posiciones = np.linspace(0, len(latitudes) - 1, len(latitudes))  # Crear una secuencia de índices para spline
  
  # Crear splines separados para latitudes, longitudes y elevaciones
  spline_lat = make_interp_spline(posiciones, latitudes, k=1)
  spline_lon = make_interp_spline(posiciones, longitudes, k=1)
  spline_elev = make_interp_spline(posiciones, elevations, k=1)
  
  # Generar nuevas posiciones con 100 puntos
  posiciones_nuevas = np.linspace(0, len(latitudes) - 1, 100)
  
  # Generar valores interpolados
  latitudes_int = spline_lat(posiciones_nuevas)
  longitudes_int = spline_lon(posiciones_nuevas)
  elevations_int = spline_elev(posiciones_nuevas)  

  # data ={
  #   "latitudes": latitudes_int,
  #   "longitudes": longitudes_int,
  #   "elevations": elevations_int
  # }
  # df = pd.DataFrame(data)
  # address = os.getcwd()
  # new = "dataset"
  # new_address = os.path.join(address, new)
  # print("Direccion",str(new_address))
  # df.to_csv(new_address+"/coordenadas_interpoladas.csv", index=False, header = True) #mode = "a"  
  return latitudes_int,longitudes_int,elevations_int

# Esta funcion filtra según las elevaciones, si una elevación es NEGATIVA, elimina la tupla
# completa con el fin de no interpolar sobre esas tuplas negativas.
def filter_on_elevations(latitudes,longitudes,elevations):
  lat_filt = []
  long_filt = []
  elev_filt = []

  for i in range(len(elevations)):
    if elevations[i] >= 0:
       lat_filt.append(latitudes[i])
       long_filt.append(longitudes[i])
       elev_filt.append(elevations[i])
  lat_filt = np.array(lat_filt)
  long_filt = np.array(long_filt)  
  elev_filt = np.array(elev_filt)
  
  #Verificar Longitudes
  if len(lat_filt) != len(long_filt) or len(long_filt) != len(elev_filt):
    raise ValueError("Los arrays latitudes, longitudes y elevaciones deben tener la misma longitud")
  # Verificar valores NaN o Inf
  if np.any(np.isnan(lat_filt)) or np.any(np.isnan(long_filt)) or np.any(np.isnan(elev_filt)):
    raise ValueError("Los arrays contienen valores NaN")
  
  if np.any(np.isinf(lat_filt)) or np.any(np.isinf(long_filt)) or np.any(np.isinf(elev_filt)):
    raise ValueError("Los arrays contienen valores infinitos")
  
  return lat_filt, long_filt, elev_filt
# Cuando recibimos la muestra observamos que tenemos muestras repetidas
# Por lo que procedemos a eliminarlas.
def filter_unique_coordinates(latitudes,longitudes,elevations):
  data = {
    'latitudes': latitudes,
    'longitudes': longitudes,
    'elevations': elevations 
  }
  
  df = pd.DataFrame(data)
  # address = os.getcwd()
  # new = "dataset"
  # new_address = os.path.join(address, new)
  # df.to_csv(new_address+"/coordenadas.csv", index=False, header = True) #mode = "a"

  print(df)
  df = df.drop_duplicates()
  print(df)

  latitudes = df['latitudes'].to_numpy()
  longitudes = df['longitudes'].to_numpy()
  elevations = df['elevations'].to_numpy()
  
  return latitudes, longitudes, elevations

# Ésta funcion tengo que ver si continuará o debe ser eliminada...
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

# Ésta función me permite pasar un .csv a .xlsx (formato Excel)
# con el fin de poder visualizar en Excel que es mas ordenado y posee multiples funciones.
def csv_to_excel():
  address = os.getcwd()
  new = "dataset"
  new_address = os.path.join(address, new)
  data = pd.read_csv(new_address+"/dataset.csv")
  print(new_address)
  data.to_excel(new_address+"/dataset_excel.xlsx",index=False)
  return
# csv_to_excel()


  # # ######################
  # address = os.getcwd()
  # new = "dataset"
  # new_address = os.path.join(address, new)
  # df.to_csv(new_address+"/coordenadas.csv", index=False, header = True) #mode = "a"
  # # ######################