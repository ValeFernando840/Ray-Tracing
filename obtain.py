import os


direccion= os.getcwd()
direccion = str(direccion)
nueva = r'\ray_tracing\dist\Release\Cygwin_1-Windows'
nuevaDireccion = direccion+nueva
print("nueva direccion: ", nuevaDireccion, type(direccion))

dir = os.getcwd()
nueva = "ray_tracing/dist/Release/Cygwin_1-Windows"
nuevaDireccion = os.path.join(dir, nueva)
os.chdir(nuevaDireccion)
