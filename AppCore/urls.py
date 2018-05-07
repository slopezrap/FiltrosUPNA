from django.urls import path
from . import views

urlpatterns = [
    path('', views.VistaHome, name='name-home'),
    path('about-me/', views.VistaAbout, name='name-about'),
    path('portfolio/', views.VistaPortfolio, name='name-portfolio'),
    path('contact/', views.VistaContacto, name='name-contact'),
]