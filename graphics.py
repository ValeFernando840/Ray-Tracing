import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd
import numpy as np

def convert_csv_space_to_comma(input_patch,output_patch): # usarlo para cuando el dataset no se encuentre separado por ,
    df = pd.read_csv(input_patch, delim_whitespace = True)
    df.to_csv(output_patch,index = False)
#def constant
constant = 1000000000
x_min_WiFi_24 = 2.412*10**9
x_max_WiFi_24 = 2.472*10**9
x_min_WiFi_5A = 5.17*10**9
x_max_WiFi_5A = 5.32*10**9
x_min_WiFi_5B = 5.5*10**9
x_max_WiFi_5B = 5.825*10**9
x_min_WiFi_6E = 5.925*10**9
x_max_WiFi_6E = 7.125*10**9
#direction file csv
measurement_csv_address = './DatasetAntena/s11.csv'
simulation_csv_address = './DatasetAntena/s11_cst.csv'

vswr_simulation = './DatasetAntena/VSWR_simulation.csv'
vswr_measurement = './DatasetAntena/VSWR_measurement.csv'
#read this csv
measurement_data = pd.read_csv(measurement_csv_address)
measurement_data['dB'] = -1*measurement_data['dB']

simulation_data = pd.read_csv(simulation_csv_address)
simulation_data['Frequency'] *= constant

plt.figure(figsize=(10, 6))
sns.lineplot(data = simulation_data, x = 'Frequency', y = 'dB', label = 'simulation')
sns.lineplot(data = measurement_data, x = 'Frequency', y = 'dB', label = 'measurement')


plt.axvspan(x_min_WiFi_24,x_max_WiFi_24,color ='red', alpha = 0.2 , label='WiFi 2.4')
plt.axvspan(x_min_WiFi_5A,x_max_WiFi_5A,color ='blue', alpha = 0.2 , label='WiFi 5')
plt.axvspan(x_min_WiFi_5B,x_max_WiFi_5B,color ='blue', alpha = 0.2)
plt.axvspan(x_min_WiFi_6E,x_max_WiFi_6E,color ='green', alpha = 0.2 , label='WiFi 6E')
#title and labels
plt.title('S-Parameters')
plt.xlabel('Frequency [GHz]')
plt.ylabel('S11 [dB]')
plt.grid(True)
plt.ylim(top=0)
plt.legend()


#convert_csv_space_to_comma(vswr_simulation,vswr_simulation) 
vswr_simulation_data = pd.read_csv(vswr_simulation)
vswr_simulation_data['Frequency'] *= constant
vswr_measurement_data = pd.read_csv(vswr_measurement)

plt.figure(figsize=(10,6))

sns.lineplot(data = vswr_simulation_data, x = 'Frequency', y = 'VSWR', label = 'simulation')
sns.lineplot(data = vswr_measurement_data, x = 'Frequency', y = 'VSWR', label = 'measurement')
plt.axvspan(x_min_WiFi_24,x_max_WiFi_24,color ='red', alpha = 0.2 , label='WiFi 2.4')
plt.axvspan(x_min_WiFi_5A,x_max_WiFi_5A,color ='blue', alpha = 0.2 , label='WiFi 5')
plt.axvspan(x_min_WiFi_5B,x_max_WiFi_5B,color ='blue', alpha = 0.2)
plt.axvspan(x_min_WiFi_6E,x_max_WiFi_6E,color ='green', alpha = 0.2 , label='WiFi 6E')
plt.title('Voltage Standing Wave Ratio (VSWR)')
plt.ylabel('VSWR')
plt.xlabel('Frequency [GHz]')
plt.ylim(top=10)
plt.grid(True)
plt.legend()
plt.show()

