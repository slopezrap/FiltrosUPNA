from django.shortcuts import render, redirect
from django.urls import reverse
from .forms import ContactForm
from django.core.mail import EmailMessage 

# Create your views here.
def VistaContacto(request):
    valor_formulario_contacto = ContactForm()
    if request.method == "POST":
        valor_formulario_contacto = ContactForm(data=request.POST)
        if valor_formulario_contacto.is_valid():
            #Si el formulario es valido recupero los valores del formulario
            #Uso valor_formulario_contacto.cleaned_data.get en lugar de request.POST.get porque el primero chequea la condicion del formulario
            name = valor_formulario_contacto.cleaned_data.get('name')
            email = valor_formulario_contacto.cleaned_data.get('email')
            content = valor_formulario_contacto.cleaned_data.get('content')
            
            #Si todo va bien, enviamos el correo y redireccionamos a la propia pagina contact/ok a traves de un request.GET
            #Uso reverse porque en lugar de meter la pagina en crudo es como un {% url 'name' %}
            
            email = EmailMessage(
                "Asunto de Web-Filtros: Nuevo mensaje de contacto",
                "Cuerpo de {} <{}>\n\nEscribio:\n\n{}".format(name,email,content),
                "no-contestar@inbox.mailtrap.io",
                ["s.lopezrap@gmail.com"],
                reply_to=[email]
                )
            try:
                email.send()
                #Luego le sumo una cadena ok a la url contact/?ok para decirle en el Contact.html que si le llega un ok escriba el mensaje
                return redirect(reverse('name-contact')+"?ok")
            except:
                #Luego le sumo una cadena fail a la url contact/?fail para decirle en el Contact.html que no se envio el mensaje
                return redirect(reverse('name-contact')+"?fail")   
    contexto = {
        'clave_en_template':valor_formulario_contacto,
        }
    return render(request,"AppContacto/Contact.html",contexto)