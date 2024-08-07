#==============================================================================
#Titulo: Confi_Trazador
#Autor: Zenon Saavedra 
#==============================================================================
"""
En este se generan los archivos.txt que configuran de forma inicial por modelos
IRI y Ray_Tracing  ambos en Fortran
    
Created on Sun May 23 22:55:24 2021
@author: Zenon
"""


import os
import sys
import numpy as np
import matplotlib.pyplot as plt
import math 
import math as pi


def Configuracion_RAY(lat_tx, long_tx, altitud_tx, frec_ini, elev, azim):
    """
    Esta funcion se encarga de generar el .txt de configuracion del
    programa ray_tracing para determinara el camino de propagacion.
    """

    Re = 6371e3; 
    file_ray = open('DATA_IN.txt','w+');
    
    ray = 1 # % 1: ordinario, 0: extra
    # altitud_tx = 0 #km
    latitud_tx = math.radians(lat_tx) #degtorad(-41.15); % Norte rad
    longitud_tx = math.radians(long_tx) #degtorad(174.89); % Este rad
    
    frec = 0; frec_stop = 0; frec_step = 0 #MHz
    #frec_ini
    
    elevacion_tx = 0; elev_stop = 0; elev_step = 0 #rad
    elev_ini = math.radians(elev) # radians(15); 
    
    azimuth_tx = 0; azim_stop = 0; azim_step = 0 #rad
    azim_ini = math.radians(azim) # radians(290); 
    
    altitud_rx = 0 # km
    only = 0 # variebale de bandera de progra RAY_TRACING
    max_hop = 1 
    max_step_hop = 1000
    latitud_geomag_polo = 1.5707963268 #rad Norte
    longitud_geomag_polo = 0 #rad Este
    
    tipo_integracion = 2 # 1: Runge and Kutta 2 : Adam-Multon
    max_error = 0.0000010000
    max_min_e = 50
    step_group = 8 # km Paso del Ray Tracing
    step_max = 100
    step_min = 0.0000000100
    step_factor = 0.5
    
    camino_fase = 1
    absorcion = 1
    corri_doppler = 1
    longitud_camino = 1
    
    frec_equa_cri = 6.5 
    hmax_ne = 250
    H0 = 62 
    alpha_beta = 0.5 # Chapman Layer: 1=beta  or   0.5 =alpha
    
    file_ray.write("%1.9f\n" % ray) # W1
    file_ray.write('%1.7f\n' % (Re/1e3))
    file_ray.write('%1.9f\n' % altitud_tx)
    file_ray.write('%1.9f\n' % latitud_tx)
    file_ray.write('%1.9f\n' % longitud_tx) # W5
    file_ray.write('%1.9f \n%1.9f \n%1.9f \n%1.9f\n' % (frec,frec_ini/1e6,frec_stop,frec_step))
    file_ray.write('%1.9f \n%1.9f \n%1.9f \n%1.9f\n' % (azimuth_tx,azim_ini,azim_stop,azim_step))
    file_ray.write('%1.9f \n%1.9f \n%1.9f \n%1.9f\n' % (elevacion_tx,elev_ini,elev_stop,elev_step))
    file_ray.write('%1.9f \n%1.9f\n' % (0,0))
    file_ray.write('%1.9f\n' % altitud_rx) # W20
    file_ray.write('%1.9f\n' % only)
    file_ray.write('%1.9f \n%1.9f\n' % (max_hop,max_step_hop))
    file_ray.write('%1.9f\n' % latitud_geomag_polo)
    file_ray.write('%1.9f\n' % longitud_geomag_polo)# W25
    
 #    file_ray.write('%1.9f\n' % zeros(1,15))
    blanco = np.zeros(15)
    
    for i in np.arange(np.size(blanco)):
        file_ray.write("%1.9f\n" % blanco[i])

    
    file_ray.write('%1.9f\n' % tipo_integracion) # W41
    file_ray.write('%1.9f\n' % max_error)
    file_ray.write('%1.9f\n' % max_min_e)
    file_ray.write('%1.9f\n' % step_group)
    file_ray.write('%1.9f\n' % step_max)
    file_ray.write('%1.9f\n' % step_min)
    file_ray.write('%1.9f\n' % step_factor) # W47
    
 #   file_ray.write(file_ray,'%1.9f\n',zeros(1,9));
    blanco = np.zeros(9)
    for i in np.arange(np.size(blanco)):
        file_ray.write("%1.9f\n" % blanco[i])
    
    file_ray.write('%1.9f\n' % camino_fase) # W57
    file_ray.write('%1.9f\n' % absorcion)
    file_ray.write('%1.9f\n' % corri_doppler)
    file_ray.write('%1.9f\n' % longitud_camino) # W60
    
 #   file_ray.write('%1.9f\n',zeros(1,10));
    blanco = np.zeros(10)
    for i in np.arange(np.size(blanco)):
        file_ray.write("%1.9f\n" % blanco[i])
        
    file_ray.write('%1.9f\n' % 5) # W71
    file_ray.write('%1.9f\n' % 1)
    
 #  file_ray.write('%1.9f\n',zeros(1,27))
    blanco = np.zeros(27)
    for i in np.arange(np.size(blanco)):
        file_ray.write("%1.9f\n" % blanco[i])
    
    file_ray.write('%1.9f\n' % 1) # W100
    file_ray.write('%1.9f\n' % frec_equa_cri)
    file_ray.write('%1.9f\n' % hmax_ne)
    file_ray.write('%1.9f\n' % H0)
    file_ray.write('%1.9f\n' % alpha_beta) #W104
    
 #   file_ray.write('%1.9f\n' % zeros(1,4));
    blanco = np.zeros(4)
    for i in np.arange(np.size(blanco)):
        file_ray.write("%1.9f\n" % blanco[i])
 
    
    file_ray.write('%1.9f\n' % 100e3) # W109
    file_ray.write('%1.9f\n' % 300);
    file_ray.write('%1.9f\n' % 80) 
    
 #   file_ray.write('%1.9f\n' % zeros(1,288))
    blanco = np.zeros(288)
    for i in np.arange(np.size(blanco)):
        file_ray.write("%1.9f\n" % blanco[i])

    
    file_ray.close()
    #cd(oldFolder); % Vuelde desde la carpera "source"

