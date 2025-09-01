import pandas as pd 
import numpy as np
import tensorflow as tf
from tensorflow.keras.layers import Input, Dense, LSTM, GRU, Bidirectional, Dropout, BatchNormalization
from tensorflow.keras.models import Model
from tensorflow.keras.callbacks import EarlyStopping, ReduceLROnPlateau
from tensorflow.keras.optimizers import Adam
from sklearn.preprocessing import StandardScaler 
from sklearn.model_selection import train_test_split
import matplotlib.pyplot as plt

x_test = pd.read_excel("../Train_Test/Dataset_Separado/x_test_new.xlsx")
x_train = pd.read_excel("../Train_Test/Dataset_Separado/x_train_new.xlsx")










































# import pandas as pd 
# import numpy as np

# import matplotlib.pyplot as plt
# from tensorflow.keras.callbacks import EarlyStopping, ReduceLROnPlateau 
# from tensorflow.keras.models import Model
# from tensorflow.keras.layers import Input, Dense
# from tensorflow.keras.regularizers import l2
# from sklearn.model_selection import train_test_split

# import sys
# sys.path.append('../')
# from Utils import utils_nn as utlnn

# x_test	= pd.read_excel("../Train_Test/Dataset_Separado/x_test_new.xlsx")
# x_train	= pd.read_excel("../Train_Test/Dataset_Separado/x_train_new.xlsx")
# y_test	= pd.read_excel("../Train_Test/Dataset_Separado/y_test_new.xlsx")
# y_train	= pd.read_excel("../Train_Test/Dataset_Separado/y_train_new.xlsx")

# # Definimos el radio R0
# R0						= 6.371E6 # [m]
# columns_drop	= [f'z_{i}' for i in range(1,101)]

# y_train_xy	= y_train.drop(columns=columns_drop)/R0
# y_test_xy		= y_test.drop(columns=columns_drop)/R0

# print(y_train_xy.head())

# # Quita columnas innecesarias
# x_train	= x_train.drop(columns = ['latitude_pos_tx', 'longitude_pos_tx', 'elevation_pos_tx', 'year'])
# x_test	= x_test.drop(columns =['latitude_pos_tx', 'longitude_pos_tx', 'elevation_pos_tx', 'year'])

# print(x_train.head())
# print(y_train_xy.iloc[:,:100])

# # Escado de datos
# from sklearn.preprocessing import MinMaxScaler

# scaler_x = MinMaxScaler()
# scaler_y = MinMaxScaler()

# y_train_x_scaled	= scaler_x.fit_transform(y_train_xy.iloc[:,:100])
# y_test_x_scaled		= scaler_x.transform(y_test_xy.iloc[:,:100])

# y_train_y_scaled	= scaler_y.fit_transform(y_train_xy.iloc[:,100:])
# y_test_y_scaled		= scaler_y.transform(y_test_xy.iloc[:,100:]) 

# reduce_lr		= ReduceLROnPlateau(
#   monitor		= 'val_loss',
#   patience	= 20,
#   factor		= 0.5
# )

# from tensorflow.keras.optimizers import Adam, AdamW, RMSprop, Nadam,SGD

# #def 
# act_name	= 'relu'
# l2_reg		= 0.0007
# epochs		= 700
# b_s				= 32
# optimizer	= Adam(learning_rate=1e-3)

# #Arquitectura de la red neuronal
# inputs	= Input(shape=(5,))
# encoded = Dense(32,	 activation = act_name, kernel_regularizer = l2(l2_reg))(inputs)
# encoded = Dense(64,	 activation = act_name, kernel_regularizer = l2(l2_reg))(encoded)
# encoded = Dense(128, activation = act_name, kernel_regularizer = l2(l2_reg))(encoded)
# encoded = Dense(256, activation = act_name, kernel_regularizer = l2(l2_reg))(encoded)
# encoded = Dense(512, activation = act_name, kernel_regularizer = l2(l2_reg))(encoded)
# encoded = Dense(256, activation = act_name, kernel_regularizer = l2(l2_reg))(encoded)

# decoded_x = Dense(100, activation = 'linear', kernel_regularizer = l2(l2_reg), name='x')(encoded)
# decoded_y = Dense(100, activation = 'linear', kernel_regularizer = l2(l2_reg), name='y')(encoded)
# # Def modelo multiples salidas
# model_xy = Model(inputs=inputs, outputs=[decoded_x, decoded_y])
# model_xy.compile(optimizer=optimizer, loss='mae')
# model_xy.summary()

# history_xy = model_xy.fit(x_train, [y_train_x_scaled, y_train_y_scaled],
#                           epochs 						= epochs,
#                           batch_size 				= b_s,
#                           validation_split	= 0.1,
#                           callbacks					= [reduce_lr]
#                           )

