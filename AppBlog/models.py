from django.db import models
from django.contrib.auth.models import User #modelo que contiene todos los usuarios del panel de administrador
from ckeditor.fields import RichTextField #Aplicacion para visualizarlo mejor en el panel de administrador
# Create your models here.
class ModeloBlog(models.Model):
    title = models.CharField(max_length=200, verbose_name = "Titulo")
    content = RichTextField(verbose_name = "Contenido")
    #blank=True: Le decimos que puede ser un campo que este en blanco
    #null=True: Le decimos que puede ser un campo nullo sin nada
    image = models.ImageField(verbose_name="Imagen",upload_to='Blog',null=True,blank=True)
    #on_delete: Le dice a Django lo que tiene que hacer con esta entrada cuando se borre el Autor
    #models.CASCADE: Borra en cascada todas las entradas de este autor
    author = models.ForeignKey(User, verbose_name = "Autor",on_delete=models.CASCADE)
    #auto_now_add: se aniadira al crear la instancia la primera vez
    created = models.DateTimeField(auto_now=False,auto_now_add=True,verbose_name = "Fecha de creacion")
    #auto_now: se actualizara cuando lo modifiquemos
    updated = models.DateTimeField(auto_now=True,auto_now_add=False, verbose_name = "Fecha de creacion")

    class Meta:
        verbose_name = "Entrada"
        verbose_name_plural ="Entradas"
        ordering = ['-created']
        
    def __str__(self):
        return self.title    
        