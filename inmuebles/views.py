from django.shortcuts import render, get_object_or_404, redirect
from django.core.paginator import Paginator
from django.http import JsonResponse, HttpResponse
from django.contrib.auth import login as auth_login, logout, authenticate
import time
from .models import Inmueble, Comuna, Region, Usuario, Transaccion, InmuebleImagen
from .forms import RegistroForm, InmuebleForm, InmuebleImagenForm
from django.templatetags.static import static
from django.contrib.auth.forms import UserCreationForm
from django.views.decorators.csrf import csrf_exempt

from django.contrib.auth.decorators import login_required


def home(request):
    disponibles = Inmueble.objects.filter(estado='Disponible').order_by('-id')[:3]
    arrendados = Inmueble.objects.filter(estado='Arrendada').order_by('-id')[:3]
    regiones = Region.objects.all().order_by('orden')
    
    for inmueble in disponibles:
        inmueble.imagen_dinamica = static(inmueble.inmuebleimagen_set.first().ruta) if inmueble.inmuebleimagen_set.exists() else ''
    for inmueble in arrendados:
        inmueble.imagen_dinamica = static(inmueble.inmuebleimagen_set.first().ruta) if inmueble.inmuebleimagen_set.exists() else ''

    context = {
        'disponibles': disponibles,
        'arrendados': arrendados,
        'regiones': regiones,
    }
    return render(request, 'home.html', context)

def explorar(request):
    inmuebles = Inmueble.objects.all()
    region = request.GET.get('region')
    comuna = request.GET.get('comuna')
    tipo = request.GET.get('tipo')
 
    if region:
        inmuebles = inmuebles.filter(region__id=region)
    if comuna:
        inmuebles = inmuebles.filter(comuna__id=comuna)
    if tipo:
        inmuebles = inmuebles.filter(tipo_inmueble=tipo)

    disponibles = inmuebles.filter(estado='Disponible').order_by('-id')
    arrendados = inmuebles.filter(estado='Arrendada').order_by('-id')

    for inmueble in disponibles:
        inmueble.imagen_dinamica = static(inmueble.inmuebleimagen_set.first().ruta) if inmueble.inmuebleimagen_set.exists() else ''
    for inmueble in arrendados:
        inmueble.imagen_dinamica = static(inmueble.inmuebleimagen_set.first().ruta) if inmueble.inmuebleimagen_set.exists() else ''

    regiones = Region.objects.all().order_by('orden')
    
    context = {
        'disponibles': disponibles,
        'arrendados': arrendados,
        'regiones': regiones,
        'region_id':region,
        'comuna_id':comuna,
        'tipo':tipo
    }
    return render(request, 'explorar.html', context)


def inmueble(request, id):
    inmueble = get_object_or_404(Inmueble, id=id)
    user = request.user
    es_arrendador = 'Arrendador'
    if user.is_authenticated:  
        es_arrendador = user.tipo_usuario
    
    inmueble.imagen_dinamica = static(inmueble.inmuebleimagen_set.first().ruta) if inmueble.inmuebleimagen_set.exists() else ''
    
    
    context = {
        'inmueble': inmueble,
        'es_arrendador': es_arrendador,
    }
    return render(request, 'inmueble.html', context)


def registrar(request):
    if request.method == 'POST':
        form = RegistroForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.set_password(form.cleaned_data['password'])
            user.save()
            auth_login(request, user)
            return redirect('home')
    else:
        form = RegistroForm()
        
    comunas = Comuna.objects.all()
    regiones = Region.objects.all()        
    return render(request, 'registrar.html', {'form': form,  'comunas': comunas, 'regiones': regiones})

def about(request):
    return render(request, 'about.html')

def api_comunas(request, region_id):
    comunas = Comuna.objects.filter(region_id=region_id)
    comunas_list = list(comunas.values('id', 'nombre'))
    return JsonResponse(comunas_list, safe=False)

