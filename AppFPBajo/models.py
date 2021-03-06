from django.db import models
from django.contrib.auth.models import User #modelo que contiene todos los usuarios del panel de administrador
from ckeditor.fields import RichTextField #Aplicacion para visualizarlo mejor en el panel de administrador
# Create your models here.
class ModeloFPBajo(models.Model):
    nameFilter = models.CharField(max_length=200, verbose_name = "Nombre Filtro")
    #blank=True: Le decimos que puede ser un campo que este en blanco
    #null=True: Le decimos que puede ser un campo nullo sin nada
    estado = models.CharField(max_length=100, null=True, blank=True)
    celery_id = models.CharField(max_length=200, null=True, blank=True)
    imagePlantilla = models.ImageField(verbose_name="Imagen Plantilla",upload_to="FPBajo",null=True,blank=True)
    imagePrototipoFiltro = models.ImageField(verbose_name="Imagen Prototipo Filtro",upload_to="FPBajo",null=True,blank=True)
    imageDesnormalizadaFreImp = models.ImageField(verbose_name="Imagen Desnormalizada en Frecuencia e Impedancia",upload_to="FPBajo",null=True,blank=True)
    tipoFiltro = models.CharField(max_length=100, null=True, blank=True)
    Ap_db = models.FloatField(verbose_name="Atenuacion en la banda de paso [dB]", default=None)
    As_db = models.FloatField(verbose_name="Atenuacion en la banda eliminada (stop) [dB]", default=None)
    Fp_Hz = models.FloatField(verbose_name="Frecuencia de paso [Hz]", default=None)
    Fs_Hz = models.FloatField(verbose_name="Frecuencia de stop [Hz]", default=None)
    Rg_Ohm = models.FloatField(verbose_name="Resistencia generador [Ohm]", default=None)
    Rl_Ohm = models.FloatField(verbose_name="Resistencia de carga (load) [Ohm]", default=None)
    #on_delete: Le dice a Django lo que tiene que hacer con esta entrada cuando se borre el Autor
    #models.CASCADE: Borra en cascada todas las entradas de este autor
    author = models.ForeignKey(User, verbose_name="Autor",on_delete=models.CASCADE)
    #auto_now_add: se aniadira al crear la instancia la primera vez
    created = models.DateTimeField(auto_now=False,auto_now_add=True,verbose_name = "Fecha de creacion")
    #auto_now: se actualizara cuando lo modifiquemos
    updated = models.DateTimeField(auto_now=True,auto_now_add=False, verbose_name = "Fecha de finalizacion")
    
    class Meta:
        verbose_name = "FPBajo"
        verbose_name_plural ="FPBajos"
        ordering = ['-created']

class Filtro_Butterworth(models.Model):
    ordenFiltro  = models.IntegerField(verbose_name = "Orden del Filtro")
    Rg = models.FloatField()
    Rl = models.FloatField()
    g_1 = models.FloatField()
    g_2 = models.FloatField()
    g_3 = models.FloatField()
    g_4 = models.FloatField()
    g_5 = models.FloatField()
    g_6 = models.FloatField()
    g_7 = models.FloatField()
    g_8 = models.FloatField()
    g_9 = models.FloatField()
    g_10 = models.FloatField()


    def __int__(self):
        return self.ordenFiltro    
    
    
class Filtro_Chebyshev(models.Model):
    ordenFiltro  = models.IntegerField(verbose_name = "Orden del Filtro")
    Rg = models.FloatField()
    Rl = models.FloatField() 
    g_1 = models.FloatField()
    g_2 = models.FloatField()
    g_3 = models.FloatField()
    g_4 = models.FloatField()
    g_5 = models.FloatField()
    g_6 = models.FloatField()
    g_7 = models.FloatField()
    g_8 = models.FloatField()
    g_9 = models.FloatField()
    g_10 = models.FloatField()


    def __int__(self):
        return self.ordenFiltro   
        