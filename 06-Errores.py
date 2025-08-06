""" Distancia Fréchet
Métrica que mide la similitud entre dos curvas o trayectorias,
teniendo en cuanta la forma y el Orden de los puntos.
"""
#Bibliotecas necesarias
import numpy as np 
from similaritymeasures import frechet_dist
from scipy.spatial.distance import euclidean
import matplotlib.pyplot as plt
# Conversion a coord cartesianas (x, y, z)
# Nota: La dist Frechet requiere puntos en un espacio métrico
def geo_to_cartesian(lat, lon, alt):
  R = 6371E3  # Radio de la Tierra en metros // No lo uso.
  lat_rad = np.radians(lat)
  lon_rad = np.radians(lon)
  x = alt * np.cos(lat_rad) * np.cos(lon_rad)
  y = alt * np.cos(lat_rad) * np.sin(lon_rad)
  z = -alt * np.sin(lat_rad)
  return np.column_stack((x, y, z)) # Matriz de Nx3

def leer_trayectoria(archivo):
  with open(archivo, 'r') as f:
        lineas = f.readlines()
  datos = [linea.strip().split(',') for linea in lineas[1:4]]
  
  lat = np.array([float(val) for val in datos[0]])
  lon = np.array([float(val) for val in datos[1]])
  alt = np.array([float(val) for val in datos[2]])
  
  alt_km = alt / 1000.0
  return lat, lon, alt_km

lat_pred, lon_pred, alt_pred = leer_trayectoria('./Trayectorias-text/trayectoria_pred1.txt')
lat_true, lon_true, alt_true = leer_trayectoria('./Trayectorias-text/trayectoria_true1.txt')

#	Conversión a coordenadas cartesianas
pred_cart = geo_to_cartesian(lat_pred, lon_pred, alt_pred) # Matriz 100x3
true_cart = geo_to_cartesian(lat_true, lon_true, alt_true) # Matriz 100x3

distancia_frechet = frechet_dist(pred_cart, true_cart)
print(f"Distancia Fréchet entre trayectorias: {distancia_frechet:.4f} km")
# 1. Comparamos primer punto


dist_primer_punto = euclidean(pred_cart[0], true_cart[0])
print(f"Distancia en primer punto: {dist_primer_punto:-2f} km")
# 2. Diferencia de altitudes
alt_diff = alt_pred - alt_true
print(f"Diferencia de altitudes: {np.mean(np.abs(alt_diff)):.2f} km")
#3. Visualización
fig = plt.figure(figsize = (15,10))

ax1 = fig.add_subplot(121, projection='3d')
ax1.scatter(pred_cart[:,0], pred_cart[:,1], pred_cart[:,2], c='blue', label='Predicha', s=20)
ax1.scatter(true_cart[:,0], true_cart[:,1], true_cart[:,2], c='red', label='Real', s=20)
ax1.set_title(f'Trayectorias 3D (Fréchet: {distancia_frechet:.4f} km)')
ax1.legend()

# Diferencias por punto
ax2 = fig.add_subplot(122)
distancias_punto_a_punto = [euclidean(p, t) for p, t in zip(pred_cart, true_cart)]
ax2.plot(distancias_punto_a_punto, 'g-', label='Distancia punto a punto')
ax2.axhline(distancia_frechet, color='r', linestyle='--', label='Distancia Fréchet')
ax2.set_title('Distancias por punto de muestreo')
ax2.set_ylabel('Metros')
ax2.legend()

plt.tight_layout()
plt.show()  