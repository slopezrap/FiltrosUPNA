from django.urls import path
from . import views


urlpatterns = [
    
    path('crearFPBajo/', views.VistaCrearFPBajo, name='name-CrearFPBajo'),
    path('Crear_FPB/',views.Crear_Filtro_Paso_Bajo, name='Creacion_FPB'),
    
]

