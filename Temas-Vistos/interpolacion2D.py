import numpy as np
import pandas as pd
from scipy.interpolate import LinearNDInterpolator,CloughTocher2DInterpolator
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D

data = pd.read_csv('./Temas-Vistos/datos/malla_puntos.dat', delimiter = ' ')
print(data.head())
#Transformo a numpy array xyz por capricho, xq ví que column_stack puede trabajar con Series de pandas tranquilamente
x = data['x'].to_numpy()
y = data['y'].to_numpy()
z = data['z'].to_numpy()
points = np.column_stack((x,y))
#print(points[0],type(points))
#Tambien Existe CloughTocher2DInterpolator que realiza una interpolacion más suave
#interpolator = CloughTocher2DInterpolator(points,z)
interpolator = LinearNDInterpolator(points,z)
size = 100
x_new = np.linspace(min(x),max(x),size)
y_new = np.linspace(min(y),max(y),size)

z_interpolate = interpolator(x_new,y_new)
print(len(z_interpolate))
print(z_interpolate, type(z_interpolate))


fig = plt.figure()

ax = fig.add_subplot(111, projection='3d')
ax.scatter(x,y,z,color='b')
ax.scatter(x_new, y_new, z_interpolate, color='r', marker='o')

# Añadimos etiquetas a los ejes
ax.set_xlabel('Eje X')
ax.set_ylabel('Eje Y')
ax.set_zlabel('Eje Z')

# Mostramos la gráfica
plt.show()  
