from django.shortcuts import render
from .models import Post 
# Create your views here.
def VistaBlog(request):
    posts = Post.objects.all()
    return render(request, "AppBlog/Blog.html", {'posts':posts})
