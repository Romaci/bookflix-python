from django.urls import path, include 
from .views import *
from django.conf.urls.static import static 
from django.conf import settings 
from django.contrib import admin 
from django.conf.urls import url
 
urlpatterns = [
    path('', landing_view, name='welcome'),
    #path('home/', home, name='home'),
    path('register_page/',register_page, name="register"),
    path('login/', login_propio, name='login'),
    path('logout/', logout, name="logout"),
    path('select_perfil/', select_perfil, name='seleccionarPerfil'),
    path('crear_perfil/', crear_perfil, name='crear_perfil'),
]   + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

