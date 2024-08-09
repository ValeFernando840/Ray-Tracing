from scipy.interpolate import interp1d
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np

#########
import os
dir_actually = os.getcwd()
print(type(dir_actually),"\n========")
#########

interp_kinds = ['linear','nearest','nearest-up','zero','slinear','quadratic','cubic','previous']
file_name = 'new_data.dat'

df = pd.read_csv('./Temas-Vistos/datos/'+file_name, names=['x','y'], delimiter = ' ')

x=df['x']
y=df['y']


interp_kind = interp_kinds[0] # position 0 is linear

for value in interp_kinds:
    y_interp=interp1d(x, y, kind = value)
    x_new = np.linspace(0,2.*np.pi,50)
    y_new = y_interp(x_new)
    plt.plot(x_new,y_new, label = value)

plt.legend()
plt.show()
