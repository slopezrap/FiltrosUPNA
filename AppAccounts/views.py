from django.shortcuts import render,redirect
from django.urls import reverse
from .forms import FormularioUserLogin,FormularioUserRegister
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
# Create your views here.
def VistaSignUp(request):
    try:
        if request.method == "GET":
            template = "AppAccounts/SignUp.html"
            nombre_pestania = "Registro"
            formulario = FormularioUserRegister()
            contexto = {
                "clave_nombre_pestania" : nombre_pestania,
                'clave_formulario_template': formulario,
            }         
            return render(request, template , contexto)  
        
        if request.method == "POST":
            formulario = FormularioUserRegister(data=request.POST)
            if formulario.is_valid(): 
                #Uso formulario.cleaned_data.get en lugar de request.POST.get porque el primero chequea la condicion del formulario
                username = formulario.cleaned_data.get("username")
                first_name = formulario.cleaned_data.get("first_name")
                last_name = formulario.cleaned_data.get("last_name")
                email = formulario.cleaned_data.get("email")
                password1 = formulario.cleaned_data.get("password1")
                user = User.objects.create_user(username=username,first_name=first_name,last_name=last_name,email=email,password=password1)
                login(request,user)
                return redirect(reverse('name-home')) 
            else:
                template = "AppAccounts/SignUp.html"
                nombre_pestania = "SignUp"
                contexto = {
                    "clave_nombre_pestania" : nombre_pestania,
                    'clave_formulario_template': formulario,
                }         
                return render(request, template , contexto)  
        
    except User.DoesNotExist:
        return redirect(reverse('name-404'))     
    
    
def VistaLogin(request):
    if request.method == "GET":
        template = "AppAccounts/Login.html"
        nombre_pestania = "Login"
        formulario = FormularioUserLogin()
        contexto = {
            "clave_nombre_pestania" : nombre_pestania,
            'clave_formulario_template': formulario,
        }         
        return render(request, template , contexto)  
    
    if request.method == "POST":
        formulario = FormularioUserLogin(data=request.POST)
        print(formulario.is_valid())
        if formulario.is_valid(): 
            #Uso formulario.cleaned_data.get en lugar de request.POST.get porque el primero chequea la condicion del formulario
            username = formulario.cleaned_data.get("username")
            password1 = formulario.cleaned_data.get("password1")
            print(password1)
            user = authenticate(username=username, password1=password1)
            print(user)
            login(request,user)
            #print(request.user.is_authenticated)
            return redirect(reverse('name-home')) 
        else:
            template = "AppAccounts/Login.html"
            nombre_pestania = "Login"
            contexto = {
                "clave_nombre_pestania" : nombre_pestania,
                'clave_formulario_template': formulario,
            }         
            return render(request, template , contexto)  

def VistaLogout(request):
    if request.method == "GET":
        logout(request)
        return redirect(reverse('name-home')) 


