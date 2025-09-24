import numpy as np
from simplekml import Kml

def transform_coords_cartesian(lat_ar,lon_ar,height_ar):
  """ Transforma Coordenadas Geograficas a Coordenadas Cartesianas

  Args:
      lat_ar(_array_): _Latitudes de entrada tipo array float_
      lon_ar(_array_): _Longitudes de entrada tipo array float_
      height_arr (_array_): _Alturas de entrada tipo array float_


  Returns:
      x,y,z (_array_): _Retorna un conjunto de coordenadas x,y,z_
  """  
  # phi = np.radians(90-lat_ar)
  phi = np.radians(lat_ar)
  theta = np.radians(lon_ar)
  x = np.array([])
  y = np. array([])
  z = np.array([])
  radio = 6.371E6 #1 [M]
  for phi_i,theta_i, height_i in zip(phi,theta,height_ar):
    h = (height_i + radio)
    x_i = h * np.cos(phi_i) * np.sin(theta_i)
    y_i = h * np.sin(phi_i) * np.sin(theta_i)
    z_i = h * np.cos(theta_i)
    x = np.append(x,x_i)
    y = np.append(y, y_i)
    z = np.append(z,z_i)
  return x,y,z

def transform_cartesian_to_spherical(x,y,z):
  """ Transforma Coordenadas Cartesianas a Coordenadas Esfericas

  Args:
      x(_array_): _x de entrada tipo array float_
      y(_array_): _y de entrada tipo array float_
      z (_array_): _z de entrada tipo array float_


  Returns:
      phi,theta,rho (_array_): _Retorna un conjunto de coordenadas phi,theta,rho_
  """ 
  rho = np.sqrt(x**2+y**2+z**2)
  phi = np.arctan(y/x)
  theta = -np.arctan(np.sqrt(x**2+y**2)/z)
  return phi,theta,rho

def transform_spherical_to_geographic(phi,theta,rho):
  """
  Transforma coordendas esféricas a coordenadas geográficas.
  A la variable de entrada 'rho' se le resta 1 [unit] ya que anteriormente
  en la Transformación a Cartesiana se toma un Radio de 1, con esto se tiene
  exactamente las coordenadas Originales.

  Args:
    phi(_array_): __
    theta(_array_): __
    rho(_array_): __
  Returns:
    latitude,longitude,height: _Retorna el conjunto de coord geográficas
  """
  latitude =  np.degrees(phi)
  longitude = np.degrees(theta)
  height = rho  ## -1 Anteriormente. 
  return latitude,longitude,height

def generate_KML_true_pred(lat_true, lon_true, alt_true,
                 lat_pred,lon_pred,alt_pred, dir,filename):
  """
  Genera un archivo KML para visualizar trayectorias en Google Earth.
  Args:
    lat_true (_array_): _Latitudes de la trayectoria verdadera._
    lon_true (_array_): _Longitudes de la trayectoria verdadera._
    alt_true (_array_): _Alturas de la trayectoria verdadera._
    lat_pred (_array_): _Latitudes de la trayectoria predicha._
    lon_pred (_array_): _Longitudes de la trayectoria predicha._
    alt_pred (_array_): _Alturas de la trayectoria predicha._
    dir (str): _Directorio donde se guardará el archivo KML._
    filename (str): _Nombre del archivo KML (sin extensión)._
  """
  R0 = 6.371E6 # Radio de la Tierra en m
  kml = Kml()
  linestring_true = kml.newlinestring(name = "True")
  linestring_true.coords = list(zip(lon_true, lat_true, alt_true-R0))
  linestring_true.altitudemode = 'absolute'
  linestring_true.extrude = 0
  linestring_true.style.linestyle.width = 5
  linestring_true.style.linestyle.color = 'ff0000ff'

  linestring_pred = kml.newlinestring(name = "Predicted")
  linestring_pred.coords = list(zip(lon_pred, lat_pred, alt_pred - R0))
  linestring_pred.altitudemode = 'absolute'
  linestring_pred.extrude = 0
  linestring_pred.style.linestyle.width = 5
  linestring_pred.style.linestyle.color = 'ff00ff00'

  kml.save(f"{dir}/{filename}.kml")
  return 0

def generate_KML(lat, lon, alt, dir,filename, color = 'ff0000ff'):
  """
  Genera un archivo KML para visualizar trayectoria en Google Earth.
  Args:
    lat (_array_): _Latitudes de la trayectoria ._
    lon (_array_): _Longitudes de la trayectoria ._
    alt (_array_): _Alturas de la trayectoria._
    dir (str): _Directorio donde se guardará el archivo KML._
    filename (str): _Nombre del archivo KML (sin extensión)._
  Note:
  La altura recibida debe ser absoluta es decir sin considerar R0.
  """
  kml = Kml()
  linestring = kml.newlinestring(name = "muestra")
  linestring.coords = list(zip(lon, lat, alt))
  linestring.altitudemode = 'absolute'
  linestring.extrude = 0
  linestring.style.linestyle.width = 5
  linestring.style.linestyle.color = color

  kml.save(f"{dir}/{filename}.kml")
  return 0
"""
NOTA: En KML la biblioteca que usamos (simplekml) se definen en formato AABBGGRR en Hexadecimal
  -AA: Canal ALPHA Transparencia (00= transparente, ff=opaco).
  -BB: Canal Blue.
  -GG: Canal Green.
  -RR: Canal Red
"""
