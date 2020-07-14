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
    path('libro_capitulo/<isbn>/', leer_libro_por_capitulo, name='libro_capitulo'),
    path('agregar_a_leyendo/<isbn>', agregar_a_leyendo, name="agregar_a_leyendo"),
    path('quitar_de_leyendo/<isbn>', quitar_de_leyendo, name="quitar_de_leyendo"),
    path('agregar_a_leyendo_libro_cap/<isbn>', agregar_a_leyendo_libro_cap, name="agregar_a_leyendo_libro_cap"),
    path('quitar_de_leyendo_libro_cap/<isbn>', quitar_de_leyendo_libro_cap, name="quitar_de_leyendo_libro_cap"),
    path('agregar_libro_favoritos/<isbn>', agregar_libro_favoritos, name='agregar_libro_favoritos'),
    path('agregar_libro_cap_favoritos/<isbn>', agregar_libro_cap_favoritos, name='agregar_libro_cap_favoritos'),
    path('agregar_cap_favoritos/<isbn>/<titulo>', agregar_cap_favoritos, name='agregar_cap_favoritos'),
    path('quitar_libro/<isbn>', quitar_libro, name='quitar_libro'),
    path('quitar_libro_cap/<isbn>', quitar_libro_cap, name='quitar_libro_cap'),
    path('quitar_cap_favoritos/<isbn>/<titulo>', quitar_cap_favoritos, name='quitar_cap_favoritos'),
    path('terminar_libro/<isbn>', terminar_libro, name="terminar_libro"),
    path('terminar_libro_cap/<isbn>', terminar_libro_cap, name="terminar_libro_cap"),
    path('quitar_terminado/<isbn>', quitar_terminado, name="quitar_terminado"),
    path('agregar_futuras_lecturas/<isbn>', agregar_futuras_lecturas, name='agregar_futuras_lecturas'),
    path('quitar_futuras_lecturas/<isbn>', quitar_futuras_lecturas, name='quitar_futuras_lecturas'),
    path('agregar_futuras_lecturas_libro_cap/<isbn>', agregar_futuras_lecturas_libro_cap, name='agregar_futuras_lecturas_libro_cap'),
    path('quitar_futuras_lecturas_libro_cap/<isbn>', quitar_futuras_lecturas_libro_cap, name='quitar_futuras_lecturas_libro_cap'),
    path('vermiscomentarios/', vermiscomentarios, name="vermiscomentarios"),
    path('borrarcomentario/<id>/<isbn>/<aux>', borrarcomentario, name="borrarcomentario"),
    path('puntuar/<isbn>/<tipo>/<puntos>', puntuar, name="puntuar"),
    path('misvotos/', misvotos, name="misvotos"),
    path('vercomentario/<id>/<deDonde>', verComentario, name="vercomentario"),
    path('comentar/<isbn>/', escribirComentario, name="escribirComentario"),
    path("historial/", historial, name="historial"),
    path('favoritos/', listar_favoritos, name='listar_favoritos'),
    path("trailers/", trailers, name="trailers"),
    path("mas_leidos/", mas_leidos, name="mas_leidos"),
    path('borrar_perfil/<perfil>', borrar_perfil, name="borrar_perfil"),
    path('borrar_perfil_definitivo/<perfil>', borrar_perfil_definitivo, name="borrar_perfil_definitivo"),
    path('borrar_cuenta/', borrar_cuenta, name="borrar_cuenta"),
    path('borrar_cuenta_definitivo/', borrar_cuenta_definitivo, name="borrar_cuenta_definitivo"),
    path('solicitudes/', solicitudes, name='solicitudes'),
    path('solicitar_cambio/', solicitar_cambio, name='solicitar_cambio'),
    path("simuladorTemporal/", simuladorTemporal, name="simuladorTemporal"),
    path("aceptarSolicitud/<idSol>/<num>/", aceptarSolicitud, name="aceptarSolicitud"),
    path("buscar/",buscar, name="buscar"),
    path("buscarSuscriptores/", entreFechas, name="entreFechas")

]   + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

