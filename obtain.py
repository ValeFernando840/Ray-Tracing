##############################################################
"""
PASOS
1) Hacer un recorrido sobre las distintas fechas (for)
2) Por cada fecha una peticion de 00 a 23 hs (for)
3) En cada llamado o peticion tiene que cambiar la fecha y la hora (valores de entrada)
  Nota para este caso solo se modificaran fecha y horas para las peticiones y el resto de variables 
  se mantendrán constante.
4) Al terminar el llamado este pasa por un interpolador de lat long y elev, 100 muestras en 3D
5) Se almacenan esas 100 muestras en 3D con los nuevos valores dejando de lado los otros y manteniendo t
  todos los parametros de entrada en el dataset
6) Al finalizar el guardado se continua el ciclo for
"""
import numpy as np
import pandas as pd
"""
En el siguiente documento procedemos a realizar un barrido en hora y fecha
El dataset se almacenará con:
    24 muestras por día en pasos de hora durante todo el año 2010
    365x24 = 8760 muestras
"""
def barrido():
  horas = np.arange(24)
  df = pd.read_csv("dataset/dates2010.csv")
  i=0
  for date in df["Date"]:
    for j in horas:
      print("Fecha:",date,"Hora:",j)
    i+=1
    if i == 10:
      break
 
barrido()