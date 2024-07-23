import django
import os
import sys

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'suenioshabitables.settings')
django.setup()

from inmuebles.service import cargar_regiones_y_comunas, crear_usuarios_y_inmuebles

if __name__ == '__main__':
    #cargar_regiones_y_comunas()
    crear_usuarios_y_inmuebles()
    print("Datos cargados exitosamente.")
