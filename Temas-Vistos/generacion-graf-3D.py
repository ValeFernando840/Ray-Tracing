import numpy as np
import matplotlib.pyplot as plt

# Definimos un rango de valores para u y v, que se usan para parametrizar la superficie
u = np.linspace(-5, 5, 20)
v = np.linspace(-5, 5, 20)
u, v = np.meshgrid(u, v)

# Definimos la superficie utilizando una función paramétrica
x = u
y = v
z = u**2 + v**2

# Guardamos los puntos en un archivo .dat
points = np.column_stack((x.ravel(), y.ravel(), z.ravel()))
np.savetxt('./Temas-Vistos/datos/malla_puntos.dat', points, header='x y z', comments='')

# Graficamos la malla de puntos en 3D
fig = plt.figure()
ax = fig.add_subplot(111, projection='3d')
ax.scatter(x, y, z, color='b')

# Añadimos etiquetas a los ejes
ax.set_xlabel('Eje X')
ax.set_ylabel('Eje Y')
ax.set_zlabel('Eje Z')

# Mostramos la gráfica
plt.show()
