#==============================================================================
#Titulo: Ray_Tracing

#==============================================================================
"""
En este se determina el camino de propagacion seguido por una O.E

Para la determinacion del camino se utiliza la tecnica del Ray Tracing.
Dos modelos son utilizados IRI y el Ray_Tracing (en Fortran)

Se definen parametros como:
      Camino de propagacion
      Retardo
      Rango Oblicuo
      Rango Terrestre
"""

import os
import sys
import numpy as np
import matplotlib.pyplot as plt 
import math
import Confi_Trazador
import pandas as pd 
from scipy.interpolate import griddata
import Utils.functions as fn
############################
class Posicion_Geo():
    def __init__(Pos,Latitud,Longitud,Altitud):
        Pos.Latitud = Latitud
        Pos.Longitud = Longitud
        Pos.Altitud = Altitud
  
def Esfe2xyz(va,az,d):  # Convierte coord. Esfericas a coord. Cartesianas
    va = np.radians(va) # va: ángulo de Elevación
    az = np.radians(az) # az: ángulo de Azimuth 
    sinv = np.sin(va)
    cosv = np.cos(va)
    sina = np.sin(az)
    cosa = np.cos(az)
    x = d*cosv*cosa     #d: distancia
    y = d*cosv*sina
    z = d*sinv
    return x,y,z

def Rango_Ground(lat_tx,lon_tx,lat_final,lon_final):
    """
    Determina el Rango Terrestre seguido por la O.E.
    float RangoGround(float lat_tx, float lon_tx, float lat_final, float lon_final)
    input:
        lat_tx: Latitud del Transmisor (º)
        lon_tx: Longitud del Transmisor (º)
        lat_final: Latitud alcanzada con el RT (º)
        lon_final: Longitud alcanzada con el RT(º)
        
    output:
        Range: Range ground between Rx position and RT position  [m]
    """
    lat_tx_r = math.radians(lat_tx)
    lon_tx_r = math.radians(lon_tx)
    
    lat_final_r = math.radians(lat_final)
    lon_final_r = math.radians(lon_final)    
    
    Re = 6371e3 # Radio de la tierra (m)
    aux = (math.sin((lat_final_r-lat_tx_r)/2))**2 + math.cos(lat_tx_r)*math.cos(lat_final_r)*(math.sin((lon_final_r-lon_tx_r)/2))**2 
    Range = 2 * Re * math.asin(math.sqrt(aux))
    
    return Range

