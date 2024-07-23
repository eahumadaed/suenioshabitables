from django.contrib import admin
from django.urls import path, include
from inmuebles import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.home, name='home'),
    path('explorar/', views.explorar, name='explorar'),
    path('about/', views.about, name='about'),
    path('inmueble/<int:id>/', views.inmueble, name='inmueble'),
    path('registrar/', views.registrar, name='registrar'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('logout_success/', views.logout_success, name='logout_success'),
    
    #apis
    path('api/comunas/<int:region_id>/', views.api_comunas, name='api_comunas'),
    path('api/arrendar/', views.api_arrendar_inmueble, name='api_arrendar_inmueble'),
    
    

    #dashboarddashboarddashboarddashboarddashboarddashboarddashboarddashboarddashboarddashboarddashboarddashboarddashboarddashboarddashboard
    path('dashboard/', views.dashboard, name='dashboard'),
    path('dashboard/agregar_inmueble/', views.agregar_inmueble, name='agregar_inmueble'),
    path('dashboard/mis_inmuebles/', views.mis_inmuebles, name='mis_inmuebles'),
    path('dashboard/modificar_inmueble/<int:inmueble_id>/', views.modificar_inmueble, name='modificar_inmueble'),
    path('dashboard/eliminar_inmueble/<int:inmueble_id>/', views.eliminar_inmueble, name='eliminar_inmueble'),
    path('dashboard/agregar_imagen/<int:inmueble_id>/', views.agregar_imagen, name='agregar_imagen'),
]