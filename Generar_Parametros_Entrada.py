import pandas as pd
import numpy as np 

fc = 10E6
elevation = 5
azimuth = 98
anio = 2010

fechas = pd.date_range(start = f'{anio}-01-01', end = f'{anio}-12-31', freq = 'D')
mmdd = fechas.strftime("%m-%d")
horas =[0, 4, 8, 12, 16, 20]
data = []

for fecha in mmdd:
    for hora in horas:
        data.append([fc, elevation, azimuth, fecha, hora])

df = pd.DataFrame(data, columns = ['fc','elevation','azimuth','mmdd', 'hora'])

print(df.head(10))