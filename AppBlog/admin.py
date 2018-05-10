from django.contrib import admin
from .models import ModeloBlog
#Configuracion extendida, para que en el panel del admin se vean los siguientes atributos del modelo



class ModeloBlogAdmin(admin.ModelAdmin):
    readonly_fields = ('created','updated',)
    #Le indicamos que columnas mostrar
    list_display = ('title','content',)
    #Le indicamos por lo que queremos ordenar
    ordering = ('title','content',)


#Registro el modelo y le paso la configuracion extendida
admin.site.register(ModeloBlog,ModeloBlogAdmin)