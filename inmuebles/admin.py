from django.contrib import admin
from .models import Region, Comuna, Usuario, Inmueble, InmuebleImagen, Transaccion

admin.site.register(Region)
admin.site.register(Comuna)
admin.site.register(Usuario)
admin.site.register(Inmueble)
admin.site.register(InmuebleImagen)
admin.site.register(Transaccion)