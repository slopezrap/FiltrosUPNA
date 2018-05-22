# encoding: utf-8
# encoding: iso-8859-1
# encoding: win-1252

from django.shortcuts import render,redirect
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from django.http.response import HttpResponse
from .models import ModeloFPBajo
from .forms import FormularioFPBajo
# Create your views here.

    
@login_required(login_url="/accounts/login/")
def VistaCrearFPBajo(request):
    if request.method == "GET":
        template = "AppFPBajo/CrearFPBajo.html"
        nombre_pestania = "Crear FPBajo"
        
        contexto = {
            "clave_nombre_pestania" : nombre_pestania,
            }
        return render(request, template , contexto)
    


   

#Cambiar en un futuro por una clase
def Crear_Filtro_Paso_Bajo(request):
    if request.method == "GET":
        template = "AppFPBajo/Crear_Filtro_Paso_Bajo.html"
        nombre_pestania = "Crear FPBajo"
        formulario = FormularioFPBajo()
        contexto = {
            "clave_nombre_pestania" : nombre_pestania,
            'clave_variablesFPBajo_template':formulario,
            }
        return render(request, template , contexto)