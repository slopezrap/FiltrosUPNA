from django.urls import path
from . import views
from .views import VistaAbout, VistaHome, VistaPortfolio

urlpatterns = [
    path('', VistaHome.as_view(), name='name-home'),
    path('404/', views.Vista404, name='name-404'),
    path('about-us/', VistaAbout.as_view(), name='name-about'),
    path('portfolio/', VistaPortfolio.as_view(), name='name-portfolio'),
]