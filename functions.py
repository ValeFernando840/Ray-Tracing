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



# df = pd.read_csv("./dataset/dataset.csv")

# latitudes = df["latitudes"].to_numpy()  # Obtengo la col lat.. y la paso a numpy
# longitudes = df["longitudes"].to_numpy()
# elevations = df["elevations"].to_numpy()


def interpolate3d(latitudes,longitudes,elevations):
  print("elevaciones sin Interpolar: ",elevations)
 
  tck, u = splprep([latitudes, longitudes, elevations], s=0)
  u_new = np.linspace(0, 1, 100)
  lat_interp, long_interp, elev_interp = splev(u_new, tck)
  print("Elevaciones Interpoladas: ",elev_interp)
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


def csv_to_excel():
  address = os.getcwd()
  new = "dataset"
  new_address = os.path.join(address, new)
  data = pd.read_csv(new_address+"/dataset.csv")
  print(new_address)
  data.to_excel(new_address+"/dataset_excel.xlsx",index=False)
  return
# csv_to_excel()