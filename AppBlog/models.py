from django.db import models
from django.utils.timezone import now
from django.contrib.auth.models import User #modelo que contiene todos los usuarios del panel de administrador
from ckeditor.fields import RichTextField #Aplicacion para visualizarlo mejor en el panel de administrador

# Create your models here.
#Modelo para las categorias: Category
class Category(models.Model):
    name = models.CharField(max_length=100, verbose_name = "Nombre")
    #auto_now_add: se aniadira al crear la instancia la primera vez
    created = models.DateTimeField(auto_now_add=True, verbose_name = "Fecha de creación")
    #auto_now: se actualizara cuando lo modifiquemos
    updated = models.DateTimeField(auto_now=True, verbose_name = "Fecha de creación")
    
    class Meta:
        verbose_name = "Categoría"
        verbose_name_plural ="Categorías"
        ordering = ['-created']   
    #es lo que devuelve, por ejemplo aqui devuelve el nombre en el panel de administrador
    def __str__(self):
        return self.name    
        
#Modelo para las entradas: Post
class Post(models.Model):
    title = models.CharField(max_length=200, verbose_name = "Título")
    content = RichTextField(verbose_name = "Contenido")
    published = models.DateTimeField(verbose_name = "Fecha de publicación",default=now)
    #blank=True: Le decimos que puede ser un campo que este en blanco
    #null=True: Le decimos que puede ser un campo nullo sin nada
    image = models.ImageField(verbose_name="Imagen",upload_to="Blog",null=True,blank=True)
    #on_delete: Le dice a Django lo que tiene que hacer con esta entrada cuando se borre el Autor
    #models.CASCADE: Borra en cascada todas las entradas de este autor
    author = models.ForeignKey(User, verbose_name = "Autor",on_delete=models.CASCADE)
    #Elige una categoría o varias del modelo Category
    categories = models.ManyToManyField(Category,verbose_name="Categorías", related_name="get_posts")
    #auto_now_add: se aniadira al crear la instancia la primera vez
    created = models.DateTimeField(auto_now_add=True, verbose_name = "Fecha de creación")
    #auto_now: se actualizara cuando lo modifiquemos
    updated = models.DateTimeField(auto_now=True, verbose_name = "Fecha de creación")
    
    class Meta:
        verbose_name = "Entrada"
        verbose_name_plural ="Entradas"
        ordering = ['-created']
        
    def __str__(self):
        return self.title    
        