def Trazador_Rayos(Lat_Tx, Long_Tx, Altitud_Tx, frec, elev, azim, Anio, Fecha, UTI, Hora,plot):
	"""
	Determina el camino de propagacion de la O.E y una serie de parametros
	relacionados con ello
			
	float Trazo_Rayos(float fc,float Lat_Tx, float Lon_Tx,string Fecha,float Rz)
			Entrada:
					fc: Frec. de Portadora[Hz]
					Lat_Tx: Latitud del Tx [º decimales]
					Lon_Tx: Longitud del Tx [º decimales]
					Fecha: dia mes anio [ddmmaa]
					Rz: Numero de manchas solares
					Ang_Elev: 
					Ang_Azi:
					plot: Si se desea realilzar el ploteo de la Ray Tracing
			Salida: 
					Retardo: Ratardo de la O.E (ida) [s]
					Rango_Terrestre: Distancia medida sobre la tierra [m]
					Rango_Oblicuo: Distancia seguida por la O:E [m]
					Atte_Des: Atenuacion con desviación 
					Lat_Obj: Latitud del Objetivo [º decimales]
					Lon_Obj: Longitud del Objetivo [º decimales]
					Alt_Obj: Altitud del Objetivo [m]
	"""
	#########################################
	#Obtiene el directorio de trabajo actual
	dir = os.getcwd()
	nueva = "ray_tracing/dist/Release/Cygwin_1-Windows"
	nuevaDireccion = os.path.join(dir, nueva)
	os.chdir(nuevaDireccion)
	#########################################
	#Se adapto para que la ruta quede de manera general
	#os.chdir(r"C:\Users\admin\Desktop\Ray-Tracing\ray_tracing\dist\Release\Cygwin_1-Windows")

	#Lat_Tx = -42.28 # Latitud Geo.
	#Long_Tx = -63.4 # Longitud Geo.
	#Altitud_Tx = 0     
	#frec = 5e6 # Hz
	#elev = 6
	#azim = 98
	#Anio = 2010
	#Fecha = "0516"
	#UTI = 0
	#Hora = 15
	
	#==============================================================================
	Confi_Trazador.Configuracion_IRI(Anio, Fecha, UTI, Hora)
	
	#==============================================================================
	Confi_Trazador.Configuracion_RAY(Lat_Tx, Long_Tx, Altitud_Tx, frec, elev, azim)
	
	#==============================================================================
																		
	os.system("ray_tracing.exe")
	
	with open ('raytracing.txt',"r") as f:
			coord = f.readlines() #Dentro de raytracing.txt hay un conjunto de 3 columnas con nums (Coord Esf?)
	
	
	N = np.size(coord) #Devuelve un valor de 84 que son las 84 lineas que tiene el archivo
	
	aux = []
	for i in np.arange(N):    
			aux.append(coord[i].split())
	# genera un array [['','',''],['','','']...,['','','']]       
	
	
	pos = np.array(aux).astype(float) #Crea un array NumPy tipo[[ele1 ele2 ele3]...[ele1 ele2 ele3]]
	
	G = np.where((np.diff(pos[:,0]) != 0) & (np.diff(pos[:,1]) != 0) & (np.diff(pos[:,2]) != 0) )
	#obtiene los indices donde se cumple con las diferencias. 
	#print(G,'\n')
	g = np.asarray(G).transpose() #Transf a un array y lo transpone para una estructura conveniente O.o
	
	"""
	pos[:,0]: indica todas las filas de la columna 0
	pos[:,1]: indica todas las filas de la columna 1
	
	"""
	
	Retardo = pos[-1,0]/1e3
	Rango_Oblicuo = pos[-1,1]*1e3
	# print("Retardo:", Retardo,'\n',"Rango Oblicuo:",Rango_Oblicuo)
	
	rho = pos[g,0]
	phi = pos[g,1]
	theta = pos[g,2]
	
	radio = rho * 1E3
	#print("radio:",radio)
	Lat = np.degrees((math.pi/2) - phi)
	Lon = np.degrees(theta)
	Alt = (radio - 6.371E6)    
	
	Lat_Final = Lat[-1]
	Lon_Final = Lon[-1]
	Alt_Final = Alt[-1]

	Rango_Terrestre = Rango_Ground(Lat_Tx,Long_Tx,Lat_Final.item(),Lon_Final.item())
	
	if (plot == True) :
			R = radio
			PHI,THETA = np.meshgrid(np.radians(phi),np.radians(theta))
			X = R * np.cos(PHI) * np.sin(THETA)
			Y = R * np.sin(PHI) * np.sin(THETA)
			Z = R * np.cos(THETA)
			
			num_muestras_interpolar = 100
			x_initial = X.ravel()[0]
			x_end = X.ravel()[-1]
			y_initial = Y.ravel()[0]
			y_end = Y.ravel()[-1]

			x_new = np.linspace(x_initial,x_end,num_muestras_interpolar)
			y_new = np.linspace(y_initial,y_end,num_muestras_interpolar)
			z_new = griddata((X.ravel(), Y.ravel()), Z.ravel(), (x_new, y_new), method='linear')

			fig = plt.figure()
			ax = fig.add_subplot(projection = '3d')
			
			ax.scatter(x_new.ravel(),y_new.ravel(),(z_new.ravel()-6.371E6)/1e3,color='blue',marker = '.')
			

			print("NuevasAlturas :",z_new-6.371E6, len(z_new))
			# surf = ax.plot_surface(X,Y, (Z- 6.371E6)/1E3, rstride=1, cstride=1, cmap=cm.jet,
			#         linewidth=0, antialiased=False)
			
			ax.plot3D(X.ravel()[0],Y.ravel()[0],(Z.ravel()[0]-6.371E6)/1e3, '2',mew = 12,label = "Tx")
			ax.legend()
			
			Pos_Lon_med = int(len(Lon)/2); Pos_Lat_med = int(len(Lat)/2)
			
			Lon_min = round(Long_Tx,2); Lon_max = round(Lon_Final.item(),2); Lon_med = round(float(Lon[Pos_Lon_med]),2) 
			ax.set_yticks([Y[0,0],Y[Pos_Lon_med, Pos_Lon_med], Y[-1,-1]])
			ax.set_yticklabels([Lon_min, Lon_med,Lon_max])
			ax.set_xticks([X[0,0], X[Pos_Lat_med,Pos_Lat_med], X[-1,-1]])
			Lat_min = round(Lat_Tx,2); Lat_max = round(Lat_Final.item(),2); Lat_med = round(float(Lon[Pos_Lat_med]),2)
			ax.set_xticklabels([Lat_min,Lat_med,Lat_max])
			
			ax.set_zlabel("Altitud (km)")
			ax.set_xlabel("Latitud ($\\degree$)")
			ax.set_ylabel("Longitud ($\\degree$)")

	plt.show()
	os.chdir(dir)
	

	return Retardo, Rango_Terrestre, Rango_Oblicuo, Lat_Final, Lon_Final, Alt_Final,Lat,Lon,Alt


