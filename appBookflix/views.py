from django.shortcuts import render
from django.contrib.auth import authenticate
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import login as do_login
from django.contrib.auth import logout as do_logout
from django.shortcuts import redirect
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_protect
from .forms import *
from .models import *
from django.contrib.auth.forms import UserCreationForm
from django import shortcuts
from appBookflix.models import *
from django.contrib import messages
from django.contrib.auth import update_session_auth_hash
from django.contrib.auth.forms import PasswordChangeForm

from django.conf import settings

from django.utils.crypto import get_random_string

from django.core import serializers

from random import randint, uniform
from .funcionesAutomatizacion import *
import datetime


def landing_view (request):
    context = {}
    libros = Libro.objects.all()
    context['libros']=libros
    return render(request, "appBookflix/landingPage.html", context)


def welcome(request):
    context={}
    publicacion=Novedad.objects.filter(mostrar_en_home=True) #NOVEDADES
    libros = Libro.objects.filter(mostrar_en_home=True)
    trailers = Trailer.objects.filter(mostrar_en_home=True)
    #context['recomendacion']= recomendados(perfil)
    #context['recomendacionCapitulo']= recomendadosCapitulo(perfil)
    context['publicaciones']=publicacion
    context['trailers']= trailers
    context['libros']=libros
    return render(request, "appBookflix/welcome.html",context)


def home(request):
    try:
        perfil= Profile.objects.get(id= request.session["perfil_ayuda"])
    except:
        perfil=False
    context={}
    noticia=Novedad.objects.filter(mostrar_en_home=True) #NOVEDADES
    libros = Libro.objects.filter(mostrar_en_home=True)
    libros_cap = BookByChapter.objects.filter(mostrar_en_home=True)
    trailers = Trailer.objects.filter(mostrar_en_home=True)
    historial_libros = StateOfBookByChapter.objects.filter(state="reading", profile=perfil) #, profile=request.session.nombrePerfil
    historial_libros_cap = StateOfBook.objects.filter(state="reading", profile=perfil)
    
    auxLibro=recomendados(perfil)
    auxLibroCap= recomendadosCap(perfil)

    
    while len(auxLibro) > 3:
        aux3= random.choice(tuple(auxLibro))
        auxLibro.remove(aux3)

    while len(auxLibroCap) > 3:
        aux3= random.choice(tuple(auxLibro))
        auxLibroCap.remove(aux3)

    context['recomendacion']= auxLibro
    context['recomendacionCapitulo']= auxLibroCap
    context['noticias']=noticia
    context['trailers']= trailers
    context['libros']=libros
    context['historial_libros']=historial_libros
    context['historial_libros_cap']=historial_libros_cap
    context['libros_cap']=libros_cap
    return render(request, "appBookflix/home.html",context) 


def register_page(request):
    context = {}
    if request.POST:
        form = RegistrationForm(request.POST)
        formCard = RegistroTarjeta(request.POST)
        # Si el formulario es válido...
        if form.is_valid() and formCard.is_valid():  

            # Creamos la nueva cuenta de usuario
            cuenta= form.save()
            id_account= form.cleaned_data.get('id')
            email= form.cleaned_data.get('email')
            raw_password= form.cleaned_data.get('password1')
            #account = authenticate(email=email, password=raw_password)
            cuenta.plan= 'normal'
            cuenta.diaspagados=30
            cuenta.save()
            
            numT= formCard.cleaned_data.get("number")
            codT= formCard.cleaned_data.get("cod")
            dateT= formCard.cleaned_data.get("date_expiration")
            cardName= formCard.cleaned_data.get("card_name")
            bankT=formCard.cleaned_data.get("bank")

            tarjeta= CreditCards(number=numT, cod=codT, date_expiration=dateT, card_name=cardName, bank=bankT, user=cuenta)
            tarjeta.save()
            
            return redirect('logout')
        else:
            context["user_creation_form"]=form
            context["creacion_tarjeta"]= formCard
            #context["profile_creation_form"]=formPerfil
    else:
        form=RegistrationForm()
        formCard=RegistroTarjeta()
        formPerfil= CrearPerfil()
        context["user_creation_form"]=form
        context["creacion_tarjeta"]=formCard
        context["profile_creation_form"]=formPerfil
    return render(request, 'appBookflix/register_page.html', context)




def perfil(request):
    #Para saber los datos del usuario hay que usar request.user."atributo"
    tarjetaActual = CreditCards.objects.get(user =request.user)
    numTarjeta = tarjetaActual.number[-3] + tarjetaActual.number[-2] + tarjetaActual.number[-1]
    return render(request, "appBookflix/perfil.html",{'tarjetaActual': tarjetaActual, 'numeroPa': numTarjeta})



def select_perfil(request):
    perfiles = Profile.objects.filter(account = request.user)
    return render(request, "appBookflix/select_perfil.html", {'perfiles': perfiles,}) #"tarjetaActual": tarjetaActual, "perfilActual":perfilActual})

def datos_personales(request):
    context = {} 
    perfiles = Profile.objects.filter(account = request.user)
    t= CreditCards.objects.get(user= request.user)
    context["tarjeta"]=t
    context["perfiles"]=perfiles
    return render(request, "appBookflix/datos_personales.html", context)



def solicitudes(request):
    solicitudes = UserSolicitud.objects.filter(type_of_solicitud='alta', is_accepted=0)
    usuarios= UserSolicitud.objects.filter(type_of_solicitud='alta', is_accepted=0).values('user')
    tarjetas= CreditCards.objects.filter(user__in= usuarios)
    return render(request,"appBookflix/solicitudes.html",{"solicitudes":solicitudes, "tarjetas":tarjetas})

