import numpy as np
from geopy.distance import geodesic
#NOTA:
#   Las variables lat_true_degrees,lon_true_degrees proviene de objetos pandas.Series por lo que se tiene
#   que convertir a un array Numpy.
#   Por otro lado lat_pred_degrees,lon_pred_degrees provienen de objetos array Numpy. Por lo que 
#   no se tiene que transformar.
def haversine_distance(lat_true_degrees,lon_true_degrees,lat_pred_degrees,lon_pred_degrees): #Determinación de Rango Terrestre
  lat_true_degrees = lat_true_degrees.to_numpy()
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
  lat_true = lat_true.to_numpy()
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
  true_heights= true_heights.to_numpy() 
  dif_heights = true_heights - pred_heights

  distance_3d = np.sqrt(distance2D**2 + dif_heights**2)
  return distance_3d 