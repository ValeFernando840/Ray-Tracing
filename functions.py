from email import header
import os
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


def generate_dataframe( latitude_position_tx, longitude_position_tx,elevation_position_tx,
  fc,elev,azim,anio,mmdd,UTI,hora,retardo,rango_terrestre,rango_slant,
  lat_final,lon_final,alt_final,latitudes,longitudes,elevations):
    latitudes = latitudes.flatten()
    longitudes = longitudes.flatten()
    elevations = elevations.flatten()

    lat_filt, long_filt, elev_filt = filter_on_elevations(latitudes,longitudes,elevations)
    latitudes ,longitudes,elevations = filter_unique_coordinates(lat_filt,long_filt,elev_filt)
    lat_interp, long_interp, elev_interp = interpolate3d(latitudes,longitudes,elevations)
    # print("Tipo de dato(latitudes):" , latitudes, type(latitudes))

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

def add_to_dataset(df):
    address = os.getcwd()
    new = "dataset"
    new_address = os.path.join(address, new)
    print("Directorio:",new_address)
    if os.path.isdir(new_address):
       print("Existe")
    df.to_csv(new_address+"/dataset.csv", index=False, header = False, mode = "a")
    return

def coordinates_on_map( initial_latitude, initial_longitude, 
                      final_latitude, final_longitude):
    # I want only its value, the initial format is a array
    final_latitude = final_latitude[0]
    final_longitude = final_longitude[0]
    url = f"https://www.google.com/maps/dir/?api=1&origin={initial_latitude},{initial_longitude}&destination={final_latitude},{final_longitude}&travelmode=driving"
    print("Open the following URL in your browser:\n", url)
    return


##Pruebas



# df = pd.read_csv("./dataset/dataset.csv")

# latitudes = df["latitudes"].to_numpy()  # Obtengo la col lat.. y la paso a numpy
# longitudes = df["longitudes"].to_numpy()
# elevations = df["elevations"].to_numpy()

def interpolate3d(latitudes,longitudes,elevations):
  # print("Longitudes Recibidas: ",len(latitudes),len(longitudes),len(elevations))
   #Verificar Longitudes
  if len(latitudes) != len(longitudes) or len(longitudes) != len(elevations):
    raise ValueError("Los arrays latitudes, longitudes y elevaciones deben tener la misma longitud")
  # Verificar valores NaN o Inf
  if np.any(np.isnan(latitudes)) or np.any(np.isnan(longitudes)) or np.any(np.isnan(elevations)):
    raise ValueError("Los arrays contienen valores NaN")
  
  if np.any(np.isinf(latitudes)) or np.any(np.isinf(longitudes)) or np.any(np.isinf(elevations)):
    raise ValueError("Los arrays contienen valores infinitos")

  
  tck, u = splprep([latitudes, longitudes, elevations], s=0,k=2)
  u_new = np.linspace(0, 1, 101)
  lat_interp, long_interp, elev_interp = splev(u_new, tck)
  
  # ######################
  data ={
    "latitudes": lat_interp,
    "longitudes": long_interp,
    "elevations": elev_interp
  }
  df = pd.DataFrame(data)
  address = os.getcwd()
  new = "dataset"
  new_address = os.path.join(address, new)
  print("Direccion",str(new_address))
  df.to_csv(new_address+"/coordenadas_interpoladas.csv", index=False, header = True) #mode = "a"
  # ######################
  # print("Latitudes Interpoladas: ",lat_interp)
  # print("Longitudes Interpoladas: ",long_interp)
  print("Elevaciones Interpoladas: ","maximo",max(elev_interp),elev_interp)
  #print("Latitudes Interp:",lat_interp[:10])
  return lat_interp,long_interp,elev_interp

# valor repetidos lat_1: -41.16502671 long_1: -31.86401752 elev_1: 0. (ultimo valor obtenido en filtrados)
# -41.16502671 -31.86401752 0.(penultimo valor obtenido)
def filter_on_elevations(latitudes,longitudes,elevations):
  # print("Latitudes Originales:",latitudes)
  # print("Longitudes Originales:", longitudes)
  print("Elevaciones Originales:",len(elevations),type(elevations),type(latitudes[-1]), elevations)
  
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
  
  # print("Latitudes filtradas:", len(lat_filt) ,type(lat_filt),"Tipo de un elemento:",type(lat_filt[1]),lat_filt)
  # print("Longitudes filtradas:",len(long_filt), long_filt)
  print("Elevaciones filtradas:",len(long_filt), elev_filt)

  return lat_filt, long_filt, elev_filt

def filter_unique_coordinates(latitudes,longitudes,elevations):
  # coordinates = np.vstack((latitudes,longitudes,elevations)).T
  # print("Coordenadas entrantes",coordinates)
  # unique_coordinates = np.unique(coordinates, axis = 0)
  # print("Coordenadas unicas",unique_coordinates)
  # latitudes = unique_coordinates[:,0]
  # longitudes = unique_coordinates[:,1]
  # elevations = unique_coordinates[:,2]
  data = {
    'latitudes': latitudes,
    'longitudes': longitudes,
    'elevations': elevations 
  }
  
  df = pd.DataFrame(data)
  print(df)
  df = df.drop_duplicates()
  print(df)
  # ######################
  address = os.getcwd()
  new = "dataset"
  new_address = os.path.join(address, new)
  df.to_csv(new_address+"/coordenadas.csv", index=False, header = True) #mode = "a"
  # ######################
  latitudes = df['latitudes'].to_numpy()
  longitudes = df['longitudes'].to_numpy()
  elevations = df['elevations'].to_numpy()
  print("elevaciones post quita de duplicados",type(elevations),len(elevations),"maximo",max(elevations),elevations)
  return latitudes, longitudes, elevations

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


def csv_to_excel():
  address = os.getcwd()
  new = "dataset"
  new_address = os.path.join(address, new)
  data = pd.read_csv(new_address+"/dataset.csv")
  print(new_address)
  data.to_excel(new_address+"/dataset_excel.xlsx",index=False)
  return
# csv_to_excel()