# loss = model_xy.evaluate(x_test,[y_test_x_scaled, y_test_y_scaled])
# save_model = False
# if (save_model == True): 
#   model_xy.save('../modelos_entrenamiento/mod_x_y_R0/modelo1_x_y_con_scaler/mod_x_y_R0.keras')
#   import pickle
#   with open('../modelos_entrenamiento/mod_x_y_R0/modelo1_x_y_con_scaler/scaler_x.pkl', 'wb') as file:
#         pickle.dump(scaler_x, file) 
#   with open('../modelos_entrenamiento/mod_x_y_R0/modelo1_x_y_con_scaler/scaler_y.pkl', 'wb') as file:
# 	  	pickle.dump(scaler_y, file)


import pandas as pd 
import numpy as np
import matplotlib.pyplot as plt
from tensorflow.keras.callbacks import EarlyStopping, ReduceLROnPlateau
from tensorflow.keras.models import Model
from tensorflow.keras.layers import Input, Dense
from tensorflow.keras.regularizers import l2
from tensorflow.keras.optimizers import Adam
from sklearn.preprocessing import MinMaxScaler

import sys
sys.path.append('../')
from Utils import plotter as plots

# Obtención, drop y normalización de los datos.
x_test		= pd.read_excel("../Train_Test/Dataset_Separado/x_test_new.xlsx")
x_train		= pd.read_excel("../Train_Test/Dataset_Separado/x_train_new.xlsx")
y_test		= pd.read_excel("../Train_Test/Dataset_Separado/y_test_new.xlsx")
y_train		= pd.read_excel("../Train_Test/Dataset_Separado/y_train_new.xlsx")

x_train 	= x_train.drop(columns = ['latitude_pos_tx', 'longitude_pos_tx', 'elevation_pos_tx', 'year'])
x_test		= x_test.drop(columns =['latitude_pos_tx', 'longitude_pos_tx', 'elevation_pos_tx', 'year'])

R0 = 6.371E6 #[m]
y_train_xyz = y_train/R0
y_test_xyz	= y_test/R0


# Escalado.
scaler_x	= MinMaxScaler()
scaler_y	= MinMaxScaler()
scaler_z	= MinMaxScaler()

y_train_x_scaled	= scaler_x.fit_transform(y_train_xyz.iloc[:,   :100])
y_train_y_scaled	= scaler_y.fit_transform(y_train_xyz.iloc[:,100:200])
y_train_z_scaled	= scaler_z.fit_transform(y_train_xyz.iloc[:,200:300])

y_test_x_scaled	= scaler_x.transform(y_test_xyz.iloc[:,		:100])
y_test_y_scaled	= scaler_y.transform(y_test_xyz.iloc[:,100:200])
y_test_z_scaled	= scaler_z.transform(y_test_xyz.iloc[:,200:300])


# Callbacks.
reduce_lr		= ReduceLROnPlateau(
	monitor		= 'val_loss',
  patience	= 20,
  factor		= 0.5
)

# definiciones Previas.
act_name	= 'relu'
l2_reg		= 0.0007
epochs		= 750
b_s				= 64
optimizer = Adam(learning_rate=0.001)

# Arquitectura.
inputs	= Input(shape=(5,))
encoded	= Dense(32,	 activation	= act_name, kernel_regularizer = l2(l2_reg))(inputs)
encoded = Dense(128, activation = act_name, kernel_regularizer = l2(l2_reg))(encoded)
encoded = Dense(256, activation = act_name, kernel_regularizer = l2(l2_reg))(encoded)
encoded = Dense(512, activation = act_name, kernel_regularizer = l2(l2_reg))(encoded)
encoded = Dense(512, activation = act_name, kernel_regularizer = l2(l2_reg))(encoded)

decoded_x = Dense(100, activation = 'linear', name = 'x')(encoded)
decoded_y = Dense(100, activation = 'linear', name = 'y')(encoded)
decoded_z = Dense(100, activation = 'linear', name = 'z')(encoded)

# Definición modelo con multiples salidas.
model_xyz = Model(inputs	= inputs, outputs=[decoded_x, decoded_y, decoded_z])
model_xyz.compile(optimizer = optimizer, loss = 'mae')
model_xyz.summary()

# Entrenamiento.
history_xyz = model_xyz.fit(x_train,
                            [y_train_x_scaled,
                            y_train_y_scaled,
                            y_train_z_scaled],
                            epochs						= epochs,
														batch_size				= b_s,
                            validation_split	= 0.1,
                            callbacks					= [reduce_lr],
                          	)


loss = model_xyz.evaluate(x_test,[y_test_x_scaled,
																	y_test_y_scaled,
																	y_test_z_scaled],
													)