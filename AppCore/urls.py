from django.urls import path
from . import views

urlpatterns = [
    path('', views.VistaHome, name='name-home'),
    path('about-us/', views.VistaAbout, name='name-about'),
    path('portfolio/', views.VistaPortfolio, name='name-portfolio'),
]