from django import forms
from .models import Usuario, Inmueble, InmuebleImagen

class RegistroForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput, label="Contraseña")
    confirm_password = forms.CharField(widget=forms.PasswordInput, label="Confirmar Contraseña")

    class Meta:
        model = Usuario
        fields = ['nombres', 'apellidos', 'email', 'rut', 'dv', 'direccion', 'comuna', 'region', 'telefono_personal', 'tipo_usuario']

    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get("password")
        confirm_password = cleaned_data.get("confirm_password")

        if password != confirm_password:
            raise forms.ValidationError("Las contraseñas no coinciden.")



class InmuebleForm(forms.ModelForm):
    class Meta:
        model = Inmueble
        fields = ['nombre', 'descripcion', 'm2_construidos', 'm2_totales', 'cantidad_estacionamientos', 'cantidad_habitaciones', 'cantidad_banos', 'direccion', 'region','comuna', 'tipo_inmueble', 'precio_mensual_arriendo', 'estado']

class InmuebleImagenForm(forms.ModelForm):
    class Meta:
        model = InmuebleImagen
        fields = ['ruta', 'inmueble']
        widgets = {
            'inmueble': forms.HiddenInput()
        }