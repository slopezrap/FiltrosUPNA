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
#---------------- FUNCIONES ----------------#
def Vista404(request):
    template = "AppCore/404.html"
    nombre_pestania = "404"
    if request.method == "GET":
        contexto = {
            "clave_nombre_pestania" : nombre_pestania,
            "clave_error_404": "Se ha producido un error 404"
            }
        return render(request, template , contexto)


#---------------- CLASES ----------------#
class VistaAbout(TemplateView):
    template_name = "AppCore/About.html"

    def get(self,request,*args,**kwargs):
        contexto = {
            'clave_nombre_pestania' : "About",
                }
        return render(request,self.template_name,contexto)
 
class VistaHome(TemplateView):
    template_name = "AppCore/Home.html"
    
    def get(self,request,*args,**kwargs):
        contexto = {
            'clave_nombre_pestania' : "Inicio",
                }
        return render(request,self.template_name,contexto)

class VistaPortfolio(TemplateView):
    template_name = "AppCore/Portfolio.html"
   
    def get(self,request,*args,**kwargs):
        contexto = {
            'clave_nombre_pestania' : "Portfolio",
                }
        return render(request,self.template_name,contexto)

