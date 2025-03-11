### PREGUNTAR
## sobre Ray_tracing.py
  Cuando se procede a Graficar la muestra sin interpolar, los valores obtenidos de la transformación de X_Y_Z en 
sistema cartesiano, en Z si existen para sus valores iniciales y finales, valores Negativos.
## sobre pruebas.py
La obtención de la gráfica la considero correcta, éste conjunto pasa por un filtro que quita las tuplas que poseen
elevación Negativa(functions.py -> filter_unique_coordinates() and filter_on_elevations()).
Luego a la hora de graficar las coordenadas cartesianas interpoladas se obtiene una grafica Recta ya que el valor de Z cartesiano
es Negativo descendente NO logro entender a que se puede deber éste tema.
Es decir estoy usando la misma funcion para graficar el conjunto filtrado y luego el conjunto interpolado.
##
  A que se debe en el plot Gral. en Ray_tracing.py se realiza la doble conversión en np.radians(), si lo que tenemos en phi y 
theta ya están en radianes (ALMENOS así lo entiendo yo).
## Por otro lado cuando se realiza la interpolación sobre X Y Z (desde Ray_tracing.py)se obtienen valores bonitos de ver.
pero éstos se encuentran en sistema cartesiano. El problema que considero 



#Lectura
página: https://botpress.com/es/blog/deep-neural-network

Redes Neuronales Profundas: 
  Las redes de aprendizaje profundo utilizan "Big Data" junto con algoritmos para resolver un problema, y estas 
  redes neuronales profundas pueden resolver problemas con una aportación humana limitada o nula.

  La red neuronal se llama así porque existe una similitud entre este enfoque de programación y la forma en que funciona el cerebro.

  Al igual que el cerebro, los algoritmos de redes neuronales utilizan una red de neuronas o nodos. Al igual que el cerebro, estas 
  neuronas son funciones discretas (o maquinitas, si se prefiere) que reciben entradas y generan salidas. Estos nodos se organizan en 
  capas, de forma que las salidas de las neuronas de una capa se convierten en las entradas de las neuronas de la capa siguiente hasta 
  que las neuronas de la capa exterior de la red generan el resultado final.

  Por lo tanto, hay capas de neuronas en las que cada una recibe entradas muy limitadas y genera salidas muy limitadas, como en el cerebro.
  La primera capa de neuronas (o capa de entrada) recibe las entradas y la última capa de neuronas (o capa de salida) emite el resultado.


  ## Gestión de datos con TensorFlow()
Extraer ================Transformar================Cargar

Extraer: Leer datos en diferentes formatos del disco y  sin importar su tamaño enviarlos a la RAM
Transformar: pre-procesar, mezclar, crear, lotes, ... tf.Data
cargar: llevar al modelo

Que es Tensor ? Sencillamente un arreglo Númerico
.take(): Toma uan cantidad finita del dataset
.filter(): Condición Ex lambda y : y > 0
.map(lambda x: x/10) : Para realizar Escalado

ver el siguiente colab:
https://colab.research.google.com/drive/1dUvL1J6kQjvoJAzvXwjFvxRhNV5MzcdA?usp=sharing


# 02-10-2024

## Escalamiento, Normalización y Estandarización 

## 1. Escalamiento (Scaling)
El **escalamiento** cambia el rango de los valores de las variables p ara hacer que estén dentro de un intervalo específico. Esta técnica es útil cuando las variables tienen difereetnes unidades o escalas, lo que pude desbalancear el aprendizaje de los algoritmos. Los métodos de escalamiento más comunes son:
* **Min-Max Scaling**: Escala los datos para que estén entre un valor mínimo y máximo, usualmente entre 0 y 1. Se calcula con la fórmula:
$$X_{scaled}= \frac{X - X{min}}{X_{max}-X_{min}}$$
Esto es útil cuando las variables tienen difernetes rangos y se desea mantener la dispersión relativa de los valores. 

## 2. Normalización (Normalization)
La **Normalización** transforma los datos para que la suma de los valores cuadrados sea igual a 1. A menudo se usa en técnicas como redes neuronales y métodos de distancias como k-NN o SVM, donde es importante que las magnitudes de las características no dominen el cálculo de distancias.
Existen diferetnes tipos de normalización, pero la más común es la normalización por norma $L^2$, que usa la fórmula: 
$$X_{nom}=\frac{X}{\sqrt{\sum X^2}}$$
Esto es útil cuando los datos tienen una distribución dispersa o no uniforme. 
## 3. Estandarización (Standardization)
La **estandarización** ajusta los valores de los datos para que tengan una **media de 0** y una **desviaciión estándar de 1**. Este método es útil para algoritmos basados en gradientes como regresión logistica, redes neuronales y SVM, donde la distribución de los datos debe ser uniforme para evitar sesgos en el entrenamiento. Se calcula con la fórmula: 
$$X_{std} =\frac{X - \mu}{\sigma}$$
donde $\mu$ es la media de los datos y $\sigma$ es la desviación estándar.

### Diferencias Clave 
* **Escalamiento** ajusta los datos dentro de un rango específico (0 a 1).
* **Normalización** ajusta los valores para que estén en una norma unitaria (módulo 1).
* **Estandarización** ajusta los valores para que tengan media 0 y desviación estándar 1.

### Cuando usar cada Técnica
* **Escalamiento (Min-Max)**: Es útil para algoritmos basados en rangos como k-NN, redes neuronales, y en modelos donde la distancia es importante.
* **Normalización**: Se usa cuando las características deben ser comparadas proporcionalmente en base a su magnitud, como en el caso de redes neuronales y SVM.
* **Estanrazación**: Es recomendable para algoritmos que asumen que los datos son gaussianos, como regresión lineal, k-means, PCA, y SVM. 

