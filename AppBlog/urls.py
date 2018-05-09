from django.urls import path
from . import views

urlpatterns = [
    path('', views.VistaBlog, name='name-blog'),
    #<int:category_id>: Un dato dinamico que se le pasa como parametro a VistaCategoria en category_id y le fuerzo a ser entero con int:
    path('categoria/<int:category_id>/',views.VistaCategoria, name='name-categoria'),
]