def login_propio(request):
    # Creamos el formulario de autenticación vacío
    form = AuthenticationForm()
    if request.method == "POST":
        # Añadimos los datos recibidos al formulario
        form = AuthenticationForm(data=request.POST)
        # Si el formulario es válido...
        if form.is_valid():
            # Recuperamos las credenciales validadas
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']

            # Verificamos las credenciales del usuario
            user = authenticate(username=username, password=password,)

            # Si existe un usuario con ese nombre y contraseña
            if user is not None:
                # Hacemos el login manualmente  Y le redireccionamos a la portada
                ##if user.confirmo:
                do_login(request, user)
                return redirect('/select_perfil')
              ##  #request.session['emailConfirm']= user.email
              ##  #request.session.modified = True
               ## #return redirect('/confirmarCuenta')
               #             
    # Si llegamos al final renderizamos el formulario
  #  publicaciones=len(Novedad.objects.all())
  #  publicacion=Novedad.objects.filter(id=randint(1,publicaciones+1))
  #  while not publicacion:
  #      publicacion=Novedad.objects.filter(id=randint(1,publicaciones+1))

  #  trailers=len(Trailer.objects.all())
  #  trailer=Trailer.objects.filter(id=randint(1,(trailers+1)))
  #  while not trailer:
 #       trailer=Trailer.objects.filter(id=randint(1,(trailers+1)))

    libros = Libro.objects.filter(mostrar_en_home=True)

    #return render(request, "appBookflix/login.html", {'form': form, 'publicaciones':publicacion, "libros":libros,"trailers":trailer})
    return render(request, "appBookflix/login.html", {'form': form, "libros":libros})


def logout(request):
    # Finalizamos la sesión
    do_logout(request)
    # Redireccionamos al login
    return redirect('/')




def crear_perfil(request):
    context={}
    request.session['ErrorDePerfil'] = "1"
    request.session.modified = True
    if request.POST:
        form= CrearPerfil(request.POST)
        if form.is_valid():
            try:
                p= Profile.objects.get(name= form.cleaned_data['name'], account=request.user)
                request.session['ErrorDePerfil'] = "2"
                request.session.modified = True
            except Profile.DoesNotExist:
                perfil= form.save(commit=False)
                perfil.account = request.user
                perfil.save()
                return redirect ('/select_perfil')
    
    form=CrearPerfil()
    context["profile_creation_form"]=form
    return render(request, 'appBookflix/crear_perfil.html', context)


def perfil_seleccionado(request,id_perfil):
    perfil_actual = Profile.objects.get(id=id_perfil)
    perfil_actual.is_active_now = True 
    perfil_actual.save()
    request.session["perfil_ayuda"] = id_perfil

    request.session['nombrePerfil']= perfil_actual.name
    perfil_actual = serializers.serialize("json", Profile.objects.all())
    request.session['perfil_actual']= perfil_actual
    #request.session['perfil_actual']= perfil_actual.name

    request.session.modified = True
    return redirect("/home") 
 

def cambiar_contrasenia(request):

    if request.method == 'POST':
        form = PasswordChangeForm(request.user, request.POST)
        if form.is_valid():
            user = form.save()
            update_session_auth_hash(request, user)  # Important!
            messages.success(request, 'Su Contraseña fue cambiada con éxito')
            #send_mail('Cambio contraseña exitoso Bookflix', "su nueva contrasena es: ... recordala!! no te lo vamos a decir", settings.EMAIL_HOST_USER,[request.user.email])            
            return redirect('/perfil')
        else:
            messages.error(request, 'Corrija el error')
    else:
        form = PasswordChangeForm(request.user)
    return render(request, "appBookflix/cambiar_contraseña.html", {
        'form': form
    })

def cambiar_tarjeta(request):
    
    if request.method == 'POST':
        form = RegistroTarjeta(request.POST)
        if form.is_valid():
            numT= form.cleaned_data.get("number")
            codT= form.cleaned_data.get("cod")
            dateT= form.cleaned_data.get("date_expiration")
            cardName= form.cleaned_data.get("card_name")
            bankT=form.cleaned_data.get("bank")
            t= CreditCards.objects.get(user= request.user).delete()
            tarjeta= CreditCards(number=numT, cod=codT, date_expiration=dateT, card_name=cardName, bank=bankT, user=request.user)
            tarjeta_vieja = CreditCards.objects.get(user=request.user)
            tarjeta_vieja.delete()
            tarjeta.save()

            tarjeta_usada= CreditCardsUsed(number=numT, cod=codT, date_expiration=dateT, card_name=cardName, bank=bankT)
            try:
                tarjeta_usada_vieja = CreditCardsUsed.objects.get(number=tarjeta.number)
                tarjeta_usada_vieja.delete()
            except CreditCardsUsed.DoesNotExist:
                pass
            tarjeta_usada.save()

            return redirect('/perfil')      
        else:
            messages.error(request, 'error tarjeta')
    else:
        form=RegistroTarjeta()
    return render(request, "appBookflix/cambiar_tarjeta.html", {'form': form})


def cambiar_email(request):
    context={}
    mm= request.user.email
    if request.POST:
        form= MailChange(request.POST, instance= request.user)
        if form.is_valid():
            #mensaje= "El nuevo email de la cuenta es " + form.cleaned_data['email'] + ". En caso de no ser usted, responder a este mail dentro de las 48hs recibido con el asunto 'yo no hice el cambio' "
            #send_mail('Cambio de Mail Bookflix', mensaje, settings.EMAIL_HOST_USER,[mm])
            form.save()
            #send_mail('Nuevo Mail Bookflix', "mensaje de confirmacion del cambio de mail", settings.EMAIL_HOST_USER,[request.user.email])            
            return redirect('/perfil')
        else:
            messages.error(request, 'El email elegido ya se encuentra en uso')
    else:
        form= MailChange(
            initial={
                "email": request.user.email,
            }
        )
    context["cambio_mail"]= form 
    return render(request, "appBookflix/cambiar_email.html", context)



def cambiar_nombre(request,nombre):
    context={}
    request.session['ErrorDePerfil'] = "1"
    request.session.modified = True
    perfil_anterior = Profile.objects.get(name= nombre, account=request.user)
    if request.POST:
        form= CrearPerfil(request.POST, instance= perfil_anterior)
        if form.is_valid():
            try:
                p= Profile.objects.get(name= form.cleaned_data['name'], account=request.user)
                request.session['ErrorDePerfil'] = "2"
                request.session.modified = True
            except Profile.DoesNotExist:
                perfil_anterior= form.save(commit=False)
                perfil_anterior.account = request.user
                perfil_anterior.save()
                return redirect ('/select_perfil')
    
    form=CrearPerfil()
    context["profile_creation_form"]=form
    return render(request, 'appBookflix/cambiar_nombre.html', context)

