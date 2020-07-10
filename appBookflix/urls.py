from django.urls import path, include 
from .views import *
from django.conf.urls.static import static 
from django.conf import settings 
from django.contrib import admin 
from django.conf.urls import url
 
urlpatterns = [
    path('', welcome, name='welcome'),
    #path('/', landing_view, name='/'),
    path('home/', home, name='home'),
    path('register_page/',register_page, name="register"),
    path('login/', login_propio, name='login'),
    path('logout/', logout, name="logout"),
    path('select_perfil/', select_perfil, name='seleccionarPerfil'),
    path('crear_perfil/', crear_perfil, name='crear_perfil'),
    path("perfil/", perfil, name='perfil'),
    path("perfil_seleccionado/<id_perfil>/", perfil_seleccionado, name="perfil_seleccionado"),  
    path("cambiar_contrasenia/", cambiar_contrasenia, name="cambiar_contrasenia"),
    path("cambiar_tarjeta/", cambiar_tarjeta, name="cambiar_tarjeta"),
    path("cambiar_email/", cambiar_email, name="cambiar_email"),
    path('leer_libro/<isbn>/', leer_libro, name='leerlibro'),
]   + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

