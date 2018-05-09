from django import forms


class ContactForm(forms.Form):
    #required=True: Le decimos que es obligatorio
    name = forms.CharField(label="Nombre",required=True)
    email = forms.EmailField(label="Email",required=True)
    content = forms.CharField(label="Mensaje",required=True,widget=forms.Textarea)
    