#CATALOGO

def catalogo(request):
    context={}
    libros=Libro.objects.filter(mostrar_en_home=True)
    try: 
         context['libros']=libros
    except Libro.DoesNotExist: None
    return render(request, 'appBookflix/catalogo.html', context)

#NOTICIAS

def noticias(request):
    noticia=Novedad.objects.filter(mostrar_en_home=True)
    return render(request, "appBookflix/noticias.html",{'noticias':noticia })

#COMENTARIOS


def verComentario(request, id, deDonde):
    aux= 0
    context={}
    try:
        comentario= CommentBook.objects.get(id=id)
        ayuda= comentario.publication
        aux=1
    except: pass
    try:
        comentario= CommentBookByChapter.objects.get(id=id)
        ayuda= comentario.publication
        aux= 2
    except: pass
    if aux==1: libro= Libro.objects.get(isbn= ayuda.isbn)
    else: libro= BookByChapter.objects.get(id= ayuda.id)
    puedeEditar= 'False'
    if str(request.session["perfil_ayuda"]) == str(comentario.profile.id):
        puedeEditar= 'True'
    if request.POST:
        form= ComentarioForm(request.POST)
        if form.is_valid():
            spoi= form.cleaned_data['spoiler']
            texto= form.cleaned_data['comentario']
            comentario.description= texto
            comentario.is_a_spoiler= spoi
            comentario.save()
            if deDonde == 'perfil': return redirect("/vermiscomentarios")
            elif aux == 1: return redirect("/leer_libro/"+str(libro.isbn))
            else: return redirect("/libro_capitulo/"+ str(libro.isbn))
    if deDonde == 'perfil': aux= 3
    context['form']= ComentarioForm(initial={'spoiler': comentario.is_a_spoiler, 'comentario': comentario.description})
    context['editar']= puedeEditar
    context['comentario']= comentario
    context['aux']= str(aux)
    context['isbn']= libro.isbn
    return render(request, "appBookflix/vercomentario.html", context)


def borrarcomentario(request,id,isbn,aux):
    aux2=0
    try:
        comentario= CommentBook.objects.get(id=id)
        comentario.delete()
        aux2= 1
    except: pass
    try:
        comentario= CommentBookByChapter.objects.get(id=id)
        comentario.delete()
        aux2= 2
    except: pass
    if aux == '3': return redirect("/vermiscomentarios")
    if aux2==1: return redirect("/leer_libro/"+str(isbn))
    else: return redirect("/libro_capitulo/"+ str(isbn))


def escribirComentario(request, isbn):
    aux= 0
    try:
        libro= Libro.objects.get(isbn=isbn)
        aux= 1
    except: pass
    try:
        libro= BookByChapter.objects.get(isbn=isbn)
        aux= 2 
    except: pass
    context={}
    if request.POST:
        form= ComentarioForm(request.POST)
        if form.is_valid():
            spoi= form.cleaned_data['spoiler']
            texto= form.cleaned_data['comentario']
            perfil= Profile.objects.get( id= request.session["perfil_ayuda"])
            if aux == 1:
                coment= CommentBook( is_a_spoiler=spoi , description=texto, profile=perfil, publication= libro )
                coment.save()
                return redirect("/leer_libro/"+str(isbn))
            else:
                coment= CommentBookByChapter( is_a_spoiler=spoi , description=texto, profile=perfil, publication= libro )
                coment.save()
                return redirect("/libro_capitulo/"+ str(isbn))
    form= ComentarioForm(initial={'spoiler': False})
    context["comentario"] = form 
    context["queEs"]= aux
    context["isbn"]= isbn
    return render(request, "appBookflix/comentar.html", context)


def vermiscomentarios(request):
    context={}
    deLibro= CommentBook.objects.filter(profile= request.session["perfil_ayuda"])
    deLibroPorCap= CommentBookByChapter.objects.filter(profile = request.session["perfil_ayuda"])
    context["deLibro"]= deLibro
    context["deLibroPorCap"]= deLibroPorCap
    return render(request, "appBookflix/vermiscomentarios.html", context)

#FIN COMENTARIOS



def puntuar(request, isbn, tipo, puntos):
    perfil= Profile.objects.get(id= request.session['perfil_ayuda'])
    points= puntos
    if tipo == "completo":
        libro= Libro.objects.get(isbn=isbn)
        try:
            like= Like.objects.get(author=perfil, book=libro)
            like.points= points
            like.save()
        except:
            like=Like(points=points, book=libro, author=perfil)
            like.save()
        return redirect("/leer_libro/"+str(libro.isbn))
    else:
        libro= BookByChapter.objects.get(isbn=isbn)
        try:
            like= LikeBookByChapter.objects.get(author=perfil, book=libro)
            like.points= points
            like.save()
        except:
            like= LikeBookByChapter(points=points, book=libro, author=perfil)
            like.save()
        return redirect("/libro_capitulo/"+ str(libro.isbn))
 
def misvotos(request):
    context={}
    perfil= Profile.objects.get(id= request.session['perfil_ayuda'])
    deLibro= Like.objects.filter(author= perfil)
    deLibroPorCap= LikeBookByChapter.objects.filter(author=perfil)
    context['deLibro']=deLibro
    context['deLibroPorCap']=deLibroPorCap
    return render(request, "appBookflix/misvotos.html", context)

def calcularPuntosDeLibro(likes, cantLikes):
    aux= 0
    for i in likes:
        aux= aux + i.points
    return (aux / cantLikes)

def entreFechas(request): 
    context={}
    #request.session['ErrorDePerfil'] = "1"
    context['suscriptores']=None
    if request.POST:
        form= suscriptosEntreFechasForm(request.POST)
        if form.is_valid():
            try:
                rango2= Account.objects.filter(date_joined__range=(form.cleaned_data['de'],form.cleaned_data['hasta'] ))
                context['suscriptores']=rango2
            except Account.DoesNotExist:
                pass
    
    form=suscriptosEntreFechasForm()
    context['rango2']=form #guarda formulario vacío
    return render(request, 'appBookflix/buscarSuscriptores.html', context)




