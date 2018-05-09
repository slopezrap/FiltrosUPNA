from django.urls import path
from . import views

urlpatterns = [
    path('', views.VistaBlog, name='name-blog'),
]

