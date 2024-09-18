import numpy as np
import pandas as pd

def generate_sweeps_in_frec_elev_azim():
  frequency = np.arange(3,31,1) * 1e6
  print(frequency)
  elevation_angle = np.arange(0,41,2)
  print(elevation_angle)
  azimuth_angle = np.arange(87,92,1)
  print(azimuth_angle)
  print("Cantidad de Muestras:",len(frequency)*len(elevation_angle)*len(azimuth_angle))

  df = pd.DataFrame(
  [(f, e, a) for f in frequency for e in elevation_angle for a in azimuth_angle],
  columns = ["Frequency","Elevation","Azimuth"])
  #Guardamos el df en un csv
  df.to_csv("dataset/nuevo.csv",index = False, header = True)
  return df

#df = generate_sweeps_in_frec_elev_azim()
data = pd.read_csv("dataset/nuevo.csv")
print(type(data))
for index, row in data.iterrows():
  print (f"Linea {index}, {row["Frequency"]}, {row["Elevation"]}, {row["Azimuth"]}", type(row["Frequency"]), type(row["Elevation"]),type(row["Azimuth"]))