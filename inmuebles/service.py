import json
import requests
import random
from .models import Region, Comuna, Usuario, Inmueble, InmuebleImagen


def cargar_regiones_y_comunas():
    URL_COMUNAS_REGIONES = 'https://gist.githubusercontent.com/juanbrujo/0fd2f4d126b3ce5a95a7dd1f28b3d8dd/raw/b8575eb82dce974fd2647f46819a7568278396bd/comunas-regiones.json'
    response = requests.get(URL_COMUNAS_REGIONES)
    data = response.json()

    orden = 1
    for region_data in data['regiones']:
        nombre_region = region_data['region']
        region = Region.objects.create(nombre=nombre_region, orden=orden)
        orden += 1
        for comuna_data in region_data['comunas']:
            Comuna.objects.create(nombre=comuna_data, region=region)

def crear_usuarios_y_inmuebles():
    # Crear usuarios
    arrendador = Usuario.objects.create_user(
        email='arrendador@example.com',
        password='arrendador123',
        nombres='Juan',
        apellidos='Pérez',
        rut=12345678,
        dv='9',
        direccion='Avenida Siempre Viva 123',
        comuna=Comuna.objects.order_by('?').first(),
        region=Region.objects.order_by('?').first(),
        telefono_personal='123456789',
        tipo_usuario='Arrendador',
        avatar='assets/images/clients/c1.png'
    )

    arrendatario = Usuario.objects.create_user(
        email='arrendatario@example.com',
        password='arrendatario123',
        nombres='Ana',
        apellidos='García',
        rut=87654321,
        dv='K',
        direccion='Calle Falsa 456',
        comuna=Comuna.objects.order_by('?').first(),
        region=Region.objects.order_by('?').first(),
        telefono_personal='987654321',
        tipo_usuario='Arrendatario',
        avatar='assets/images/clients/c2.png'
    )

    # Crear inmuebles
    imagenes = ['e1.jpg', 'e2.jpg', 'e3.jpg', 'e4.jpg', 'e5.jpg', 'e6.jpg']
    for i in range(20):
        inmueble = Inmueble.objects.create(
            nombre=f'Inmueble Ficticio {i+1}',
            descripcion='Este es un inmueble de prueba creado para testing.',
            m2_construidos=100 + i,
            m2_totales=200 + i,
            cantidad_estacionamientos=1,
            cantidad_habitaciones=3,
            cantidad_banos=2,
            direccion=f'Calle de Prueba {i+1}',
            comuna=Comuna.objects.order_by('?').first(),
            region=Region.objects.order_by('?').first(),
            tipo_inmueble='casa',
            precio_mensual_arriendo=500000 + i * 10000,
            arrendatario=arrendatario,
            estado='Disponible' if i % 2 == 0 else 'Arrendada'
        )

        num_imagenes = random.randint(1, 3)
        for _ in range(num_imagenes):
            imagen = random.choice(imagenes)
            InmuebleImagen.objects.create(
                ruta=f'assets/images/explore/{imagen}',
                inmueble=inmueble
            )
