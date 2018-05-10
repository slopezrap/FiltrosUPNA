from django.urls import path
from .views import VistaAbout, VistaHome, VistaPortfolio

urlpatterns = [
    path('', VistaHome.as_view(), name='name-home'),
    path('about-us/', VistaAbout.as_view(), name='name-about'),
    path('portfolio/', VistaPortfolio.as_view(), name='name-portfolio'),
]