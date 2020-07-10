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
            
            numT= formCard.cleaned_data.get("number")
            codT= formCard.cleaned_data.get("cod")
            dateT= formCard.cleaned_data.get("date_expiration")
            cardName= formCard.cleaned_data.get("card_name")
            bankT=formCard.cleaned_data.get("bank")

            tarjeta= CreditCards(number=numT, cod=codT, date_expiration=dateT, card_name=cardName, bank=bankT, user=cuenta)
            tarjeta.save()
            
            return redirect('login')
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
    return redirect('/login')




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




def leer_libro(request,isbn):
     context={}
     libro= Libro.objects.get(isbn = isbn)  #Aca recupero el libro por el isbn para no cambiar el template
     request.session["lectura_otro_perfil"] = False
     if request.user.plan == 'normal':
        try:
            perfil = Profile.objects.exclude(id=request.session["perfil_ayuda"]).get(account=request.user) #aca agrego el isbn al objeto
            try: 
                state = StateOfBook.objects.get(state="reading", profile=perfil, book= libro.id)
                request.session["lectura_otro_perfil"] = True
            except StateOfBook.DoesNotExist:
                pass 
        except Profile.DoesNotExist:
            pass    
        try:
            estado_propio = StateOfBook.objects.get(state="reading", profile=request.session["perfil_ayuda"])
            comenzado = True
            context['comenzado']= comenzado
        except StateOfBook.DoesNotExist:
            comenzado = False
            context['comenzado']= comenzado
            context['terminado']= True

            ##
            state = StateOfBook.objects.get(state="finished", profile=perfil, book= libro.id)
            context['terminado']= True

     try:
        estado = StateOfBook.objects.get(state="finished", profile=request.session["perfil_ayuda"])
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
        estado_propio = StateOfBook.objects.get(state="reading", profile=request.session["perfil_ayuda"])
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