def leer_libro(request,isbn):
     context={}
     libro= Libro.objects.get(isbn = isbn)  #Aca recupero el libro por el isbn para no cambiar el template
     request.session["lectura_otro_perfil"] = False
     #if request.user.plan == 'normal' or request.user.plan == 'free' or request.user.plan == 'premium':
       # try:
        #    perfil = Profile.objects.exclude(id=request.session["perfil_ayuda"]).get(account=request.user) #aca agrego el isbn al objeto
        #    try: 
         #       state = StateOfBook.objects.get(state="reading", profile=perfil, book= libro.isbn)
         #       request.session["lectura_otro_perfil"] = True
         #   except StateOfBook.DoesNotExist:
         #       pass 
      #  except Profile.DoesNotExist:
        #    pass    
      #  try:
       #     estado_propio = StateOfBook.objects.get(state="reading", profile=request.session["perfil_ayuda"])
      #      comenzado = True
       #     context['comenzado']= comenzado
      #  except StateOfBook.DoesNotExist:
       #     comenzado = False
       #     context['comenzado']= comenzado
       #     context['terminado']= True

        

     try:
        estado = StateOfBook.objects.get(state="finished", profile=request.session["perfil_ayuda"],book=libro)
        context['terminado']= True
     except:
         context['terminado']= False


     libro = Libro.objects.get(isbn=isbn)
     try: 
        puntajeMio= Like.objects.get(book=libro, author= request.session['perfil_ayuda'])
     except: 
         puntajeMio= 0
     try:
         likes= Like.objects.filter(book= libro)
         cantLikes= Like.objects.filter(book= libro).count()
         puntaje= calcularPuntosDeLibro(likes, cantLikes)
     except: puntaje= 0

     comentarios= CommentBook.objects.filter(publication = libro)
     context['puntaje']= puntaje
     context['puntajeMio']= puntajeMio
     context['libro']= libro
     context['comentarios']= comentarios
     #Este try lo agregué para el Agregar y quitar de leyendo, reever en un futuro
     try:
        estado_propio = StateOfBook.objects.get(state="reading", profile=request.session["perfil_ayuda"],book=libro)
        comenzado = True
        context['comenzado']= comenzado
     except StateOfBook.DoesNotExist:
        comenzado = False
        context['comenzado']= comenzado
     #Fin del try de leyendo
     try:
        perfil = Profile.objects.get(id=request.session["perfil_ayuda"]) 
        favorito = LibroFavorito.objects.get(isbn=isbn, profile=perfil)
        context['agregar_favorito'] = False
     except LibroFavorito.DoesNotExist:
        context['agregar_favorito'] = True 
     try: 
        perfil = Profile.objects.get(id=request.session["perfil_ayuda"]) 
        libro = Libro.objects.get(isbn=isbn)
        futura_lectura = StateOfBook.objects.get(state="future_reading", profile=perfil, book=libro)
        context['agregar_futura_lectura'] = False
     except StateOfBook.DoesNotExist:
        context['agregar_futura_lectura'] = True    
     return render(request,"appBookflix/leer_libro.html",context) 



def leer_libro_por_capitulo(request,isbn):
     context= {}
     libro = BookByChapter.objects.get(isbn=isbn)
     if libro.mostrar_en_home == False:
        return redirect('/')
     cap_actual = 1
     capitulos=[]
     for i in range (0,libro.cant_chapter): 
        try: 
            Chapter.objects.get(book=libro, number=cap_actual, active=True) 
            capitulos.append(Chapter.objects.get(book=libro, number=cap_actual))
            cap_actual = cap_actual + 1
        except Chapter.DoesNotExist: 
            pass
        #capitulos = Chapter.objects.filter(book=libro)
     try: 
        puntajeMio= LikeBookByChapter.objects.get(book=libro, author= request.session['perfil_ayuda'])
     except: 
        puntajeMio= 0
     try:
        likes= LikeBookByChapter.objects.filter(book= libro)
        cantLikes= LikeBookByChapter.objects.filter(book= libro).count()
        puntaje= calcularPuntosDeLibro(likes, cantLikes)
     except: puntaje= 0

     comentarios= CommentBookByChapter.objects.filter(publication = libro)
     context['capitulos']=capitulos
     context['libro']= libro
     context['comentarios']= comentarios
     context['puntaje']= puntaje
     context['puntajeMio']= puntajeMio



     #desde acá empiezo a agregar funcionalidades del otro leer

     
     request.session["lectura_otro_perfil"] = False
     if request.user.plan == 'normal'  :
        try:
            perfil = Profile.objects.exclude(id=request.session["perfil_ayuda"]).get(account=request.user) #aca agrego el isbn al objeto
            try: 
                state = StateOfBookByChapter.objects.get(state="reading", profile=perfil, book= libro.isbn)
                request.session["lectura_otro_perfil"] = True
            except StateOfBookByChapter.DoesNotExist:
                pass 
        except Profile.DoesNotExist:
            pass    
        try:
            estado_propio = StateOfBookByChapter.objects.get(state="reading", profile=request.session["perfil_ayuda"])
            comenzado = True
            context['comenzado']= comenzado
        except StateOfBookByChapter.DoesNotExist:
            comenzado = False
            context['comenzado']= comenzado
            context['terminado']= True

            ##
            state = StateOfBookByChapter.objects.get(state="finished", profile=perfil, book= libro.isbn)
            context['terminado']= True

     try:
        estado = StateOfBookByChapter.objects.get(state="finished", book=libro, profile=request.session["perfil_ayuda"])
        context['terminado']= True
     except:
         context['terminado']= False


     libro = BookByChapter.objects.get(isbn=isbn)
     try: 
        puntajeMio= Like.objects.get(book=libro, author= request.session['perfil_ayuda'])
     except: 
         puntajeMio= 0
     try:
         likes= LikeBookByChapter.objects.filter(book=libro)
         cantLikes= LikeBookByChapter.objects.filter(book=libro).count()
         puntaje= calcularPuntosDeLibro(likes, cantLikes)
     except: puntaje= 0

     comentarios= CommentBookByChapter.objects.filter(publication = libro)
     context['puntaje']= puntaje
     context['puntajeMio']= puntajeMio
     context['libro']= libro
     context['comentarios']= comentarios
     #Este try lo agregué para el Agregar y quitar de leyendo, reever en un futuro
     try:
        estado_propio = StateOfBookByChapter.objects.get(state="reading", book=libro, profile=request.session["perfil_ayuda"])
        comenzado = True
        context['comenzado']= comenzado
     except StateOfBookByChapter.DoesNotExist:
        comenzado = False
        context['comenzado']= comenzado
     #Fin del try de leyendo
     try:
        perfil = Profile.objects.get(id=request.session["perfil_ayuda"]) 
        favorito = LibroPorCapituloFavorito.objects.get(isbn=isbn, profile=perfil)
        context['agregar_favorito'] = False
     except LibroPorCapituloFavorito.DoesNotExist:
        context['agregar_favorito'] = True 
     try: 
        perfil = Profile.objects.get(id=request.session["perfil_ayuda"]) 
        libro = BookByChapter.objects.get(isbn=isbn)
        futura_lectura = StateOfBookByChapter.objects.get(state="future_reading", book=libro, profile=perfil)
        context['agregar_futura_lectura'] = False
     except StateOfBookByChapter.DoesNotExist:
        context['agregar_futura_lectura'] = True 

    
     favoritos = CapituloFavorito.objects.filter(profile=perfil, book=libro)#.values("titulo_capitulo")
     
     context["favoritos"]= favoritos
     
     return render(request,"appBookflix/libro_capitulo.html",context) 


