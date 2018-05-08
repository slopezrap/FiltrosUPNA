from django.contrib import admin
from .models import Category,Post
#Configuracion extendida, para que en el panel del admin se vean los siguientes atributos del modelo

class CategoryAdmin(admin.ModelAdmin):
    readonly_fields = ('created','updated',)


class PostAdmin(admin.ModelAdmin):
    readonly_fields = ('created','updated',)
    #Le indicamos que columnas mostrar
    list_display = ('title','author','published','post_categories')
    #Le indicamos por lo que queremos ordenar
    ordering = ('author','published',)
    #filtro, como es un author que se un ForeignKey hay que poner dos barras bajas y username que es como esta en models author
    list_filter = ('author__username','categories__name')
    
    #Este metodo es para listar las categorias, hay que hacerlo as�, ya que es un campo manytomany
    def post_categories(self,obj):
        #Lo que hago es recorrer una lista sacando el nombre para cada categoria y genera una cadena de caracteres separadas por coma ","
        return ", ".join([c.name for c in obj.categories.all().order_by("name")])
    #Esto me cambia el post_categories que debera ir en list_display por Categoria
    post_categories.short_description = "Categorías"
    

#Registro el modelo y le paso la configuracion extendida
admin.site.register(Category,CategoryAdmin)
admin.site.register(Post,PostAdmin)