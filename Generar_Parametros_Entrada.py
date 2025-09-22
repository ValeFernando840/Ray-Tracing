import pandas as pd
import numpy as np 

path = "./Solicitudes.xlsx" 
data = []
def generar_primera_parte_df(data):
    """Primera parte consiste de:
Fijo:
    - frecuencia de corte (fc)
    - elevacion (elevation)
    - azimuth (azimuth)
    - Año (anio)
Variables:
    - mmdd (mes y dia)
    - hora (0, 4, 8, 12, 16, 20)
    """
    fc = 10E6
    elevation = 5
    azimuth = 98
    anio = 2010
    fechas = pd.date_range(start = f'{anio}-01-01', end = f'{anio}-12-31', freq = 'D')
    mmdd = fechas.strftime("%m-%d")
    horas = [0, 4, 8, 12, 16, 20]
    for fecha in mmdd:
        for hora in horas:
            data.append([fc, elevation, azimuth, fecha, hora])
    return data


def generar_segunda_parte_df(data):
	"""
	La segunda parte del dataset consiste
	de tomar 2 muestras por cada dos meses en 1 am y 1 pm
	- frecuencia(fc): de 3MHz a 30MHz con paso de 1MHz
	- elevacion(elevation): de 0 a 40 grados con paso de 2 grados
	- azimuth(azimuth): de 87 a 91 grados con paso de 1 grado
	- Año (anio): 2010
	- mmdd (mes y dia): 15 de los meses impares
	- hora (1, 13)
	"""
	anio = 2010
	meses = [1,3,5,7,9,11]  
	hours = [1,13] # corresponde a 1am y 1pm
	fechas = [pd.Timestamp(anio,mes, 15) for mes in meses]
	fechas_str = [fecha.strftime("%m-%d") for fecha in fechas]
	frec = np.arange(3E6, 31E6, 1E6, dtype=int) # de 3MHz a 30MHz con paso de 1MHz
	elev = np.arange(0,41,2)
	azim = np.arange(87,92,1)
	print(f"fechas: {len(fechas_str)}, hours: {len(hours)}, elev: {len(elev)}, frec: {len(frec)}, azim: {len(azim)}")

	for fecha in fechas_str:
		for hora in hours:
				for frecuencia in frec:
						for elevation in elev:
								for azimuth in azim:
										data.append([frecuencia, elevation, azimuth, fecha, hora])
	return data

data = generar_primera_parte_df(data)
data = generar_segunda_parte_df(data)

print(f"Longitud solicitudes para el dataset: {len(data)}")

df = pd.DataFrame(data, columns = ['fc','elevation','azimuth','mmdd', 'hora'])

df.to_excel(path, index = False)