#acciones de usuario con los libros

def agregar_futuras_lecturas(request,isbn):
    perfil = Profile.objects.get(id=request.session["perfil_ayuda"])
    libro = Libro.objects.get(isbn=isbn)
    #variable = StateOfBook(state="future_reading",book=libro, profile=perfil)
    try:
        variable = StateOfBook.objects.get(book=libro, profile=perfil)
        variable.state= "future_reading"
    except StateOfBook.DoesNotExist:
        variable = StateOfBook(book=libro,profile=perfil,state="future_reading")
    variable.save()
    return redirect(to="/leer_libro/"+ str(isbn))

def quitar_futuras_lecturas(request,isbn):
    perfil = Profile.objects.get(id=request.session["perfil_ayuda"])
    libro = Libro.objects.get(isbn=isbn)
    #variable = StateOfBook(state="future_reading",book=libro, profile=perfil)
    variable = StateOfBook.objects.get(book=libro, profile=perfil)
    variable.state= "null"
    variable.save()
    return redirect(to="/leer_libro/"+ str(isbn))


def agregar_futuras_lecturas_libro_cap(request,isbn):
    perfil = Profile.objects.get(id=request.session["perfil_ayuda"])
    libro = BookByChapter.objects.get(isbn=isbn)
    try:
        variable = StateOfBookByChapter.objects.get(book=libro, profile=perfil)
        variable.state= "future_reading"
    except StateOfBookByChapter.DoesNotExist:
        variable = StateOfBookByChapter(book=libro,profile=perfil,state="future_reading")
    variable.save()
    return redirect(to="/libro_capitulo/"+ str(isbn))


def quitar_futuras_lecturas_libro_cap(request,isbn):
    perfil = Profile.objects.get(id=request.session["perfil_ayuda"])
    libro = BookByChapter.objects.get(isbn=isbn)
    variable = StateOfBookByChapter.objects.get(book=libro, profile=perfil)
    variable.state= "null"
    variable.save()
    return redirect(to="/libro_capitulo/"+ str(isbn))

def agregar_libro_favoritos(request,isbn):
    perfil = Profile.objects.get(id=request.session["perfil_ayuda"])
    libro = Libro.objects.get(isbn=isbn)
    favorito = LibroFavorito(isbn=isbn, profile=perfil, book=libro)
    favorito.save()
    return redirect(to="/leer_libro/"+ str(isbn))

def agregar_libro_cap_favoritos(request,isbn):
    perfil = Profile.objects.get(id=request.session["perfil_ayuda"])
    libro = BookByChapter.objects.get(isbn=isbn)
    favorito = LibroPorCapituloFavorito(isbn=isbn, profile=perfil, book=libro)
    favorito.save()
    return redirect(to="/libro_capitulo/"+ str(isbn))


def agregar_cap_favoritos(request,isbn,titulo):
    perfil = Profile.objects.get(id=request.session["perfil_ayuda"])
    libro = BookByChapter.objects.get(isbn=isbn)
    capitulo = Chapter.objects.get(book=libro, title=titulo)
    favorito = CapituloFavorito(profile=perfil, book=libro, titulo_capitulo=titulo, capitulo=capitulo)
    favorito.save()
    return redirect(to="/libro_capitulo/"+ str(isbn))


def quitar_libro(request,isbn):
    perfil = Profile.objects.get(id=request.session["perfil_ayuda"])
    favorito = LibroFavorito.objects.get(isbn=isbn, profile=perfil)
    favorito.delete()
    return redirect(to="/leer_libro/"+ str(isbn))


def quitar_libro_cap(request,isbn):
    perfil = Profile.objects.get(id=request.session["perfil_ayuda"])
    favorito = LibroPorCapituloFavorito.objects.get(isbn=isbn, profile=perfil)
    favorito.delete()
    return redirect(to="/libro_capitulo/"+ str(isbn))


def quitar_cap_favoritos(request,isbn,titulo):
    perfil = Profile.objects.get(id=request.session["perfil_ayuda"])
    libro = BookByChapter.objects.get(isbn=isbn)
    capitulo = Chapter.objects.get(book=libro, title=titulo)
    favorito = CapituloFavorito.objects.get(profile=perfil, book=libro, titulo_capitulo=titulo, capitulo=capitulo)
    favorito.delete()
    return redirect(to="/libro_capitulo/"+ str(isbn))