def main():
	print(f'\n')
	print(f'=============Inicio============')
	#Parametros de Entrada
	Tipo_zona = "Rural"    #'Comercial' 'Residencial' 'Rural' 'Rural Tranquila' NO USADO
	Lat_Tx = -42.28 # Latitud Geografica [º decimales]
	Lon_Tx = -63.4 # Longitud Geografica [º decimales]
	Alt_Tx = 0 # m 
	UTI = 0
	Posicion_Tx = Posicion_Geo(Lat_Tx,Lon_Tx,Alt_Tx)

	# Hora = 10 # Hora 24 hs
	# Fecha = "15-06-2010" # ddmmaa
	# dia,mes,anio = Fecha.split("-")
	# Anio = float(anio)
	# mmdd = mes + dia
	fc = 21E6 # Hz   [3-30] initial_value = 10e6
	elev = 34              #initial_value = 5
	azim = 91              #initial_value = 98
	AB = 10e3 # Hz
	##barrido
	horas = np.arange(0,24,4)
	# df = pd.read_csv("dataset/dates2010.csv")
	#desde el elemento 1 al elemento 30 de Date
	# [Retardo, Rango_Terrestre, Rango_slant, Lat_Final,Lon_Final, Alt_Final,latitudes,longitudes,elevations] = Trazador_Rayos(
	#     Posicion_Tx.Latitud,Posicion_Tx.Longitud,Posicion_Tx.Altitud,
	#     fc, elev, azim, Anio, mmdd, UTI, Hora,plot = False)


												# 15
	# for date in df["Date"][80:365]:
	# 	dia,mes,anio = date.split("-")
	# 	mmdd = mes + dia
	# 	Anio = float(anio)
	# 	print("Fecha",date)
	# 	for hora in horas:
	# 		# print("Fecha:",date,"Hora:",hora)
	# 		[Retardo, Rango_Terrestre, Rango_oblicuo, Lat_Final,Lon_Final, Alt_Final,latitudes,longitudes,elevations] = Trazador_Rayos(
	# 		Posicion_Tx.Latitud,Posicion_Tx.Longitud,Posicion_Tx.Altitud,
	# 		fc, elev, azim, Anio, mmdd, UTI, hora,plot = False)

	# 		df = fn.generate_dataframe(Posicion_Tx.Latitud,Posicion_Tx.Longitud,Posicion_Tx.Altitud,
	# 		fc, elev, azim, Anio, mmdd, UTI, hora,Retardo, Rango_Terrestre, Rango_oblicuo, 
	# 		Lat_Final,Lon_Final, Alt_Final,latitudes,longitudes,elevations)
	# 		fn.add_to_dataset(df)
        
	#Desde Aqui agregamos code para armar la segunda parte del Dataset
	data = pd.read_csv("dataset/nuevo.csv")
  #Se cambio la fecha a una en especifico 15 de diciembre de 2010  a 12 hs
	Fecha = "15-12-2010" # ddmmaa
	dia,mes,anio = Fecha.split("-")
	Anio = float(anio)
	mmdd = mes + dia
	hora = 12
	# for index,row in data.iterrows():
	# 	print("Estamos en el index: ",index)
	# 	print("Muestra: Frequency Elevation Azimuth",row["Frequency"], row["Elevation"], row["Azimuth"])
	# 	fc = int(row["Frequency"])
	# 	elev = int(row["Elevation"])
	# 	azim = int(row["Azimuth"])
	# 	[Retardo, Rango_Terrestre, Rango_oblicuo, Lat_Final,Lon_Final, Alt_Final,latitudes,longitudes,elevations] = Trazador_Rayos(
	# 		Posicion_Tx.Latitud,Posicion_Tx.Longitud,Posicion_Tx.Altitud,
	# 		fc, elev, azim, Anio, mmdd, UTI, hora,plot = False)
		
	# 	df = fn.generate_dataframe(Posicion_Tx.Latitud,Posicion_Tx.Longitud,Posicion_Tx.Altitud,
	# 		fc, elev, azim, Anio, mmdd, UTI, hora,Retardo, Rango_Terrestre, Rango_oblicuo, 
	# 		Lat_Final,Lon_Final, Alt_Final,latitudes,longitudes,elevations)
		
	fn.add_to_dataset(df)
		# print("=====Agregado Nueva Muestra=====")


	[Retardo, Rango_Terrestre, Rango_oblicuo, Lat_Final,Lon_Final, Alt_Final,latitudes,longitudes,elevations] = Trazador_Rayos(
			Posicion_Tx.Latitud,Posicion_Tx.Longitud,Posicion_Tx.Altitud,
			fc, elev, azim, Anio, mmdd, UTI, hora,plot = False)
		
	df = fn.generate_dataframe(Posicion_Tx.Latitud,Posicion_Tx.Longitud,Posicion_Tx.Altitud,
			fc, elev, azim, Anio, mmdd, UTI, hora,Retardo, Rango_Terrestre, Rango_oblicuo, 
			Lat_Final,Lon_Final, Alt_Final,latitudes,longitudes,elevations)

	# df.to_excel("prueba04-09.xlsx", index = False)
	fn.add_to_excel(dir="prueba04-09.xlsx", line_df=df)
	return 



# INICIO    
if __name__ == '__main__':
    main()