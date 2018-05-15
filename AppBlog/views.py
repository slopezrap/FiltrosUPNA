# encoding: utf-8
# encoding: iso-8859-1
# encoding: win-1252

from django.shortcuts import render,redirect
from django.urls import reverse
from .models import ModeloBlog
from .forms import FormularioBlog
from django.contrib.auth.decorators import login_required
from django.http.response import HttpResponse



# Create your views here.

def VistaBlog(request):
    if request.method == "GET":
        template = "AppBlog/Blog.html"
        nombre_pestania = "Blog"
        #El .all() coge todos los registros.
        #El .get() coge un unico registro filtrando por una serie de campos.
        EntradasBlog = ModeloBlog.objects.all()
        contexto = {
            "clave_nombre_pestania" : nombre_pestania,
            'clave_entradasBlog_template':EntradasBlog,
            }
        return render(request, template , contexto)

@login_required(login_url="/accounts/login/")
def VistaCrearEntradaBlog(request):
    if request.method == "GET":
        template = "AppBlog/CrearEntradaBlog.html"
        nombre_pestania = "Crear Entrada Blog"
        formulario = FormularioBlog()
        contexto = {
            "clave_nombre_pestania" : nombre_pestania,
            'clave_formulario_template': formulario,
            }
        return render(request, template , contexto)
    
    if request.method == "POST":
        formulario = FormularioBlog(request.POST)
        if formulario.is_valid():
            autor = request.user
            #Uso formulario.cleaned_data.get en lugar de formulario.cleaned_data.get porque el primero chequea la condicion del formulario
            tituloEntrada = formulario.cleaned_data.get("title")
            contenidoEntrada = formulario.cleaned_data.get("content")
            imagenEntrada = formulario.cleaned_data.get("image")
            #Guardo en la base de datos
            ModeloBlog.objects.create(title=tituloEntrada,content=contenidoEntrada,author=autor,image=imagenEntrada) 
            #La linea de arriba es igual que las 3 lineas de abajo comentadas:
            #objeto = ModeloBlog()
            #obj.title = tituloEntrada
            #obj.save
            return redirect(reverse('name-blog'))

    """
    #Otra forma de hacerlo con menos codigo pero menos intuitivo seria:
    formulario = FormularioBlog(request.POST or None)
    if formulario.is_valid():
        instancia = formulario.save(commit=False)
        intance.save()
    """

@login_required(login_url="/accounts/login/")   
def VistaEditarEntradaBlog(request, pk):  
    try:
        instancia_objeto_bbdd = ModeloBlog.objects.get(pk=pk)
        if (instancia_objeto_bbdd.author) != (request.user):
            reponse = HttpResponse("No tienes permisos para modificar esta entrada")
            reponse.status_code = 403
            return reponse  
        else:         
            if request.method == "GET":
                template = "AppBlog/EditarEntradaBlog.html"
                nombre_pestania = "Editar Entrada Blog"
                EntradaBlog = FormularioBlog(instance=instancia_objeto_bbdd)
                contexto = {
                    "clave_nombre_pestania" : nombre_pestania,
                    'clave_formulario_template': EntradaBlog,
                    }    
                return render(request, template, contexto)        
            
            if request.method == "POST":
                formulario = FormularioBlog(request.POST, instance=instancia_objeto_bbdd)
                if formulario.is_valid():
                    autor = request.user
                    #Uso formulario.cleaned_data.get en lugar de request.POST.get porque el primero chequea la condicion del formulario
                    tituloEntrada = formulario.cleaned_data.get("title")
                    contenidoEntrada = formulario.cleaned_data.get("content")
                    imagenEntrada = formulario.cleaned_data.get("image")
                    #Edito en la base de datos
                    ModeloBlog.objects.filter(pk=pk).update(title=tituloEntrada,content=contenidoEntrada,author=autor,image=imagenEntrada) 
                    return redirect(reverse('name-blog')+"?editado")
            
    except ModeloBlog.DoesNotExist:
        return redirect(reverse('name-404'))

@login_required(login_url="/accounts/login/")
def VistaBorrarEntradaBlog(request,pk): 
    try:
        instancia_objeto_bbdd = ModeloBlog.objects.get(pk=pk)
        if (instancia_objeto_bbdd.author) != (request.user):
            reponse = HttpResponse("No tienes permisos para borrar esta entrada")
            reponse.status_code = 403
            return reponse  
        
        else:
            if request.method == "GET":
                template = "AppBlog/BorrarEntradaBlogConfirmacion.html"
                nombre_pestania = "Borrar Entrada Blog"
                contexto = {
                    "clave_nombre_pestania" : nombre_pestania,
                    }
                
                return render(request, template, contexto)
            if request.method =="POST":
                ModeloBlog.objects.filter(pk=pk).delete()    
                return redirect(reverse('name-blog')+"?borrada")     
                    
    except ModeloBlog.DoesNotExist:
        return redirect(reverse('name-404'))  
       
            
def VistaDetalleEntradasBlog(request,pk):
    try:
        if request.method == "GET":
            template = "AppBlog/DetalleEntrada.html"
            nombre_pestania = "Detalle"
            #El .get() coge un unico registro filtrando por una serie de campos.
            EntradaBlog = ModeloBlog.objects.all().filter(author__id=pk)
            contexto = {
                "clave_nombre_pestania" : nombre_pestania,
                'clave_entradasBlog_template':EntradaBlog,
                }
            return render(request, template , contexto)
        
    except ModeloBlog.DoesNotExist:
        return redirect(reverse('name-404'))



