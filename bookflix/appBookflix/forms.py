from django import forms
from .models import *
from django.views.decorators.csrf import csrf_protect
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import authenticate
from django.forms import ModelForm
from django.forms import ValidationError
from datetime import datetime, timedelta
from creditcards.forms import CardNumberField, CardExpiryField, SecurityCodeField



class UserSolicitudForm(forms.Form):
    CHOICESS= GEEKS_CHOICES =( 
    ("free", "free"), 
    ("normal", "normal"), 
    ("premium", "premium"), )

    tipo_de_plan= forms.ChoiceField(label="Seleccione Plan", choices=CHOICESS, )


#class MailConfirmacion(forms.Form):
    #codigoV = forms.CharField(label='codigo Validacion')


class RegistroTarjeta(forms.Form):
    number = CardNumberField(label='Número de tarjeta',error_messages = {'invalid': 'La tarjeta debe tener entre 12 y 16 numeros'})
    date_expiration = CardExpiryField(error_messages = {'date_passed': 'Fecha Invalida', } )
    cod = SecurityCodeField(error_messages = {'invalid': 'Código inválido'},)
    card_name = forms.CharField( max_length=50)
    bank = forms.CharField(max_length=50)
    

class RegistrationForm(UserCreationForm):
    email = forms.EmailField(required=True)
    class Meta:
        model = Account
        fields = (  
            'username',
            'email',
            'password1',
            'password2',            
        )

class CrearPerfil(ModelForm):
    class Meta: 
        model = Profile
        fields = ('name',)

class MailChange(ModelForm):

    class Meta: 
        model = Account
        fields = ('email',)

    def clean_email(self):
        if self.is_valid():
            email=self.cleaned_data['email']
            try:
                account= Account.objects.exclude(pk=self.instance.pk).get(email=email)
            except Account.DoesNotExist:
                return email
            raise forms.ValidationError("el mail se encuentra en uso" )
