### Uso drop()
***drop()*** es una función incorporada en Pandas que te permite eliminar una o más **filas o columnas** de un Marco de Datos. Devuelve un nuevo Marco de Datos con las filas o columnas especificadas eliminadas y no modifica el Marco de Datos original en su lugar, a menos que establezcas el parámetro inplace en True .
##### División de los datos en conjuntos de entrenamiento y prueba
  `train_test_split` es una función que forma parte de la biblioteca de scikit-learn en el módulo `sklearn.model_selection`.
  Se lo usa comunmente para dividir un conjunto de datos en dos subconjuntos (entrenamiento y prueba)
#### Sus parámetros
* **Datos**(obligatorio): Conjunto de datos que se desea dividir. 
  ```python
    train_test_split(X,Y)
* **test_size**(opcional): Define el porcentaje o la cantidad de datos que se reserva para prueba. Si es 0.2 indica un 20% reservado para prueba.
  ```python
    train_test_split(X,Y, test_size=0.2)
* **train_size**(opcional): Especifica el tamaño del conjunto de Entrenamiento.
* **random_state**(opcional): Controla la aleatoridad de la división. Si se usa un valor fijo (`random_state=42`), la división siempre es la misma cada vez que se ejecute el código.
  ```python
    train_test_split(X, Y, test_size=0.2, random_state=42)
* **shuffle** (opcional): Especificsa si los datos deben ser barajados antes de ser divididos. Por defecto está en `True`. Es decir, los datos se mezclarán aleatoriamente antes de ser divididos.

### Explicando el modelo
La primera etapa consta de la importación de los módulos
```py
from tensorflow.keras.models import Model
from tensorflow.keras.layers import Input, Dense
```
#### 1. Importación de módulos
  * **Model**: Esta clase permite crear un modelo en Keras, especificando cuáles son las entradas y salidas de la red neuronal
  * **Input**: Representa la capa de entrada del modelo. Aquí se define cuántas características tendrá cada muestra de entrada.
  * **Dense**: Es una capa densa o completamente conectada, donde cada neurona está conectada a todas las neoronas de la capa anterior y posterior.

```py
inputs = Input(shape=(10,))
```
#### 2. Definición de la capa de entrada
  * input(shape=(10,)): Aquí se define la entrada del modelo, que tendrá 10 caracteristicas.
  Esto significa que cada muestra de entrada tendrá 10 valores, que corresponden a ***'latitude_pos_tx', 'longitude_pos_tx', 'elevation_pos_tx', 'fc', 'elevation', 'azimuth', 'year', 'mmdd', 'UTI', 'hour'***
```py
encoded = Dense(8, activation='relu')(inputs)
```
#### 3. Primera capa densa
  * **Dense(8, activation='relu')**: Esta es una capa densa con 8 neuronas. Aquí, cada una de las 10 entradas de la capa anterior se conecta a estas 8 neuronas.
  * **Función de activación 'relu'**: 'relu' (Rectified Linear Unit) es una función de activación que introduce no linealidad en el modelo. Convierte los valores negativos en 0 y deja pasar los valores positivos tal como están, lo que permite que la red aprenda patrones no lineales en los datos.
  * Esta capa está actuando como un **codificador**. Se está reduciendo la dimensionalidad de las características de entrada, condensando la información en 8 valores.

  ```py
  decoded = Dense(300, activation='linear')(encoded)
  ```
### 4. Segunda capa densa (decodificación)
  * **Dense(300, activation='linear')**: Esta capa tiene 300 neuronas, ya que el objetivo es generar los 100 puntos de salida, cada uno con 3 coordenadas (latitud, longitud y elevación), lo que da 300 valores en total.
  * **Función de activación 'linear'**: 'linear' significa que no hay transformación en los valores de salida; simplemente devuelve el valor calculado en la capa, lo cual es común en problemas de regresión (como este, donde estás prediciendo valores continuos).
  * Esta capa se usa para "reconstruir" la salida a partir de la representación comprimida en la capa anterior.

  ```pyth
  autoencoder = Model(inputs, decoded)
  ```
### 5. Creación del modelo
  * **Model(inputs, decoded)**: Aquí defines el modelo completo, especificando cuáles son las entradas (inputs) y las salidas (decoded).
  * El modelo se basa en una arquitectura de autoencoder, donde la primera parte del modelo (codificador) reduce la dimensionalidad de los datos y la segunda parte (decodificador) intenta reconstruir la salida original (en este caso, los 100 puntos geográficos).

  ```py
  autoencoder.compile(optimizer='adam', loss='mse')
  ```
### 6. Compilación del modelo
  * **compile(optimizer='adam', loss='mse')**: Aquí defines cómo se entrenará el modelo.
    * **optimizer='adam'**: Adam es un algoritmo de optimización popular y eficiente que ajusta los pesos del modelo en base al error de las predicciones. Es una versión mejorada del descenso de gradiente estocástico.
    * **loss='mse'**: La función de pérdida es el error cuadrático medio (MSE, Mean Squared Error), que mide qué tan lejos están las predicciones del modelo con respecto a los valores reales. En este caso, mide la distancia entre los 100 puntos predichos y los puntos reales del dataset.

  ```py
  autoencoder.summary()
  ```
### 7. Resumen del modelo
  * summary(): Esta línea imprime un resumen del modelo en la consola. Muestra cuántas capas tiene el modelo, cuántos parámetros se van a entrenar (pesos y bias), y el tamaño de las entradas y salidas de cada capa. Esto es útil para verificar si el modelo se ha construido correctamente.

## Entrenamiento y Prueba

### 1. Preparar los datos de entrada y salida
Considerando que los datos de entrada y salida ya se encuentran organizados, lo que sigue es dividir el dataset en conjutos de entrenamiento(x_train, y_train) y prueba (x_test, y_test)
```py
x_train,x_test,y_train,y_test = train_test_split(X,Y,test_size=0.2,random_state=42)
```
Por lo que tenemos un 80% para entrenamiento y un 20% para prueba.
### 2. Entrenar el modelo 
Con los datos de entrada y salida listos, entrenamos el modelo con la función fit(), que ajusta los pesos del modelo según los datos de entrenamiento.
```py
history = autoencoder.fit(x_train, y_train, 
                          epochs=50,           # Número de veces que el modelo verá todo el dataset
                          batch_size=32,        # Número de muestras que se entrenan antes de actualizar los pesos
                          validation_data=(x_test, y_test))  # Conjunto de validación para monitorear el rendimiento