## Referencias
* Raschka, Sebastian & Mirjalili, Vahid. Python Machine Learning (3rd Edition). Packt Publishing, 2019.
* Géron, Aurélien. Hands-On Machine Learning with Scikit-Learn, Keras, and TensorFlow. O'Reilly Media, 2019.
* Brownlee, Jason. "A Gentle Introduction to Normalization of Datasets in Machine Learning." Machine Learning Mastery, 2017.

## 06/10/24
# Normalización vs Estandarización 
### *Normalización y Estandarización en Modelos de Machine Learning y Series de Tiempo: Mejorando el **Rendimiento** y la **Interpretación*** 
## Normalización (VER SI ES CORRECTO)
La normalización es un proceso que ajusta los valores de una característica para que se encuentren dentro de un rango específico, generalmente entre 0 y 1. Esto se logra restando el valor mínimo de la característica y dividiendo por la diferencia entre el valor máximo y el valor mínimo. La normalización es útil cuando los datos tienen diferentes escalas y rangos, lo que puede afectar el rendimiento de algunos algoritmos de Machine Learning.

En el caso de las Series de Tiempo, la normalización puede ser especialmente importante cuando se trabaja con varias series que tienen diferentes unidades de medida o magnitudes. Al normalizar cada serie individualmente, se logra una comparación más justa y se evita que una serie domine sobre las demás debido a su escala.

## Estandarización: 
La estandarización es un proceso que transforma los valores de una característica para que tengan una media cero y una desviación estándar de uno. Esto se logra restando la media de la característica y dividiendo por la desviación estándar. A diferencia de la normalización, la estandarización no restringe los valores a un rango específico, lo que puede ser beneficioso en algunos algoritmos que asumen una distribución normal de los datos.

En el contexto de las Series de Tiempo, la estandarización puede ser especialmente útil cuando se trabaja con algoritmos que se basan en la suposición de normalidad, como los modelos ARIMA. Al estandarizar las series, se pueden cumplir mejor los supuestos de estos modelos y obtener resultados más confiables.

## Beneficios y consideraciones
1. Mejora del rendimiento del modelo: La normalización y la estandarización pueden mejorar el rendimiento de los modelos de Machine Learning al garantizar que todas las características tengan un impacto equilibrado en el proceso de aprendizaje. Al tener características en una escala común, los modelos pueden converger más rápido y ser más eficientes.
2. Facilita la interpretación: Al normalizar o estandarizar los datos, las características estarán en una escala comparable, lo que facilita la interpretación de los coeficientes o pesos asignados a cada característica en el modelo. Esto permite identificar qué características tienen una mayor influencia en las predicciones del modelo.
3. Reducción de sesgos: La normalización y la estandarización también pueden ayudar a reducir el impacto de los valores atípicos o outliers en el modelo. Al escalar los datos, estos valores extremos tendrán menos influencia en la distribución general de los datos.

**Es importante tener en cuenta que la normalización y la estandarización deben aplicarse después de dividir los datos en conjuntos de entrenamiento y prueba. Esto evita filtrar información del conjunto de prueba hacia el conjunto de entrenamiento y garantiza una evaluación imparcial del modelo.**

![YA_NO_ESTA_LA_IMAGEN_F](/Teoria/imagenes/Normalizacion_vs_Estandarizacion.png)

La normalización y la estandarización son técnicas esenciales en el preprocesamiento de datos para modelos de Machine Learning y Series de Tiempo. Estas técnicas garantizan que las características estén en una escala común, lo que mejora el rendimiento de los modelos y facilita la interpretación de los resultados.

Ya sea para equilibrar características con diferentes escalas, garantizar la suposición de normalidad en ciertos algoritmos o reducir el impacto de valores atípicos, la normalización y la estandarización desempeñan un papel crucial en la construcción de modelos más precisos y confiables.

Al aplicar estas técnicas, es importante considerar el contexto del problema, la distribución de los datos y los supuestos del modelo utilizado. Además, se recomienda realizar experimentos comparativos utilizando diferentes enfoques de normalización y estandarización para evaluar su impacto en el rendimiento del modelo.

En última instancia, al aprovecharlas ventajas de la normalización y la estandarización, los profesionales del Machine Learning y las Series de Tiempo pueden obtener resultados más sólidos y confiables, lo que a su vez facilita la toma de decisiones informadas en una amplia gama de aplicaciones y dominios.

[REFERENCIA](https://www.linkedin.com/posts/naren-castellon-1541b8101_normalizaci%C3%B3n-y-estandarizaci%C3%B3n-en-modelos-activity-7154235226783641600-iV37/?originalSubdomain=es)


## Validation_stlit
El parámetro validation_split en el método .fit() de Keras controla qué porcentaje de tus datos de entrenamiento (x_train y y train) se reserva para 
validar el modelo durante el entrenamiento. Esto significa que separa la pérdida y las métricas en un conjunto de validación después de cada época, sin usar lso datos de prueba explícitos.

### Propósito del validation_split:
* Evalúa el rendimineto del modelo en datos que no está usando directamente para ajustar los pesos(es decir, datos que el modelo no ha "visto").
* Ayuda a monitorear problemas como el sobreajuste (cuando el modelo
aprende demasiado bien los datos de entrenamiento pero generaliza 
mal a nuevos datos).
* Permite ajustar hiperpáramentros como la arquitectura, la tasa de aprendizaje, etc., sin necesidad de usar el conjunto de prueba.