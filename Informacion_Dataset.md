# <span style="color:#FF5733;">Información Dataset</span>

## <span style="color:#33A1FF;">Posición del Tx:</span>
- **latitude_tx**: -42.28  
- **longitude_tx**: -63.40  
- **elevation_tx**: 0  

## <span style="color:#33A1FF;">Primera parte del Dataset</span>
**Cantidad de Muestras**: 2190  

### <span style="color:#28B463;">Fijo:</span>
- **frecuencia**: 10 MHz  
- **elevation**: 5°  
- **azimuth**: 98°  
- **year**: 2010  

### <span style="color:#28B463;">Variable:</span>
- **mmdd**: [01/01 - 12/31] (saltos de 1 día)  
- **hour**: 4 valores → 0, 4, 12, 16, 20  

## <span style="color:#33A1FF;">Segunda Parte del Dataset</span>
**Cantidad de Muestras**: 2940  

### <span style="color:#28B463;">Fijo:</span>
- **year**: 2010  
- **mmdd**: 12/15  
- **hour**: 12 hs  

### <span style="color:#28B463;">Variable:</span>
- **frecuencia**: [3 - 30] MHz (saltos de 1 MHz)  
- **elevation**: [0 - 40]° (saltos de 2°)  
- **azimuth**: [87 - 91]° (saltos de 1°)  

## <span style="color:#33A1FF;">Muestras</span>
- **Total de muestras**: 5130  
- **Muestras para entrenar**: 4104  
- **Muestras para test**: 1026  

## <span style="color:#33A1FF;">Parámetros de Entrada</span>
- **latitude_pos_tx**  
- **longitude_pos_tx**  
- **elevation_pos_tx**  
- **fc**  
- **elevation**  
- **azimuth**  
- **year**  
- **mmdd**  
- **hour**  

## <span style="color:#33A1FF;">Parámetros de Salida</span>
- **x_1 - x_100**: 100 valores por fila  
- **y_1 - y_100**: 100 valores por fila  
- **z_1 - z_100**: 100 valores por fila  

# <span style="color:#FF5733;">Arquitectura Red Neuronal </span>

```python
from tensorflow.keras.models import Model
from tensorflow.keras.layers import Input, Dense
from tensorflow.keras.regularizers import l2

# Definir hiperparámetros
act_name = 'relu'  # Puedes cambiar la función de activación según sea necesario
l2_reg = 0.01  # Regularización L2

# Construcción del modelo de autoencoder
inputs = Input(shape=(9,))
encoded = Dense(9, activation=act_name, kernel_regularizer=l2(l2_reg))(inputs)
encoded = Dense(16, activation=act_name, kernel_regularizer=l2(l2_reg))(encoded)
encoded = Dense(32, activation=act_name, kernel_regularizer=l2(l2_reg))(encoded)
encoded = Dense(64, activation=act_name, kernel_regularizer=l2(l2_reg))(encoded)
encoded = Dense(80, activation=act_name, kernel_regularizer=l2(l2_reg))(encoded)
encoded = Dense(90, activation=act_name, kernel_regularizer=l2(l2_reg))(encoded)
decoded = Dense(100, activation='linear', kernel_regularizer=l2(l2_reg), name='y_output')(encoded)

autoencoder_y = Model(inputs, decoded)
````
