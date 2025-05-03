import matplotlib.pyplot as plt 

def plot_1D(true_axis,pred_axis,name_axis):
  plt.figure(figsize = (10,6))
  plt.plot(true_axis, label = f'{name_axis} Reales',linestyle = 'None', marker='.')
  plt.plot(pred_axis, label = f'{name_axis} Predichas',linestyle = 'None', marker='o')

  plt.ylim()
  plt.title(f'Comparación Coord {name_axis}')
  plt.legend()
  plt.show()

def plot_3D(x,y,z,ax=None, color='blue', label=None , marker='o'):
  if ax is None:
    fig = plt.figure(figsize=(10,6))
    ax = fig.add_subplot(projection='3d')
  
  ax.scatter(x,y,(z+6371E3),c = color, marker = marker, label=f'Gráfica de {label}')
  ax.scatter(x[0],y[0],(z[0]),c = color,marker = marker,s=100,label='Tx')
  ax.legend()

  ax.set_zlabel('Altitud Z')
  return ax
