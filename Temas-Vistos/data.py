import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
x = np.linspace(0, 2.*np.pi,10)
y = np.sin(x)

data = pd.DataFrame({'x':x,'y':y})
name_file = 'new_data.dat'
data.to_csv("./Temas-Vistos/datos/"+name_file, header= False, index = False, sep=' ')

plt.plot(x,y,marker='o')
plt.show()