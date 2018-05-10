from django.urls import path
from . import views


urlpatterns = [
    
    path('', views.VistaBlog, name='name-blog'),
    path('crearEntrada/', views.VistaCrearEntradaBlog, name='name-crearEntrada'),
    path('detalleEntrada/', views.VistaDetalleEntradasBlog, name='name-detalleEntrada'),
    path('editarEntrada/<int:pk>/', views.VistaEditarEntradaBlog, name='name-editarEntrada'),
    path('borrarEntrada/<int:pk>/', views.VistaBorrarEntradaBlog, name='name-borrarEntrada'),
    
]

