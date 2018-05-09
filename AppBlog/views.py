from django.shortcuts import render,get_object_or_404
from .models import Post, Category
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