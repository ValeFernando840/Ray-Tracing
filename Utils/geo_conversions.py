import numpy as np

def transform_coords_cartesian(lat_ar,lon_ar,height_ar):
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
  rho = np.sqrt(x**2+y**2+z**2)
  phi = np.arctan(y/x)
  theta = -np.arctan(np.sqrt(x**2+y**2)/z)
  return phi,theta,rho