from django.urls import path
from . import views

urlpatterns = [
    path('', views.VistaContacto, name='name-contact'),
]

