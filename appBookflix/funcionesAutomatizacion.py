def cambioNormal(lista, bool):
    for l in lista:
        l.on_normal= bool
        l.save()

def cambioPremium(lista, bool):
    for l in lista:
        l.on_premium= bool
        l.save()
def cambioOtros(lista, bool):
    for l in lista:
        l.active=bool
        l.save()
def cambioBilTra(lista, bool):
    for l in lista:
        l.mostrar_en_home=bool
        l.save()

import datetime
from django.utils import timezone
from .models import Account, UserSolicitud, StateOfBook, StateOfBookByChapter, Libro, BookByChapter, Genero, Editorial, Autor

def darDeBajaUsuarios(objectAccounts):

    for acc in objectAccounts:
        if timezone.now().date() == (acc.date_start_plan + datetime.timedelta(days=acc.time_pay)):
            acc.plan = 'free'
            acc. time_pay = 0
            acc.save()
            
from random import randint, uniform
import random



    
def recomendados(perfil):
    lib= Libro.objects.all()
    def randomCood(num):
        if num >= 1:
            unique_id = random.randint(0,(num-1))
            return unique_id
        return num
#Primero selecciono unlibros que el usuario leyo, de forma random
    try:
        estados= StateOfBook.objects.filter(profile_id =perfil.id, state='finished').values('book')
        
        libros_leidos=[]
        for i in estados:
            libros_leidos.append(Book.objects.get(id = i['book']))
    #Aqui saco el libro random leido para buscar otros con características similares
        
        libroARandom=libros_leidos[randomCood(len(libros_leidos))]

    #Recupero algun libro con alguno de los generos de ese libro
        generos= libroARandom.genders.all()
        aux= [ ]
        for genero in generos:
            aux.append(genero)
        genero= aux[randomCood(len(aux))]
            
        librosConEseGenero= set(Libro.objects.filter(genders=genero, mostrar_en_home=True)) - set(libros_leidos)
        librosDeEseGenero=librosConEseGenero
        
    #Recupero Algun Libro de esa Editorial
        editorial= libroARandom.editorial
        
        librosConEsaEditorial= set(Libro.objects.filter(editorial=editorial, mostrar_en_home=True)) - set(libros_leidos)
        librodeEsaEditorial= librosConEsaEditorial
        
    #Recupero Libro de Ese Autor
        autor= libroARandom.author
        librosConEseAutor= set(Libro.objects.filter(author=autor, mostrar_en_home=True)) - set(libros_leidos)
        libroDeEseAutor=librosConEseAutor

        auxiliar=  librodeEsaEditorial | libroDeEseAutor | librosDeEseGenero

        if len(auxiliar)> 0:
            return auxiliar
        return  ( set(lib) - set(libros_leidos) )
       
    except:
        
        return  set(lib)

def recomendadosCap(perfil):
    lib= BookByChapter.objects.all()
    
    def randomCood(num):
        if num >= 1:
            unique_id = random.randint(0,(num-1))
            return unique_id
        return num
#Primero selecciono unlibros que el usuario leyo, de forma random
    try:
        estados= StateOfBookByChapter.objects.filter(profile_id =perfil.id, state='finished').values('book')
        
        libros_leidos=[]
        for i in estados:
            libros_leidos.append(BookByChapter.objects.get(id = i['book']))
    #Aqui saco el libro random leido para buscar otros con características similares
        
        libroARandom=libros_leidos[randomCood(len(libros_leidos))]

    #Recupero algun libro con alguno de los generos de ese libro
        generos= libroARandom.genders.all()
        aux= [ ]
        for genero in generos:
            aux.append(genero)
        genero= aux[randomCood(len(aux))]
            
        librosConEseGenero= set(BookByChapter.objects.filter(genders=genero, mostrar_en_home=True)) - set(libros_leidos)
        librosDeEseGenero=librosConEseGenero
        
    #Recupero Algun Libro de esa Editorial
        editorial= libroARandom.editorial
        
        librosConEsaEditorial= set(BookByChapter.objects.filter(editorial=editorial, mostrar_en_home=True)) - set(libros_leidos)
        librodeEsaEditorial= librosConEsaEditorial
        
    #Recupero Libro de Ese Autor
        autor= libroARandom.author
        librosConEseAutor= set(BookByChapter.objects.filter(author=autor, mostrar_en_home=True)) - set(libros_leidos)
        libroDeEseAutor=librosConEseAutor

        auxiliar=  librodeEsaEditorial | libroDeEseAutor | librosDeEseGenero
        if len(auxiliar)> 0:
            return auxiliar
        return  ( set(lib) - set(libros_leidos) )

    except:
       
        return  set(lib)