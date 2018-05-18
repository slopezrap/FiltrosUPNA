from django.urls import path
from . import views


urlpatterns = [
    
    path('listado/', views.VistaListadoFiltros, name='name-ListadoFiltros'),
    
]