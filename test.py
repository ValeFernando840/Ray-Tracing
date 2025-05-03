import tensorflow as tf
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

from tensorflow.keras.models import load_model
import pickle
from Utils import plotter as utlnn
from Utils import geo_conversions as gc


x_test = pd.read_excel("./Train_Test/Dataset_Separado/x_test_new.xlsx")
y_test = pd.read_excel("./Train_Test/Dataset_Separado/y_test_new.xlsx")


# Quita de columnas no usadas en Train 
x_test = x_test.drop(columns=['latitude_pos_tx', 'longitude_pos_tx', 'elevation_pos_tx', 'year'])

#Carga de Modelos Entrenados.
autoencoder_x =  load_model('./modelos_entrenamiento/mod_x_R0/modelo1_x_con_scaler/modelo1_x.keras')
with open('./modelos_entrenamiento/mod_x_R0/modelo1_x_con_scaler/scaler_x1.pkl', 'rb') as f:
  scaler_x = pickle.load(f)

autoencoder_y = load_model('./modelos_entrenamiento/mod_y_R0/modelo1_y_con_scaler/modelo1_y.keras')
with open('./modelos_entrenamiento/mod_y_R0/modelo1_y_con_scaler/scaler_y1.pkl', 'rb') as f:
  scaler_y = pickle.load(f)
  
autoencoder_z = load_model('./modelos_entrenamiento/mod_z_R0/modelo1_con_scaler/modelo1.keras')
with open('./modelos_entrenamiento/mod_z_R0/modelo1_con_scaler/scaler_z1.pkl','rb') as f:
  scaler_z = pickle.load(f)

# Valores verdaderos
idx = 20
R0 = 6.371E6


y_true_x = (y_test.iloc[idx].to_numpy())[0:100]/R0
y_true_y = (y_test.iloc[idx].to_numpy())[100:200]/R0
y_true_z = (y_test.iloc[idx].to_numpy())[200:300]/R0

# Predicciones
y_pred_scaled_x = autoencoder_x.predict(np.expand_dims(x_test.iloc[idx], axis = 0))
y_pred_scaled_y = autoencoder_y.predict(np.expand_dims(x_test.iloc[idx], axis = 0))
y_pred_scaled_z = autoencoder_z.predict(np.expand_dims(x_test.iloc[idx], axis = 0))

y_pred_x = scaler_x.inverse_transform(y_pred_scaled_x).flatten()
y_pred_y = scaler_y.inverse_transform(y_pred_scaled_y).flatten()
y_pred_z = scaler_z.inverse_transform(y_pred_scaled_z).flatten()



# # Graficar resultados
# plt.figure(figsize = (12,6))
# plt.plot(y_true_x, label = 'True x', color = 'blue')
# plt.plot(y_pred_x, label = 'Pred x', color = 'red')
# plt.title('Comparación de valores verdaderos y predicciones para X')
# plt.grid(True)
# plt.legend()
# plt.show()


# plt.figure(figsize = (12,6))
# plt.plot(y_true_y, label = 'True y', color = 'blue')
# plt.plot(y_pred_y, label = 'Pred y', color = 'red')
# plt.title('Comparación de valores verdaderos y predicciones para Y')
# plt.grid(True)
# plt.legend()
# plt.show()


# plt.figure(figsize = (12,6))
# plt.plot(y_true_z, label = 'True z', color = 'blue')
# plt.plot(y_pred_z, label = 'Pred z', color = 'red')
# plt.title('Comparación de valores verdaderos y predicciones para Z')
# plt.grid(True)
# plt.legend()
# plt.show()


# Gráficos de resultado 3D

# utlnn.plot_3D(y_true_x*R0, y_true_y*R0, y_true_z*R0)
fig = plt.figure(figsize=(10, 6))
ax = fig.add_subplot(projection = '3d')
ax.scatter(y_true_x*R0, y_true_y*R0, y_true_z*R0, c='blue', label='True')
ax.scatter(y_pred_x*R0, y_pred_y*R0, y_pred_z*R0, c='red', label='Pred')
plt.show()
phi_true, theta_true, r_true = gc.transform_cartesian_to_spherical(y_true_x*R0, y_true_y*R0, y_true_z*R0)
phi_pred, theta_pred, r_pred = gc.transform_cartesian_to_spherical(y_pred_x*R0, y_pred_y*R0, y_pred_z*R0)


h_true = r_true
X_true = h_true * np.cos(phi_true) * np.sin(theta_true)
Y_true = h_true * np.sin(phi_true) * np.sin(theta_true)
Z_true = h_true * np.cos(theta_true)

fig = plt.figure(figsize=(10, 6))
ax = fig.add_subplot(projection='3d')
ax.scatter(X_true, Y_true, (Z_true-6.371E6)/1E3, c='blue', label='True')
plt.show()