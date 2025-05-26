import matplotlib.pyplot as plt 
import numpy as np

def plot_1D(true,pred,name_axis):
  y_true_max = np.max(true)
  y_true_min = np.min(true)
  y_pred_max = np.max(pred)
  y_pred_min = np.min(pred)

  plt.figure(figsize = (12,6))
  label_true = f'{name_axis} Real'
  label_pred = f'{name_axis} Predicción'
  plt.plot(true, label = label_true, linestyle = 'None', marker = '.')
  plt.plot(pred, label = label_pred, linestyle = 'None', marker = 'o')
  plt.axhline(y = y_true_max, color = 'red',  linestyle = '-.', label=f'Máx_true: {y_true_max:.3f}')
  plt.axhline(y = y_pred_max, color = 'red',  linestyle = ':' , label=f'Máx_pred: {y_pred_max:.3f}')
  plt.axhline(y = y_true_min, color = 'blue', linestyle ='-.' , label=f'Mín_true: {y_true_min:.3f}')
  plt.axhline(y = y_pred_min, color = 'blue', linestyle = ':' , label=f'Mín_pred: {y_pred_min:.3f}')
  plt.title("Gráfico Predicción vs Real")
  plt.xlabel(f'Coordenada {name_axis}')
  plt.grid(True)
  plt.title(f'Comparación Coord {name_axis}')
  plt.legend()
  plt.show()

def plot_2D(true_x,true_y,pred_x,pred_y):
  plt.figure(figsize = (12,6))
  label_true = 'Real'
  label_pred = 'Predicción' 
  plt.scatter(true_x, true_y, label = label_true, color = 'blue',alpha = 0.5)
  plt.scatter(pred_x, pred_y, label = label_pred, color = 'red', alpha = 0.5)
  
  plt.title('Gráfico Predicción vs Real')
  plt.xlabel('Coordenada X')
  plt.ylabel('Coordenada Y')
  plt.grid(True)
  plt.legend()
  plt.show()

def plot_3D(x,y,z,ax=None, color='blue', label=None , marker='o'):
  if ax is None:
    fig = plt.figure(figsize=(10,6))
    ax  = fig.add_subplot(projection='3d')
  
  ax.scatter(x,y,(z+6371E3),c = color, marker = marker, label=f'Gráfica de {label}')
  ax.scatter(x[0],y[0],(z[0]),c = color,marker = marker,s=100,label='Tx')
  ax.legend()

  ax.set_zlabel('Altitud Z')
  return ax
