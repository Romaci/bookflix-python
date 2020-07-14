from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django import forms


from  .models import *
from .forms import *



class ChapterAdmin(admin.ModelAdmin):
    form = ChapForm
    list_display = ('book', 'title', 'number', 'description', 'pdf', 'active')


class SolicitudAdmin(admin.ModelAdmin):
    form = SolicitudFormAdmin
    list_display= ('type_of_solicitud', 'type_of_plan', 'user', 'date_of_solicitud', 'is_accepted')


class AccountAdmin(UserAdmin): 
    list_display= ('email', 'username', 'date_joined', 'plan') #lo que voy a ver en las columnas del dashboard del administrador
    search_fields= ('email', 'username') #los parámetros por los que permito buscar
    readonly_fields= ('last_login', 'date_joined') #atributos que no se pueden cambiar, los hago solo de lectura

    filter_horizontal= ()
    list_filter=()
    fieldsets=() #NI IDEA PERO SI NO PONÉS ESTOS TRES, TIRA ERROR


class UserCreationForm(forms.ModelForm):
    password1 = forms.CharField(label='Password', widget=forms.PasswordInput)
    password2 = forms.CharField(label='Password confirmation', widget=forms.PasswordInput)

    class Meta:
        model = Account
        fields = '__all__'

    def clean_password2(self):
        password1 = self.cleaned_data.get("password1")
        password2 = self.cleaned_data.get("password2")
        if password1 and password2 and password1 != password2:
            raise forms.ValidationError("Password no son iguales")
        return password2

    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data["password1"])
        if commit:
            user.save()
        return user

admin.site.register(Autor)
admin.site.register(Genero)
admin.site.register(Editorial)
admin.site.register(Libro)
admin.site.register(CreditCards)
admin.site.register(BookByChapter)
admin.site.register(Novedad)
admin.site.register(Trailer)
#admin.site.register(Usuario)
admin.site.register(Account, AccountAdmin)
admin.site.register(CapituloFavorito)
admin.site.register(CommentBook)

admin.site.register(CreditCardsUsed)
admin.site.register(Like)
admin.site.register(LikeBookByChapter)

admin.site.register(Profile)
admin.site.register(UserSolicitud, SolicitudAdmin)

admin.site.register(StateOfBook)
admin.site.register(StateOfBookByChapter)

admin.site.register(UpDownBook)
admin.site.register(UpDownBookByChapter)
admin.site.register(UpDownChapter)
admin.site.register(UpDownNovedad)
admin.site.register(UpDownTrailer)
admin.site.register(LibroFavorito)
admin.site.register(LibroPorCapituloFavorito)

#admin.site.register(PuntuacionDeLibro)


#admin.site.register(Chapter)
admin.site.register(Chapter, ChapterAdmin)
