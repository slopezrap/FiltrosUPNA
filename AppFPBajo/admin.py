from django.contrib import admin
from .models import ModeloFPBajo
#Configuracion extendida, para que en el panel del admin se vean los siguientes atributos del modelo



class ModeloFPBajoAdmin(admin.ModelAdmin):
    readonly_fields = ('created','updated',)
    #Le indicamos que columnas mostrar
    list_display = ('nameFilter','Ap_db','As_db','Fp_Hz','Fs_Hz','Rg_Ohm','Rl_Ohm')
    #Le indicamos por lo que queremos ordenar
    ordering = ('created','nameFilter',)


#Registro el modelo y le paso la configuracion extendida
admin.site.register(ModeloFPBajo,ModeloFPBajoAdmin)