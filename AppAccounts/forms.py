# encoding: utf-8
# encoding: iso-8859-1
# encoding: win-1252
from django import forms
from django.contrib.auth import get_user_model, authenticate
from django.contrib.auth.forms import UserCreationForm
User = get_user_model()

class FormularioUserLogin(forms.Form):
    username = forms.CharField(max_length=254, help_text='Requerido. Escriba un usuario válido.',label="Usuario")
    password1 = forms.CharField(widget=forms.PasswordInput,help_text='Requerido. Escriba una constraseña válida.',label="Contraseña")
    
    def clean(self, *args, **kwargs):
        username = self.cleaned_data.get("username")
        password1 = self.cleaned_data.get("password1")        
        if username and password1:
            print(username)
            print(password1)
            print(authenticate(username=username, password1=password1))
            user = authenticate(username=username, password1=password1)
            if not user:
                raise forms.ValidationError("Usuario o password incorrecto")
            if not user.is_active:    
                raise forms.ValidationError("El usuario ya no esta activo")   
            
            return super(FormularioUserLogin,self).clean(*args,**kwargs)   
        
        
class FormularioUserRegister(UserCreationForm):
    first_name = forms.CharField(max_length=30, required=False, help_text='Opcional.',label="Nombre")
    last_name = forms.CharField(max_length=30, required=False, help_text='Opcional.',label="Apellido")  
    email = forms.EmailField(max_length=254, help_text='Requerido. Escriba un email válido.')
    email2 = forms.EmailField(max_length=254, help_text='Para verificar, introduzca el mismo email anterior.',label="Email (confirmación)")    
    
    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name', 'email','email2', 'password1', 'password2', )
        
    def clean_email2(self):
        email = self.cleaned_data.get("email")
        email2 = self.cleaned_data.get("email2")
        if email != email2:
            raise forms.ValidationError("Los emails no coinciden")
        email_qs = User.objects.filter(email=email)
        if email_qs.exists():
            raise forms.ValidationError("Este email ya esta registrado")
        return email
        
        