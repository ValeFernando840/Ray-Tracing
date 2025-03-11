import numpy as np

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
  radio = 1 #6.371E6
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
  """ Transforma Coordenadas Cartesianas a Esfericas

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
  height = rho - 1
  return latitude,longitude,height