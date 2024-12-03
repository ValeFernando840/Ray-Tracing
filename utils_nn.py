import numpy as np
import pandas as pd
from geopy.distance import geodesic
import os
#NOTA:
#   Las variables lat_true_degrees,lon_true_degrees proviene de objetos pandas.Series por lo que se tiene
#   que convertir a un array Numpy.
#   Por otro lado lat_pred_degrees,lon_pred_degrees provienen de objetos array Numpy. Por lo que 
#   no se tiene que transformar.
def haversine_distance(lat_true_degrees,lon_true_degrees,lat_pred_degrees,lon_pred_degrees): #Determinación de Rango Terrestre
  if isinstance(lat_true_degrees, pd.Series):
    lat_true_degrees = lat_true_degrees.to_numpy()
  if isinstance(lon_true_degrees, pd.Series):
    lon_true_degrees = lon_true_degrees.to_numpy()

  lat_true = np.radians(lat_true_degrees)
  lon_true = np.radians(lon_true_degrees)
  lat_pred = np.radians(lat_pred_degrees)
  lon_pred = np.radians(lon_pred_degrees)    
  
  Re = 6371e3 # Radio de la tierra (m)
  aux = (np.sin((lat_pred-lat_true)/2))**2 + np.cos(lat_true)*np.cos(lat_pred)*(np.sin((lon_pred-lon_true)/2))**2 
  Range = 2 * Re * np.arcsin(np.sqrt(aux))/1000 #Km
  return Range

# Calculo de Distancias usando biblioteca Geodesic
def distances_by_geodesic(lat_true,lon_true,lat_pred,lon_pred):
  if isinstance(lat_true, pd.DataFrame):
    lat_true = lat_true.to_numpy()
  if isinstance(lon_true, pd.DataFrame):
    lon_true = lon_true.to_numpy()

  errors = np.array([])

  for lat_t,lon_t,lat_p,lon_p in zip(lat_true,lon_true,lat_pred,lon_pred):
    real_coord = (lat_t,lon_t)
    predict_coord = (lat_p,lon_p)

    distance = geodesic(real_coord,predict_coord).kilometers
    errors = np.append(errors,distance)
  return errors

# ====Calculo de distancias en 3D====
# Las alturas true and pred estan en km RECORDAR. Ver que el input distance2D 
# tiene que estar en la misma unidad.
# Tener en cuenta que true_heights es tipo Serie por lo que transformamos a array numpy.
def distances_3D(distance2D, true_heights, pred_heights):
  if isinstance(true_heights,pd.Series) or isinstance(true_heights,pd.DataFrame):
    true_heights= true_heights.to_numpy() 
  dif_heights = true_heights - pred_heights

  distance_3d = np.sqrt(distance2D**2 + dif_heights**2)
  return distance_3d 
def ecm_recm(distances):
  ecm = np.sum(distances**2)/len(distances)
  recm = np.sqrt(ecm)
  return ecm,recm

def generate_df(distancias_2d,error_2d,distancias_3d,error_3d):
  dist2D_columns = [f'dist2D_{i}' for i in range(1,101)]
  dist3D_columns = [f'dist3D_{i}' for i in range(1,101)]
  error_dist2D = ["ECM_2D","R-ECM_2D"]
  error_dist3D = ["ECM_3D","R-ECM_3D"]

  df_2d = pd.DataFrame(distancias_2d, columns = [dist2D_columns])
  df_error_dist2D = pd.DataFrame(error_2d, columns = [error_dist2D])
  df_3d = pd.DataFrame(distancias_3d, columns = [dist3D_columns])
  df_error_dist3D = pd.DataFrame(error_3d, columns = [error_dist3D])

  new_df = pd.concat([df_2d,df_error_dist2D,df_3d,df_error_dist3D],axis=1)
  return new_df

def save_file_error(new_df,dir,sheet_name):
  if not os.path.exists(f'Errores/{dir}.xlsx'):
    new_df.to_excel(f'Errores/{dir}.xlsx', index=False, sheet_name=sheet_name)
  else:
    with pd.ExcelWriter(f'Errores/{dir}.xlsx', mode='a',engine='openpyxl') as writer:
      new_df.to_excel(writer, sheet_name=sheet_name, index = False)
  