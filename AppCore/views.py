from django.shortcuts import render
from django.views.generic.base import TemplateView
# Create your views here.
"""
#---------------- FUNCIONES ----------------#
def VistaAbout(request):
    return render(request,"AppCore/About.html")

def VistaHome(request):
    return render(request,"AppCore/Home.html")

def VistaPortfolio(request):
    return render(request,"AppCore/Portfolio.html")
"""


#---------------- CLASES ----------------#
class VistaAbout(TemplateView):
    template_name = "AppCore/About.html"

    def get(self,request,*args,**kwargs):
        contexto = {
            'clave_cabecera_template' : "ABOUT",
                }
        return render(request,self.template_name,contexto)
 
class VistaHome(TemplateView):
    template_name = "AppCore/Home.html"
    
    def get(self,request,*args,**kwargs):
        contexto = {
            'clave_cabecera_template' : "HOME",
                }
        return render(request,self.template_name,contexto)

class VistaPortfolio(TemplateView):
    template_name = "AppCore/Portfolio.html"
   
    def get(self,request,*args,**kwargs):
        contexto = {
            'clave_cabecera_template' : "PORTFOLIO",
                }
        return render(request,self.template_name,contexto)

