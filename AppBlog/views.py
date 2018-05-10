from django.shortcuts import render,get_object_or_404
from .models import Post, Category
from django.views.generic.list import ListView

"""
#---------------- FUNCIONES ----------------#

# Create your views here.
def VistaBlog(request):
    #El .all() coge todos los registros.
    #El .get() coge un unico registro filtrando por una serie de campos.
    posts = Post.objects.all()
    return render(request, "AppBlog/Blog.html", {'posts':posts})

def VistaCategoria(request,category_id):
    #category_id: Es la clave primaria
    #El .get() coge un unico registro filtrado por una serie de campos.
    category = get_object_or_404(Category,id=category_id)
    return render(request,"AppBlog/Categoria.html", {'category':category})
"""

#---------------- CLASES ----------------#
# Create your views here.
#ListView me muestra una lista de objetos, en este caso, los objetos seran los modelos.
class VistaBlog(ListView):
    model = Post
    template_name = "AppBlog/Blog.html"
    
    def get(self,request,*args,**kwargs):
        valor_post = Post.objects.all()
        contexto = {
            'clave_cabecera_template' : "BLOG",
            'clave_posts_template':valor_post,
                }
        return render(request,self.template_name,contexto)
    
def VistaCategoria(request,category_id):
    #category_id: Es la clave primaria
    #El .get() coge un unico registro filtrado por una serie de campos.
    category = get_object_or_404(Category,id=category_id)
    return render(request,"AppBlog/Categoria.html", {'category':category})