from django.core.management.base import BaseCommand
from inmuebles.models import Inmueble, InmuebleImagen, Comuna, Region, Usuario
import random

class Command(BaseCommand):

    def handle(self, *args, **kwargs):
        self.clean_tables()
        self.create_inmuebles()

    def clean_tables(self):
        InmuebleImagen.objects.all().delete()
        Inmueble.objects.all().delete()

    def create_inmuebles(self):
        region_arica = Region.objects.get(id=1)
        region_metropolitana = Region.objects.get(id=16)
        comuna_arica = Comuna.objects.get(id=1)
        comuna_providencia = Comuna.objects.get(id=347)
        comuna_las_condes = Comuna.objects.get(id=348)

        usuario = Usuario.objects.filter(tipo_usuario='Arrendador').first()


        direcciones_arica = [
            "Avenida Santa María 1234", "Calle Los Olivos 567", "Pasaje Las Palmeras 89", 
            "Calle 21 de Mayo 101", "Avenida Brasil 202", "Calle Colón 303", 
            "Pasaje Los Pinos 404", "Avenida Libertador 505", "Calle El Golf 606", 
            "Pasaje Los Álamos 707", "Avenida Diego Portales 808"
        ]

        direcciones_providencia = [
            "Calle Los Leones 123", "Avenida Providencia 456", "Calle Suecia 789", 
            "Avenida Nueva Providencia 101", "Calle Pedro de Valdivia 202", "Avenida Andrés Bello 303", 
            "Calle Manuel Montt 404", "Avenida Tobalaba 505", "Calle Ricardo Lyon 606", 
            "Avenida Holanda 707", "Calle Antonio Varas 808"
        ]

        direcciones_las_condes = [
            "Avenida Apoquindo 123", "Calle El Golf 456", "Avenida Kennedy 789", 
            "Calle Las Verbenas 101", "Avenida Las Condes 202", "Calle San Sebastián 303", 
            "Avenida Vitacura 404", "Calle Los Militares 505", "Avenida Manquehue 606", 
            "Calle Cerro El Plomo 707", "Avenida Presidente Riesco 808"
        ]

        nombres_casas = [
            "Casa de dos pisos con jardín", "Casa moderna con piscina", "Casa familiar cerca de parque",
            "Casa tradicional con amplio terreno", "Casa rústica en zona tranquila", "Casa luminosa con patio",
            "Casa renovada con garaje", "Casa acogedora con terraza", "Casa con diseño arquitectónico único",
            "Casa minimalista con espacios abiertos", "Casa de lujo con acabados de alta calidad"
        ]

        nombres_departamentos = [
            "Departamento céntrico con vista", "Departamento moderno en edificio nuevo", "Departamento amplio con balcón",
            "Departamento con acabados de lujo", "Departamento en zona exclusiva", "Departamento cerca de transporte público",
            "Departamento con gimnasio y piscina", "Departamento en edificio seguro", "Departamento con espacios integrados",
            "Departamento amoblado y equipado", "Departamento con excelente iluminación"
        ]

        descripciones = [
            "Esta propiedad cuenta con todas las comodidades necesarias para una vida confortable.",
            "Ubicada en una zona tranquila, esta propiedad ofrece un ambiente relajante y acogedor.",
            "Con acabados de alta calidad, esta propiedad está lista para ser habitada.",
            "Disfrute de espacios amplios y luminosos en esta maravillosa propiedad.",
            "Perfecta para familias, esta propiedad ofrece seguridad y comodidad.",
            "Con una ubicación privilegiada, esta propiedad está cerca de todas las comodidades urbanas.",
            "Esta propiedad combina elegancia y funcionalidad en cada rincón.",
            "Con una excelente distribución de espacios, esta propiedad es ideal para vivir cómodamente.",
            "Equipado con las mejores instalaciones, este inmueble es una excelente opción para su próximo hogar.",
            "Esta propiedad ofrece una excelente relación entre calidad y precio."
        ]

        inmuebles_data = [
            (direcciones_arica, comuna_arica, region_arica),
            (direcciones_providencia, comuna_providencia, region_metropolitana),
            (direcciones_las_condes, comuna_las_condes, region_metropolitana)
        ]

        images_dir = 'assets/images/explore/'

        inmueble_count = 0

        for direcciones, comuna, region in inmuebles_data:
            for direccion in direcciones:
                if inmueble_count >= 37:
                    break

                if inmueble_count % 2 == 0:
                    nombre = random.choice(nombres_casas)
                    tipo_inmueble = 'casa'
                else:
                    nombre = random.choice(nombres_departamentos)
                    tipo_inmueble = 'departamento'

                descripcion = random.choice(descripciones)

                inmueble = Inmueble.objects.create(
                    nombre=nombre,
                    descripcion=descripcion,
                    m2_construidos=120,
                    m2_totales=200,
                    cantidad_estacionamientos=2,
                    cantidad_habitaciones=3,
                    cantidad_banos=2,
                    direccion=direccion,
                    comuna=comuna,
                    region=region,
                    tipo_inmueble=tipo_inmueble,
                    precio_mensual_arriendo=500000,
                    arrendatario=usuario,
                    estado='Disponible'
                )

                imagen_path = f'{images_dir}c{inmueble_count + 1}.jpg'
                InmuebleImagen.objects.create(
                    ruta=imagen_path,
                    inmueble=inmueble
                )

                inmueble_count += 1

        print("FINNNNNNNNNN")
