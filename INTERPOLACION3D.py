#Bibliotecas 
import pandas as pd
import numpy as np
import ast
import matplotlib.pyplot as plt
from scipy.interpolate import CubicSpline
from scipy.interpolate import make_interp_spline
from scipy.interpolate import griddata
from scipy.interpolate import PchipInterpolator
from Utils import geo_conversions as gc

df = pd.read_excel("prueba04-09.xlsx")
R0 = 6.371E6 # Radio de la Tierra en m
idx = 1 # Index 0 a 3
strng_lat = df["latitudes"].iloc[idx] ; latitudes = np.fromstring(strng_lat.strip("[]"), sep=" ")
strng_lon = df["longitudes"].iloc[idx] ; longitudes = np.fromstring(strng_lon.strip("[]"), sep=" ")
strng_alt = df["alturas"].iloc[idx] ; altitudes = np.fromstring(strng_alt.strip("[]"), sep=" ")

def transform_to_cartesian(latitudes, longitudes, altitudes):
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
	# phi <-- latitud, theta <-- longitud
	R_earth = 6.371E6 # Radio de la Tierra en m
	phi = np.radians(latitudes)
	theta = np.radians(longitudes)
	# PHI,THETA = np.meshgrid(np.radians(phi), np.radians(theta))          
	r = R_earth + altitudes
	x = r * np.cos(phi) * np.sin(theta)
	y = r * np.sin(phi) * np.sin(theta)
	z = r * np.cos(theta) 
	print("Shape x", x.shape)
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
	num_points = 100
	x_initial = x.ravel()[0]
	x_end = x.ravel()[-1]
	print(x_end)
	y_initial = y.ravel()[0]
	y_end = y.ravel()[-1]
	x_new = np.linspace(x_initial, x_end, num_points)
	y_new = np.linspace(y_initial, y_end, num_points)
	x_new,y_new = np.meshgrid(x_new, y_new)
	z_new = griddata((x.ravel(), y.ravel()), z.ravel(), (x_new, y_new), method='linear')
  
	return x_new, y_new, z_new
def interpolate_with_Pchip(x,y,z):
	"""
	Interpola puntos 3D utilizando PCHIP (Piecewise Cubic Hermite Interpolating Polynomial).
	Args:
		x (_array_): _Array de coordenadas x._
		y (_array_): _Array de coordenadas y._
		z (_array_): _Array de coordenadas z._
	Returns:
		x_pchip (_array_): _Array de coordenadas x interpoladas._	
		y_pchip (_array_): _Array de coordenadas y interpoladas._
		z_pchip (_array_): _Array de coordenadas z interpoladas._
	"""
	dx = np.diff(x)
	dy = np.diff(y)
	dz = np.diff(z)

	dist = np.sqrt(dx**2 + dy**2 + dz**2)
	cumulative_dist = np.concatenate(([0], np.cumsum(dist)))
	t_coarse = cumulative_dist
	t_fine = np.linspace(0, cumulative_dist[-1],200)

	interp_x = PchipInterpolator(t_coarse, x)
	interp_y = PchipInterpolator(t_coarse, y)
	interp_z = PchipInterpolator(t_coarse, z)
	x_pchip = interp_x(t_fine)
	y_pchip = interp_y(t_fine)
	z_pchip = interp_z(t_fine)
	print(f"Original x range: [{x.min():.2f}, {x.max():.2f}]")
	print(f"Interpolated x range: [{x_pchip.min():.2f}, {x_pchip.max():.2f}]")
	return x_pchip, y_pchip, z_pchip

x,y,z = transform_to_cartesian(latitudes, longitudes, altitudes)
x_int, y_int, z_int = interpolate_with_Pchip(x,y,z)
phi_int, theta_int, rho_int = gc.transform_cartesian_to_spherical(x_int,y_int,z_int)
lat_int, lon_int, alt_int = gc.transform_spherical_to_geographic(phi_int, theta_int, rho_int)
gc.generate_KML(latitudes, longitudes, altitudes+R0,
								 lat_int, lon_int, alt_int,
								 "./", "Resultados1")
draw = False
if draw == True:
  fig = plt.figure()
  ax = fig.add_subplot(111, projection = '3d')
  ax.plot(x,y,(z-6.371e6)/1e3,'o', label = 'Datos Originales')
  ax.plot(x_int, y_int, (z_int-6.371e6)/1e3, '.', label = 'Interpolación Lineal')
  ax.set_xlabel("X")	
  ax.set_ylabel("Y")
  ax.set_zlabel("Z")
  ax.legend()
  plt.show()