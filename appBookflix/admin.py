from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django import forms


from  appBookflix.models import *
#from .forms import ChapForm



class AccountAdmin(UserAdmin): 
    list_display= ('email', 'username', 'date_joined', 'plan') #lo que voy a ver en las columnas del dashboard del administrador
    search_fields= ('email', 'username') #los parámetros por los que permito buscar
    readonly_fields= ('last_login', 'date_joined') #atributos que no se pueden cambiar, los hago solo de lectura

    filter_horizontal= ()
    list_filter=()
    fieldsets=() #NI IDEA PERO SI NO PONÉS ESTOS TRES, TIRA ERROR

admin.site.register(Autor)
admin.site.register(Genero)
admin.site.register(Editorial)
admin.site.register(Libro)
admin.site.register(CreditCards)
admin.site.register(BookByChapter)
admin.site.register(Novedad)
#admin.site.register(Usuario)
admin.site.register(Account, AccountAdmin)