# encoding: utf-8
# encoding: iso-8859-1
# encoding: win-1252

from django.shortcuts import render,redirect
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from django.http.response import HttpResponse



# Create your views here.
@login_required(login_url="/accounts/login/")
def VistaListadoFiltros(request):
    if request.method == "GET":
        template = "AppFiltrosCore/ListadoFiltrosHechos.html"
        nombre_pestania = "Filtros"
        #El .all() coge todos los registros.
        #El .get() coge un unico registro filtrando por una serie de campos.
        
        contexto = {
            "clave_nombre_pestania" : nombre_pestania,
            
            }
        return render(request, template , contexto)
    
    