@csrf_exempt
def api_arrendar_inmueble(request):
    if request.method == 'POST' and request.user.is_authenticated:
        inmueble_id = request.POST.get('inmueble_id')
        try:
            inmueble = Inmueble.objects.get(id=inmueble_id, estado='Disponible')
            inmueble.estado = 'Arrendada'
            inmueble.arrendatario = request.user
            inmueble.save()
            Transaccion.objects.create(usuario_arrendador=request.user, inmueble=inmueble)
            return JsonResponse({'success': True})
        except Inmueble.DoesNotExist:
            return JsonResponse({'success': False, 'message': 'Inmueble no encontrado o no disponible.'})
    return JsonResponse({'success': False, 'message': 'Solicitud inválida.'})




def login_view(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')
        user = authenticate(request, email=email, password=password)
        if user is not None:
            auth_login(request, user)
            if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
                return JsonResponse({'success': True})
            else:
                return redirect('home')
        else:
            if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
                return JsonResponse({'success': False, 'message': 'Correo o contraseña incorrectos'})
            else:
                return render(request, 'login.html', {'error': 'Correo o contraseña incorrectos'})
    return render(request, 'login.html')

def logout_view(request):
    logout(request)
    return redirect('logout_success')

def logout_success(request):
    return render(request, 'logout_success.html')







@login_required
def dashboard(request):
    return render(request, 'dashboard_base.html')

@login_required
def agregar_inmueble(request):
    if request.method == 'POST':
        form = InmuebleForm(request.POST)
        if form.is_valid():
            inmueble = form.save(commit=False)
            inmueble.arrendatario = request.user
            inmueble.save()
            return redirect('mis_inmuebles')
    else:
        form = InmuebleForm()
    comunas = Comuna.objects.all()
    regiones = Region.objects.all()
    return render(request, 'agregar_inmueble.html', {'form': form, 'comunas': comunas, 'regiones': regiones})


@login_required
def mis_inmuebles(request):
    user = request.user
    es_arrendador = user.tipo_usuario == 'Arrendador'

    if es_arrendador:
        inmuebles = Inmueble.objects.filter(arrendatario=user)
    else:
        inmuebles = Inmueble.objects.all()

    return render(request, 'mis_inmuebles.html', {
        'inmuebles': inmuebles,
        'es_arrendador': es_arrendador
    })


@login_required
def modificar_inmueble(request, inmueble_id):
    inmueble = get_object_or_404(Inmueble, id=inmueble_id, arrendatario=request.user)
    if request.method == 'POST':
        form = InmuebleForm(request.POST, instance=inmueble)
        if form.is_valid():
            form.save()
            return redirect('mis_inmuebles')
    else:
        form = InmuebleForm(instance=inmueble)
    comunas = Comuna.objects.all()
    regiones = Region.objects.all()
    return render(request, 'modificar_inmueble.html', {'form': form, 'comunas': comunas, 'regiones': regiones})

@login_required
def eliminar_inmueble(request, inmueble_id):
    inmueble = get_object_or_404(Inmueble, id=inmueble_id, arrendatario=request.user)
    if request.method == 'POST':
        inmueble.delete()
        return redirect('mis_inmuebles')
    return render(request, 'eliminar_inmueble.html', {'inmueble': inmueble})

@login_required
def agregar_imagen(request, inmueble_id):
    inmueble = get_object_or_404(Inmueble, id=inmueble_id, arrendatario=request.user)
    if request.method == 'POST':
        form = InmuebleImagenForm(request.POST, request.FILES)
        if form.is_valid():
            imagen = form.save(commit=False)
            imagen.inmueble = inmueble
            imagen.save()
            return redirect('modificar_inmueble', inmueble_id=inmueble.id)
    else:
        form = InmuebleImagenForm()
    return render(request, 'agregar_imagen.html', {'form': form, 'inmueble': inmueble})