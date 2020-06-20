from django.shortcuts import render
from django.shortcuts import redirect 
from django.http import HttpResponse
from .models import *

# Create your views here.

def home_screen_view(request):
    print(request.headers)
    return render(request, "base.html", {})

def welcome(request):
    libros=Libro.objects.all()
    context={} #declaro que context es una lista
    context["Libro"]=libros
    return render(request, "appBookflix/home.html", context)

def login(request):
    libros=Libro.objects.all()
    context={} #declaro que context es una lista
    context["Libro"]=libros
    return render(request, "appBookflix/loginUser.html", context)