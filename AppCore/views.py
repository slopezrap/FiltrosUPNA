from django.shortcuts import render

# Create your views here.
def VistaAbout(request):
    return render(request,"AppCore/About.html")

def VistaContacto(request):
    return render(request,"AppCore/Contact.html")

def VistaHome(request):
    return render(request,"AppCore/Home.html")


def VistaPortfolio(request):
    return render(request,"AppCore/Portfolio.html")



