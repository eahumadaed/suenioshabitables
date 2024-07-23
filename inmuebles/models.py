from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager

class Region(models.Model):
    nombre = models.CharField(max_length=255)
    orden = models.IntegerField()

    def __str__(self):
        return self.nombre

class Comuna(models.Model):
    nombre = models.CharField(max_length=255)
    region = models.ForeignKey(Region, on_delete=models.CASCADE)

    def __str__(self):
        return self.nombre

class UserManager(BaseUserManager):
    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError('El email es obligatorio')
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        return self.create_user(email, password, **extra_fields)

class Usuario(AbstractBaseUser):
    TIPO_USUARIO_CHOICES = [
        ('Arrendador', 'Arrendador'),
        ('Arrendatario', 'Arrendatario'),
    ]

    nombres = models.CharField(max_length=255)
    apellidos = models.CharField(max_length=255)
    rut = models.BigIntegerField(unique=True)
    dv = models.CharField(max_length=1)
    direccion = models.CharField(max_length=255, null=True, blank=True)
    comuna = models.ForeignKey(Comuna, on_delete=models.CASCADE)
    region = models.ForeignKey(Region, on_delete=models.CASCADE)
    telefono_personal = models.CharField(max_length=20, null=True, blank=True)
    email = models.EmailField(unique=True)
    avatar = models.CharField(max_length=255, null=True, blank=True)
    fecha_registro = models.DateTimeField(auto_now_add=True)
    tipo_usuario = models.CharField(max_length=20, choices=TIPO_USUARIO_CHOICES)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)

    objects = UserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['nombres', 'apellidos', 'rut', 'dv', 'comuna', 'region', 'tipo_usuario']

    def __str__(self):
        return f'{self.nombres} {self.apellidos}'

class Inmueble(models.Model):
    ESTADO_CHOICES = [
        ('Arrendada', 'Arrendada'),
        ('Disponible', 'Disponible'),
        ('Eliminada', 'Eliminada'),
    ]

    nombre = models.CharField(max_length=255)
    descripcion = models.TextField()
    m2_construidos = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    m2_totales = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    cantidad_estacionamientos = models.IntegerField(null=True, blank=True)
    cantidad_habitaciones = models.IntegerField(null=True, blank=True)
    cantidad_banos = models.IntegerField(null=True, blank=True)
    direccion = models.CharField(max_length=255)
    comuna = models.ForeignKey(Comuna, on_delete=models.CASCADE)
    region = models.ForeignKey(Region, on_delete=models.CASCADE)
    tipo_inmueble = models.CharField(max_length=255, choices=[('casa', 'Casa'), ('departamento', 'Departamento'), ('oficina', 'Oficina')])
    precio_mensual_arriendo = models.DecimalField(max_digits=10, decimal_places=2)
    arrendatario = models.ForeignKey(Usuario, on_delete=models.CASCADE)
    estado = models.CharField(max_length=255, choices=ESTADO_CHOICES)

    def __str__(self):
        return self.nombre

class InmuebleImagen(models.Model):
    ruta = models.CharField(max_length=255)
    inmueble = models.ForeignKey(Inmueble, on_delete=models.CASCADE)

    def __str__(self):
        return self.ruta

class Transaccion(models.Model):
    usuario_arrendador = models.ForeignKey(Usuario, on_delete=models.CASCADE)
    inmueble = models.ForeignKey(Inmueble, on_delete=models.CASCADE)
    fecha_inicio = models.DateTimeField(auto_now_add=True)
    fecha_fin = models.DateField(null=True, blank=True)

    def __str__(self):
        return f'Transacción {self.id} - {self.inmueble.nombre}'