```
### 3. Visualizar el proceso de entrenamiento
Podemos visualizar el rendimiento del entrenamiento usando el objeto history que devuelve **fit()**. Esto es útil para ver cómo evoluciona la función de pérdida (error) durante las épocas de entrenamiento.


## Epochs 
**Definición**: Una época es una pasada completa por todo el conjunto de datos de entrenamiento. Es decir, cuando cuando el modelo ha visto y procesado todos los ejemplos del cojunto de entrenamiento una vez, se ha completado una época.
**Cómo funciona**: Suponga que tiene 1000 muestras de datos de entrenamiento. Si defines que entrenarás tu red neuronal durante 10 épocas, esto significa que el modelo veráy ajustará sus pesos en esas 1000 muestras 10 veces en total.
**Importancia**: Cuanto mayor sea el número de épocas, más oportunidades tiene el modelo para ajustar sus pesos y mejorar su precisión. Sin embargo, más épocas no siempre equivalen a mejor rendimiento, ya que entrenar demasiadas veces puede llevar a sobreajuste (overfitting), donde el modelo memoriza el conjunto de entrenamiento pero no generaliza bien a datos nuevos.

## Batch_size (Tamaño de lote)
**Definición**: El tamaño de lote se refiere al número de muestras que el modelo procesa antes de actualizar sus pesos. Es decir, en lugar de calcular el error y ajustar los pesos después de cada muestra, el modelo lo hace después de procesar un lote de muestras.
**Cómo funciona**: Supón que tienes las mismas 1000 muestras de datos. Si el batch_size es de 100, entonces el conjunto de entrenamiento se dividirá en 10 lotes de 100 muestras cada uno. El modelo procesa un lote, calcula el error, ajusta sus pesos, y luego pasa al siguiente lote. Una vez que haya procesado los 10 lotes, se completará una época.

**Importancia**: El batch_size afecta el rendimiento y la eficiencia del entrenamiento.
* Un batch_size pequeño (32 o 64) genera actualizaciones más frecuentes de los pesos, lo que puede conducir a un aprendizaje más detallado, pero más lento.
* Un batch_size grande (256 o 512) puede aprovechar mejor el hardware (como las GPUs), pero las actualizaciones de los pesos serán menos frecuentes, lo que puede ralentizar el aprendizaje.

## Resumiendo el proceso
1. **Época completa**: Cada ejemplo del conjunto de datos se usa una vez en una época. Si tienes 1,000 muestras y el batch_size es 100, se necesitarán 10 lotes para completar una época.

2. **Lote (batch)**: Dentro de una época, el conjunto de datos se divide en lotes. Si tienes un lote de 100 muestras, el modelo ajusta sus pesos después de procesar ese lote completo.

3. **Actualización de los pesos**: El modelo ajusta sus parámetros (pesos) después de cada lote, no después de cada muestra individual.

## Relación entre épocas, lotes y  actualizaciones
Si entrenas el modelo durante 10 épocas con un batch_size de 100 en un conjunto de datos de 1,000 muestras:
* Cada época consta de 10 lotes.
* En cada lote, el modelo procesa 100 muestras y ajusta sus pesos.
* Al final de las 10 épocas, el modelo habrá ajustado sus pesos 100 veces (10 lotes por 10 épocas).

## Elección entre epochs y batch_size
* Épocas (epochs):
  * Si defines pocas épocas, el modelo puede no aprender lo suficiente (subentrenamiento).
  * Si defines demasiadas épocas, el modelo podría memorizar los datos (sobreajuste).
* Tamaño de lote (batch_size):
  * Un tamaño de lote pequeño tiende a hacer que el entrenamiento sea más ruidoso, pero más preciso en términos de convergencia.
  * Un tamaño de lote grande hace que el entrenamiento sea más rápido, pero puede perderse detalles y hacer que el modelo tarde más en aprender.

**Resumiendo**, ***epochs*** es cuántas veces el modelo verá el conjunto de datos completo durante el entrenamiento, y ***batch_size*** es cuántas muestras el modelo procesará antes de ajustar sus parámetros. Ambos parámetros son claves para determinar cómo de rápido y bien aprenderá la red neuronal.

# Como guardar un modelo
Para guardar un modelo en **TensorFlow**, se puede usar la función model.save() de Keras. TensorFlow permite guardar el modelo completo en un solo archivo o en un directorio, que incluye:
1. La arquitectura del modelo.
2. Los pesos del modelo.
3. La configuración de entrenamiento (si se utilizo *compile*).
4. El optimizador y su estado (para poder reanudar el entrenamiento si es necesario).

### Procedimiento
```python
model.save('mi_modelo.h5')
```
Este comando guarda el modelo en un solo archivo HDF5(formato .h5),
que es un método común para guardar modelos en TensorFlow. Si se 
prefiere el formato carpeta(más común en versiones recientes de 
TensorFlow), puedes hacer lo siguiente:
```python
model.save('mi_modelo')
```
Con esto creamos una carpeta *mi_modelo/* que contiene todo lo necesario 
para la restauración del modelo.

## Cargamos el modelo
Para la carga del modelo guardado, usamos `tf.keras.load_model`:
```python
import tensorflow as tf

# Si cargamos desde un Archivo .h5
modelo_cargado = tf.keras.models.load_model('mi_modelo.h5')

# si cargamos desde una Carpeta
modelo_cargado = tf.keras.models.load_model('mi_modelo')
```
Luego de cargar el modelo, podemos realizar predicciones, evaluaciones o continuar con el entrenamiento si fuese necesario. 