def listar_favoritos(request):
    perfil = Profile.objects.get(id=request.session["perfil_ayuda"])
    libros_favoritos = LibroFavorito.objects.filter(profile=perfil)
    libros_por_capitulo_favoritos = LibroPorCapituloFavorito.objects.filter(profile=perfil)
    return render(request,"bookflix/listar_favoritos.html", {"libros_favoritos":libros_favoritos, "libros_por_capitulo_favoritos":libros_por_capitulo_favoritos})

def agregar_a_leyendo(request,isbn):
    perfil = Profile.objects.get(id=request.session["perfil_ayuda"])
    libro = Libro.objects.get(isbn=isbn)
    try:
        variable = StateOfBook.objects.get(book=libro, profile=perfil)
        variable.state= "reading"
    except StateOfBook.DoesNotExist:
        variable = StateOfBook(state="reading",book=libro, profile=perfil)
    variable.save()
    return redirect(to="/leer_libro/"+ str(isbn))

def agregar_a_leyendo_libro_cap(request,isbn):
    perfil = Profile.objects.get(id=request.session["perfil_ayuda"])
    libro = BookByChapter.objects.get(isbn=isbn)
    try:
        variable = StateOfBookByChapter.objects.get(book=libro, profile=perfil)
        variable.state= "reading"
    except StateOfBookByChapter.DoesNotExist:
        variable = StateOfBookByChapter(state="reading",book=libro, profile=perfil)
    variable.save()
    return redirect(to="/libro_capitulo/"+ str(isbn))


def quitar_de_leyendo(request,isbn):
    perfil = Profile.objects.get(id=request.session["perfil_ayuda"])
    libro = Libro.objects.get(isbn=isbn)
    variable = StateOfBook.objects.get(book=libro, profile=perfil)
    variable.state= "null"
    variable.save()
    return redirect(to="/leer_libro/"+ str(isbn))


def quitar_de_leyendo_libro_cap(request,isbn):
    perfil = Profile.objects.get(id=request.session["perfil_ayuda"])
    libro = BookByChapter.objects.get(isbn=isbn)
    variable = StateOfBookByChapter.objects.get(book=libro, profile=perfil)
    variable.state= "null"
    variable.save()
    return redirect(to="/libro_capitulo/"+ str(isbn))



def terminar_libro(request,isbn):
    perfil = Profile.objects.get(id=request.session["perfil_ayuda"])
    libro = Libro.objects.get(isbn=isbn)
    variable = StateOfBook.objects.get(book=libro, profile=perfil)
    variable.state="finished"
    variable.save()
    return redirect(to="/leer_libro/"+ str(isbn))

def terminar_libro_cap(request,isbn):
    perfil = Profile.objects.get(id=request.session["perfil_ayuda"])
    libro = BookByChapter.objects.get(isbn=isbn)
    variable = StateOfBookByChapter.objects.get(book=libro, profile=perfil)
    variable.state="finished"
    variable.save()
    return redirect(to="/libro_capitulo/"+ str(isbn))

#Esta función se puede obviar porque agregar a leyendo hace lo mismo que se necesita, pero la dejo por si en un futuro se marean
def quitar_terminado(request,isbn):
    perfil = Profile.objects.get(id=request.session["perfil_ayuda"])
    libro = Libro.objects.get(isbn=isbn)
    variable = StateOfBook.objects.get(book=libro, profile=perfil)
    variable.state= "reading"
    variable.save()
    return redirect(to="/leer_libro/"+ str(isbn))




def libro_cap_por_leer(request,isbn):
    libro = BookByChapter.object.get(isbn=isbn)
    perfil = Profile.object.get(id=request.session["perfil_ayuda"])
    variable = StateOfBookByChapter(state="reading",book=libro, profile=perfil)
    return render(request,"bookflix/libro_por_leer.html", {"libro":libro} )
     

def historial(request):
     historial_libros = StateOfBook.objects.filter(state="finished")
     historial_libros_cap = StateOfBookByChapter.objects.filter(state="finished")
     #historial = historial_libros_cap |= historial_libros
     sesion = request.session
     return render(request,"appBookflix/historial.html",{"historial_libros":historial_libros,"historial_libros_cap":historial_libros_cap, "sesion":sesion }) 

def listar_favoritos(request):
    perfil = Profile.objects.get(id=request.session["perfil_ayuda"])
    libros_favoritos = LibroFavorito.objects.filter(profile=perfil)
    libros_por_capitulo_favoritos = LibroPorCapituloFavorito.objects.filter(profile=perfil)
    capitulos_favoritos = CapituloFavorito.objects.filter(profile=perfil)
    return render(request,"appBookflix/favoritos.html", {"libros_favoritos":libros_favoritos, "libros_por_capitulo_favoritos":libros_por_capitulo_favoritos,"capitulos_favoritos":capitulos_favoritos})


def trailers(request):
    trailers = Trailer.objects.filter(mostrar_en_home=True)
    return render(request,"appBookflix/trailers.html",{"trailers":trailers})



def mas_leidos (request):

    context={}
    libro= StateOfBook.objects.filter(state="finished").values('book').annotate(terminado=models.Count('book'))
    libroCap= StateOfBookByChapter.objects.filter(state="finished").values('book').annotate(terminado=models.Count('book'))

    libro2= sorted(libro, key = lambda user: user['terminado'])
    libro2= libro2[::-1]    
    libro4= sorted(libroCap, key = lambda user: user['terminado'])
    libro4= libro4[::-1]    
    libro3=[]
    libro5=[]
    for i in libro2:
        l4= Libro.objects.get(isbn= i['book'])
        libro3.append({'libro':l4, 'cantidad': i['terminado']})
    for i in libro4:
        l4= BookByChapter.objects.get(id= i['book'])
        libro5.append({'libro':l4, 'cantidad': i['terminado']})
    context['libros']= libro3
    context['librosCap']= libro5
    
    return render(request,'appBookflix/mas_leidos.html', context)




#ELIMINAR

def borrar_perfil(request,perfil):
    perfil_a_borrar = Profile.objects.get(account=request.user, name=perfil)
    return render(request,"appBookflix/borrar_perfil.html", {"perfil":perfil_a_borrar})


