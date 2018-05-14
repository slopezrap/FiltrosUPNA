from django.urls import path
from . import views


urlpatterns = [
    path('registrate/', views.VistaSignUp, name='name-signup'),
    path('login/', views.VistaLogin, name='name-login'),
    path('logout/', views.VistaLogout, name='name-logout'),
]

