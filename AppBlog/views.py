from django.shortcuts import render,redirect
from django.urls import reverse
from .models import ModeloBlog
from .forms import FormularioBlog


#---------------- FUNCIONES ----------------#
# Create your views here.

def VistaBlog(request):
    template = "AppBlog/Blog.html"
    nombre_pestania = "Blog"
    if request.method == "GET":
        #El .all() coge todos los registros.
        #El .get() coge un unico registro filtrando por una serie de campos.
        EntradasBlog = ModeloBlog.objects.all()
        contexto = {
            "clave_nombre_pestania" : nombre_pestania,
            'clave_entradasBlog_template':EntradasBlog,
            }
        return render(request, template , contexto)


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
        formulario = FormularioBlog(request.POST or None)
        if formulario.is_valid():
            autor = request.user
            tituloEntrada = request.POST.get("title",'')
            contenidoEntrada = request.POST.get("content",'')
            imagenEntrada = request.POST.get("image",'')
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
    
def VistaEditarEntradaBlog(request, pk):  
    try:
        instancia_objeto_bbdd = ModeloBlog.objects.get(pk=pk)
        if request.method == "POST":
            form = FormularioBlog(request.POST, instance=instancia_objeto_bbdd)
            if form.is_valid():
                autor = request.user
                tituloEntrada = request.POST.get("title",'')
                contenidoEntrada = request.POST.get("content",'')
                imagenEntrada = request.POST.get("image",'')
                #Edito en la base de datos
                ModeloBlog.objects.filter(pk=pk).update(title=tituloEntrada,content=contenidoEntrada,author=autor,image=imagenEntrada) 
                return redirect(reverse('name-blog')+"?editado")
            
        if request.method == "GET":
            template = "AppBlog/EditarEntradaBlog.html"
            nombre_pestania = "Editar Entrada Blog"
            EntradaBlog = FormularioBlog(instance=instancia_objeto_bbdd)
            contexto = {
                "clave_nombre_pestania" : nombre_pestania,
                'clave_formulario_template': EntradaBlog,
                }
            
            return render(request, template, contexto)
    
    except ModeloBlog.DoesNotExist:
        return redirect(reverse('name-404'))


def VistaBorrarEntradaBlog(request,pk):
    try: 
        if request.method == "GET":
            ModeloBlog.objects.filter(pk=pk).delete()
            return redirect(reverse('name-blog')+"?borrada")
    
    except ModeloBlog.DoesNotExist:
        return redirect(reverse('name-404'))
         
            
def VistaDetalleEntradasBlog(request):
    return None