def borrar_perfil_definitivo(request,perfil):
    perfil_a_borrar = Profile.objects.get(account=request.user, name=perfil)
    perfil_a_borrar.delete()
    request.session["perfil_ayuda"] = False
    request.session['nombrePerfil']= False
    request.session['perfil_actual']= None
    request.session.modified = True
    return redirect(to="/select_perfil")

def borrar_cuenta(request):
    return render(request,"appBookflix/borrar_cuenta.html")


def borrar_cuenta_definitivo(request):
    cuenta = Account.objects.get(id=request.user.id)
    cuenta.delete()
    return redirect(to="/login")



#SOLICITUDES

def solicitar_cambio(request):
    context= { }
    request.session["solicitud"]="1"
    request.session.modified = True
    try:
        cambio_plan =  UserSolicitud.objects.get(is_accepted=0, user=request.user)
        request.session["solicitud"]="0"
        request.session.modified = True
    except UserSolicitud.DoesNotExist: 
        pass
    request.session['ErrorSolicitudCambio']= "Su plan es: " + request.user.plan + ". Si selecciona el mismo no tendrá efecto" 
    request.session.modified = True
    if request.POST:   
        form= UserSolicitudForm(request.POST)
        if form.is_valid():
            planSolicitad= form.cleaned_data['tipo_de_plan']
            if planSolicitad == request.user.plan:
                request.session['ErrorSolicitudCambio']="No puede seleccionar un plan"
                request.session.modified=True
            elif planSolicitad == 'free':
                sol=UserSolicitud(type_of_solicitud='baja', type_of_plan='free', user= request.user)
                sol.save()
                return redirect('/perfil')
            elif planSolicitad == 'normal':
                if request.user.plan == 'free':
                    sol= UserSolicitud(type_of_solicitud='alta', type_of_plan='normal', user= request.user)
                    sol.save()
                else:
                    sol= UserSolicitud(type_of_solicitud='cambio', type_of_plan='normal', user= request.user)
                    sol.save()
                return redirect('/perfil')    
            else:
                if request.user.plan == 'free':
                    sol= UserSolicitud(type_of_solicitud='alta', type_of_plan='premium', user= request.user)
                    sol.save()
                else: 
                    sol= UserSolicitud(type_of_solicitud='cambio', type_of_plan='premium', user= request.user)
                    sol.save()
                return redirect('/perfil') 
    form= UserSolicitudForm()
    context['solicitud'] = form
    return render(request,"appBookflix/solicitar_cambio.html", context)



def aceptarSolicitud(request,idSol,num):
    try:
        sol= UserSolicitud.objects.get(id=idSol)
        
        if num == '1':
            userSol= UserSolicitud.objects.filter(id=idSol).values('user')
            us= Account.objects.get(id__in=userSol)
            sol.is_accepted= num
            sol.save()
            us.plan= sol.type_of_plan
            us.time_pay=30
            us.date_start_plan= timezone.now()
            us.save()
        else:
            sol.is_accepted=num
            sol.save()
    except UserSolicitud.DoesNotExist:
        pass
    return redirect('/solicitudes')   




#BUSCAR

def buscar(request):
    context={ }
    if request.POST:
        form= BuscarForm(request.POST)
        if form.is_valid():

            def buscar_por_autor(query):
                autores = Autor.objects.filter(nombre__icontains=query)
                autores2 = Autor.objects.filter(apellido__icontains=query)
                result = []
                for autor in autores:
                    result = result + list(Libro.objects.filter(autor=autor, mostrar_en_home=True))
                for autor in autores2:
                    result = result + list(Libro.objects.filter(autor=autor, mostrar_en_home=True))
                return result

            def buscar_por_genero(query):
                generos = Genero.objects.filter(nombre__icontains=query)
                result = []
                for genero in generos:
                    result = result + list(Libro.objects.filter(genero=genero, mostrar_en_home=True))
                return result

            def buscar_por_editorial(query):
                editoriales = Editorial.objects.filter(name__icontains=query)
                result = []
                for editorial in editoriales:
                    result = result + list(Libro.objects.filter(editorial=editorial, mostrar_en_home=True))
                return result

            def buscar_por_titulo(query):
                result = Libro.objects.filter(titulo__icontains=query)
                return result


            def buscar_por_autorCap(query):
                autores = Autor.objects.filter(nombre__icontains=query)
                autores2 = Autor.objects.filter(apellido__icontains=query)
                result = []
                for autor in autores:
                    result = result + list(BookByChapter.objects.filter(autor=autor, mostrar_en_home=True))
                for autor in autores2:
                    result = result + list(BookByChapter.objects.filter(autor=autor, mostrar_en_home=True))
                return result

            def buscar_por_generoCap(query):
                generos = Genero.objects.filter(nombre__icontains=query)
                result = []
                for genero in generos:
                    result = result + list(BookByChapter.objects.filter(genders=genero, mostrar_en_home=True))
                return result

            def buscar_por_editorialCap(query):
                editoriales = Editorial.objects.filter(name__icontains=query)
                result = []
                for editorial in editoriales:
                    result = result + list(BookByChapter.objects.filter(editorial=editorial, mostrar_en_home=True))
                return result

            def buscar_por_tituloCap(query):
                result = BookByChapter.objects.filter(title__icontains=query, mostrar_en_home=True)
                return result

            def buscar_por_isbn(query):
                result = Libro.objects.filter(isbn=query, mostrar_en_home=True)
                return result

            def buscar_por_isbnCap(query):
                result = BookByChapter.objects.filter(isbn=query, mostrar_en_home=True)
                return result

            palabra= form.cleaned_data['buscar']
            query= str(palabra).split(' ')
            allBook = Libro.objects.filter(mostrar_en_home = True)
            AllBookCap= BookByChapter.objects.filter(mostrar_en_home = True)
            results=set()
            resultsCap=set()
            for palabra in query:

                #if buscar_por_autor(palabra):
                resultsAutor = set(allBook) & set(buscar_por_autor(palabra))
                #if buscar_por_genero(palabra):
                resultsGenero =  set(allBook)  & set(buscar_por_genero(palabra))
                #if buscar_por_titulo(palabra):
                resultsTitulo =  set(allBook)  & set(buscar_por_titulo(palabra))
                #if buscar_por_editorial(palabra):                    
                resultsEditorial = set(allBook)  & set(buscar_por_editorial(palabra))
                resultsIsbn= set(allBook) & set(buscar_por_isbn(palabra))
                results= results | (resultsAutor | resultsGenero | resultsTitulo | resultsEditorial | resultsIsbn)

                #if buscar_por_autorCap(palabra):
                resultsAutor = set(AllBookCap) & set(buscar_por_autorCap(palabra))
                #if buscar_por_generoCap(palabra):
                resultsGenero = set(AllBookCap) & set(buscar_por_generoCap(palabra))
                #if buscar_por_tituloCap(palabra):
                resultsTitulo = set(AllBookCap) & set(buscar_por_tituloCap(palabra))
                #if buscar_por_editorialCap(palabra):
                resultsEditorial = set(AllBookCap) & set(buscar_por_editorialCap(palabra))
                resultsIsbn= set(AllBookCap) & set(buscar_por_isbnCap(palabra))
                resultsCap= resultsCap | (resultsAutor | resultsGenero | resultsTitulo | resultsEditorial | resultsIsbn)

            context['libros']= set(results)
            context['librosCap']= set(resultsCap) 
    else:
        context['libros']= Libro.objects.all()
        context['librosCap']= BookByChapter.objects.all()
    form=BuscarForm()
    context['form']= form
    return render(request, "appBookflix/buscar.html", context)




