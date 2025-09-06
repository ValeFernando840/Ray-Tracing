#Bibliotecas 
import pandas as pd
import numpy as np
import ast
import matplotlib.pyplot as plt
from scipy.interpolate import CubicSpline
from scipy.interpolate import make_interp_spline
from scipy.interpolate import griddata


df = pd.read_excel("prueba04-09.xlsx")

idx = 3 # Index 0 a 3
strng_lat = df["latitudes"].iloc[idx] ; latitudes = np.fromstring(strng_lat.strip("[]"), sep=" ")
strng_lon = df["longitudes"].iloc[idx] ; longitudes = np.fromstring(strng_lon.strip("[]"), sep=" ")
strng_alt = df["alturas"].iloc[idx] ; altitudes = np.fromstring(strng_alt.strip("[]"), sep=" ")

def transfor_to_cartesian(latitudes, longitudes, altitudes):
		"""
		Transforma coordenadas esféricas (latitud, longitud, altura) a coordenadas cartesianas (x, y, z).
		Parámetros:
		latitudes : array-like
			Array de latitudes en grados.
		longitudes : array-like
			Array de longitudes en grados.
		altitudes : array-like
			Array de alturas en metros.	
		Retorna:
		x : array-like
			Coordenada x en metros.
		y : array-like
			Coordenada y en metros.
		z : array-like
			Coordenada z en metros.
		"""
		R_earth = 6.371E6 # Radio de la Tierra en m
		phi = np.radians(latitudes)
		theta = np.radians(longitudes)
		r = R_earth + altitudes
		x = r * np.cos(phi) * np.sin(theta)
		y = r * np.sin(phi) * np.sin(theta)
		z = r * np.cos(phi)
		return x, y, z
def interpolate_with_spline(x,y,z):
	"""
  Interpola puntos 3D utilizando splines."""
	pos = np.linspace(0, len(x) - 1, len(x))
	spline_x = make_interp_spline(pos, x, k=3)  # 
	spline_y = make_interp_spline(pos, y, k=3)
	spline_z = make_interp_spline(pos, z, k=3)
	new_pos = np.linspace(0, len(x) - 1, 200) # nuevos indices
	x_interp = spline_x(new_pos)
	y_interp = spline_y(new_pos)
	z_interp = spline_z(new_pos)
	return x_interp, y_interp, z_interp
def interpolate_with_griddata(x,y,z):
  """
  Interpola puntos 3D utilizando griddata."""
  # Crear una cuadrícula regular en el espacio 3D
  num_points = 200
  xi = np.linspace(np.min(x), np.max(x), num_points)
  yi = np.linspace(np.min(y), np.max(y), num_points)
  zi = np.linspace(np.min(z), np.max(z), num_points)
  XI, YI, ZI = np.meshgrid(xi, yi, zi)
  # Interpolar los datos originales en la cuadrícula
  points = np.vstack((x, y, z)).T
  values = np.zeros(len(x))  # Valores ficticios para la interpolación
  grid_z = griddata(points, values, (XI, YI, ZI), method='linear')
  # Extraer los puntos interpolados no nulos
  x_interp = XI[~np.isnan(grid_z)]
  y_interp = YI[~np.isnan(grid_z)]
  z_interp = ZI[~np.isnan(grid_z)]
  return x_interp, y_interp, z_interp
x,y,z = transfor_to_cartesian(latitudes, longitudes, altitudes)
x_int, y_int, z_int = interpolate_with_spline(x,y,z)

draw = False
if draw == True:
  fig = plt.figure()
  ax = fig.add_subplot(111, projection = '3d')
  ax.plot(x,y,z,'o', label = 'Datos Originales')
  ax.plot(x_int, y_int, z_int, '.', label = 'Interpolación Lineal')
  ax.set_xlabel("X")
  ax.set_ylabel("Y")
  ax.set_zlabel("Z")
  ax.legend()
  plt.show()
	
  
print(len(latitudes))