def Configuracion_IRI(Anio, Fecha, UTI, Hora):
    """
    Esta funcion se encarga de generar el .txt que configura el
    programa IRI.
    """


    file_IRI = open('CONFI_IRI.txt','w+')
    file_IRI.seek(0,0)
    #file.write('0 %d %d\n' %(Lat, Long))
    file_IRI.write("%d %s %d %d\n" %(Anio,Fecha,UTI,Hora))
    
    Alt = 100
    altura_inicial = 1 
    altura_final = 300 
    altura_paso =  1
    file_IRI.write("%d\n" % Alt)
    file_IRI.write("%d\n" % 0)
    file_IRI.write("%d\n" % 0)
    file_IRI.write("%d\n" % 1)
    file_IRI.write("%d %d %d\n" %(altura_inicial,altura_final,altura_paso))
    file_IRI.write("%d\n" % 1)
    
    # datos_IRI = ["T","F","F","F","F","T","F","T","T","T","T","F","T","T","T","T",
    #              "F","F","T","F","F","T","F","F","F","F","F","F","F","F","T","F",
    #              "F","T","F","T","T","T","T","T","T","T","T","T","T","T","T","T",
    #              "T","T","107.5","107","50","52.7"]
    
    
    
    
    datos_IRI = ["T","F","F","F","F","T","F","T","T","T","T","F","T","T","T","T",
                "T","F","T","F","F","T","T","T","T","F","T","F","F","F","T","T",
                "F","T","F","T","T","T","T","T","T","T","T","T","T","T","T","T",
                "T","T","107.5","107","50","52.7"]

    
    
    for i in np.arange(np.size(datos_IRI)):
        file_IRI.write("%s\n" %datos_IRI[i])
            
    file_IRI.close()
    
