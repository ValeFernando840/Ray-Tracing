
# Solución al error "No module named 'tensorflow'" en entorno virtual

## Problema
Al ejecutar un script en Python, aparece el error:
```
ModuleNotFoundError: No module named 'tensorflow'
```

Al verificar el intérprete con:
```python
import sys
print(sys.executable)
```
La ruta obtenida fue:
```
C:\Users\Alexis\AppData\Local\Programs\Python\Python312\python.exe
```
Esto indica que se está utilizando la instalación global de Python en lugar del entorno virtual.

## Solución

### 1) Activar el entorno virtual manualmente
Ejecuta en la terminal:
```
f:\Ray_Tracing-main\venv\Scripts\activate
```

Si usas PowerShell:
```
f:\Ray_Tracing-main\venv\Scripts\Activate.ps1
```

Si usas Git Bash:
```
source f:/Ray_Tracing-main/venv/Scripts/activate
```

Verifica que el entorno esté activado ejecutando:
```python
python -c "import sys; print(sys.executable)"
```
Debe mostrar algo como:
```
f:\Ray_Tracing-main\venv\Scripts\python.exe
```

### 2) Reinstalar TensorFlow en el entorno virtual
Si ya estás en el entorno virtual, instala TensorFlow con:
```
pip install tensorflow
```

Si sigue sin funcionar:
```
pip uninstall tensorflow
pip install tensorflow
```

### 3) Ejecutar el script con el Python correcto
Usa el Python del entorno virtual en lugar del global:
```
f:\Ray_Tracing-main\venv\Scripts\python.exe f:\Ray_Tracing-main\Graficas 1D y 3D\Graficando_1D_3D.py
```

### 4) Configurar VSCode correctamente
Si usas VSCode:
1. Presiona `Ctrl + Shift + P`
2. Escribe `"Python: Select Interpreter"`
3. Selecciona la versión dentro de `venv`.
