#CORRECTO!!!

import numpy as np
import matplotlib.pyplot as plt
from scipy.interpolate import splev, splprep

# Generamos puntos en una curva 3D usando una función paramétrica
t = np.linspace(0, 2*np.pi, 20)  # 20 puntos a lo largo de la curva
x = np.sin(t)
y = np.cos(t)
z = t

tck,u = splprep([x,y,z],s=0)
u_new = np.linspace(0,1,100)
#print("tck:",type(tck),"u:",type(u))
#print(tck)
x_new,y_new,z_new = splev(u_new,tck)
"""
Al utilizar splev(u,tck) los puntos interpolados se generan en las mismas
posiciones que se encuentran inicialmente debido a xyz.
por ello cambiamos a splev(u_new,tck) y generamos n muestras interpoladas.
"""
#print(x_new,y_new,z_new)

# Graficamos los puntos en 3D
fig = plt.figure(figsize=(12, 8))
ax = fig.add_subplot(projection='3d')
ax.plot(x, y, z, 'o')
ax.plot(x_new,y_new,z_new,marker='.',linestyle='None',color='red',markersize=5)
# Añadimos etiquetas a los ejes
ax.set_xlabel('Eje X')
ax.set_ylabel('Eje Y')
ax.set_zlabel('Eje Z')

# Mostramos la gráfica
plt.show()