#Funciones de automatizacion, escribir cualquier otra view antes que esta

def simuladorTemporal(request):
    context={}
   #Libros
    try:
        Lib= UpDownBook.objects.filter(up_normal =timezone.now()).values('book')
        li= Libro.objects.filter(isbn__in=Lib)
        cambioNormal(li, True)
        
    except UpDownBook.DoesNotExist:
        pass
    try:
        Lib= UpDownBook.objects.filter(expiration_normal=timezone.now().date()).values('book')         
        li= Libro.objects.filter(isbn__in=Lib)
        cambioNormal(li, False)
    except UpDownBook.DoesNotExist:
        pass
    try:
        Lib= UpDownBook.objects.filter(up_premium =timezone.now()).values('book')
        li= Libro.objects.filter(isbn__in=Lib)
        cambioPremium(li, True)
    except UpDownBook.DoesNotExist:
        pass
    try:
        Lib= UpDownBook.objects.filter(expiration_premium=timezone.now().date()).values('book')         
        li= Libro.objects.filter(isbn__in=Lib)
        cambioPremium(li,False)
    except UpDownBook.DoesNotExist:
        pass

    #LibrosPorCapitulo
    try:
        Lib= UpDownBookByChapter.objects.filter(up_normal =timezone.now()).values('book')
        li= BookByChapter.objects.filter(id__in=Lib)
        cambioNormal(li, True)
    except UpDownBookByChapter.DoesNotExist:
        pass
    try:
        Lib= UpDownBookByChapter.objects.filter(expiration_normal=timezone.now().date()).values('book')         
        li= BookByChapter.objects.filter(id__in=Lib)
        cambioNormal(li, False)
    except UpDownBookByChapter.DoesNotExist:
        pass
    try:
        Lib= UpDownBookByChapter.objects.filter(up_premium =timezone.now()).values('book')
        li= BookByChapter.objects.filter(id__in=Lib)
        cambioPremium(li, True)
    except UpDownBookByChapter.DoesNotExist:
        pass
    try:
        Lib= UpDownBookByChapter.objects.filter(expiration_premium=timezone.now().date()).values('book')         
        li= BookByChapter.objects.filter(id__in=Lib)
        cambioPremium(li,False)
    except UpDownBookByChapter.DoesNotExist:
        pass
    
    #Capitulos

    try:
        cha= UpDownChapter.objects.filter(up =timezone.now()).values('chapter')
        c= Chapter.objects.filter(id__in=cha)
        cambioOtros(c, True )
    except Chapter.DoesNotExist: 
        pass
    try:
        cha= UpDownChapter.objects.filter(expirationl =timezone.now()).values('chapter')
        c= Chapter.objects.filter(id__in=cha)
        cambioOtros(c, False )
    except Chapter.DoesNotExist: pass

    #Novedades

    try:
        cha= UpDownNovedad.objects.filter(up =timezone.now()).values('Novedad')
        c= Novedad.objects.filter(id__in=cha)
        cambioBilTra(c, True )
    except Novedad.DoesNotExist: pass
    try:
        cha= UpDownNovedad.objects.filter(expirationl =timezone.now()).values('Novedad')
        c= Novedad.objects.filter(id__in=cha)
        cambioBilTra(c, False )
    except Novedad.DoesNotExist: pass

    #Trailer

    try:
        cha= UpDownTrailer.objects.filter(up =timezone.now()).values('trailer')
        c= Trailer.objects.filter(id__in=cha)
        cambioBilTra(c, True )
    except Trailer.DoesNotExist: pass
    try:
        cha= UpDownTrailer.objects.filter(expirationl =timezone.now()).values('trailer')
        c= Trailer.objects.filter(id__in=cha)
        cambioBilTra(c, False )
    except Trailer.DoesNotExist: pass

    #Bajas usuarios
    try:
        sol= UserSolicitud.objects.filter(type_of_solicitud='baja', is_accepted=0).values('user', 'is_accepted', 'id')
        darDeBajaUsuarios(sol)
        context['libros']= sol
    except UserSolicitud.DoesNotExist: pass


    try:
        sol= UserSolicitud.objects.filter(type_of_solicitud='cambio', type_of_plan='normal', is_accepted=0).values('user', 'is_accepted', 'id')
        CambiarjaUsuariosNormal(sol)
        context['libros']= sol
    except UserSolicitud.DoesNotExist: pass

    try:
        sol= UserSolicitud.objects.filter(type_of_solicitud='cambio', type_of_plan='premium', is_accepted=0).values('user', 'is_accepted', 'id')
        CambiarjaUsuariosPremium(sol)
        context['libros']= sol
    except UserSolicitud.DoesNotExist: pass
    return redirect('/solicitudes')








    