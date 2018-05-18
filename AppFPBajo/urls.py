from django.urls import path
from . import views


urlpatterns = [
    
    path('crearFPBajo/', views.VistaCrearFPBajo, name='name-CrearFPBajo'),
    
]

