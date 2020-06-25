from django.contrib.auth.models import AbstractBaseUser, BaseUserManager
from django.db import models
from django.core.exceptions import FieldError, ValidationError
from datetime import datetime
from django.utils import timezone
from creditcards.models import CardNumberField, CardExpiryField, SecurityCodeField



#ACCOUNT MANAGER
class MyAccountManager(BaseUserManager):
    def create_user(self, email, username, password=None):
        """
        Creates and saves a User with the given email and password.
        """
        if not email:
            raise ValueError('El email es requerido')
        if not username:
            raise ValueError('El nombre de usuario es requerido')
        
        user = self.model(email=self.normalize_email(email), username=username)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, username, password):
        user = self.create_user(
            email=self.normalize_email(email),
            password=password,
            username=username
        )
        user.is_admin=True
        user.is_staff=True
        user.is_superuser=True
        user.is_active=True
        user.confirmo=True
        user.save(using=self.db)
        return user

    """ def get_by_natural_key(self, username):
       return self.get(username=username)"""



#Account
class Account(AbstractBaseUser):

    #Valores para los diferentes tipos de cuenta
    free='free'
    normal='normal'
    premium='premium'
    admin = 'admin'
    AC_CHOICES= (
        (free, 'free'),
        (normal, 'normal'),
        (premium, 'premium'),
        (admin, 'admin')
    )

    email = models.EmailField(verbose_name='mail',max_length=60, unique=True)
    username = models.CharField("nombre de usuario", max_length=50, unique=True)
    
    date_joined = models.DateTimeField(verbose_name='date joined', auto_now_add=True)
    last_login = models.DateField(verbose_name='last login', auto_now=True)
    is_admin = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)
    confirmo= models.BooleanField(default=False)
    plan = models.CharField( max_length=8, choices=AC_CHOICES, default=free)
    date_start_plan = models.DateField(blank=True, null=True, auto_now=False, auto_now_add=False)
    time_pay = models.IntegerField(default=0)
    objects = MyAccountManager()

    USERNAME_FIELD = 'email' #LE ESTOY INDICANDO QUE PARA LOGUEARSE TIENE QUE USAR EL EMAIL
    REQUIRED_FIELDS = ['username'] #ACÁ VAN LOS CAMPOS QUE QUIERO QUE SEAN REQUERIDO, CON COMAS LE AGREGO LOS QUE QUIERA

    def __str__(self): #CADA VEZ QUE HAGA PRINT DE UN OBJETO ACCOUNT LO QUE VOY A MOSTRAR ES LO QUE DEVUELVO EN ESTA FUNCTION POR DEFECTO __srt__
        return self.email # + "," + self.username (puedo concatenar)

    def nombre(self):
        return self.username

    def has_perm (self, perm, obj=None): #ESTO SIGNIFICA QUE SI ES ADMIN VA A PODER HACER CAMBIOS EN LA DB
        return self.is_admin
    
    def has_module_perms(self, app_label):
        return True

    class Meta:
        verbose_name = "Cuenta"
        verbose_name_plural = "Cuentas"




"""
class Tarjeta(models.Model):
    cc_number = CardNumberField(('Número de tarjeta'))
    cc_expiry = CardExpiryField(('Fecha de vencimiento'))
    cc_code = SecurityCodeField(('Código de seguridad'))
 
class Usuario (models.Model):
    nombre= models.CharField(max_length=50, blank=True, null=True)
    apellido= models.CharField(max_length=50, blank=True, null=True)
    password=models.CharField(max_length=20)
    email= models.EmailField(max_length=254)
    username= models.CharField(max_length=50)
    tarjeta=models.OneToOneField(Tarjeta,on_delete=models.CASCADE)
 
    def publish(self):         
        self.save()
    def __str__(self):         
        return self.nombre
    class Meta:
        verbose_name = "Usuario"
        verbose_name_plural = "Usuarios"
"""


#CreditCards
class CreditCards(models.Model):
    number = CardNumberField('numero')
    date_expiration= CardExpiryField('fecha de vencimiento')
    cod = SecurityCodeField('codigo de seguridad')
    card_name = models.CharField("nombre de tarjeta",max_length=50)
    bank = models.CharField(('banco'),max_length=50)
    user = models.OneToOneField(Account, on_delete=models.CASCADE,verbose_name="usuario")

    def publish(self):
        self.save()

    def __str__(self):
        return self.card_name

    class Meta:
        verbose_name = "Tarjeta"
        verbose_name_plural = "Tarjetas"
 




#AUTOR 
class Autor (models.Model):
    nombre= models.CharField(max_length=50, blank=True, null=True)
    apellido= models.CharField(max_length=50, blank=True, null=True)
    #image= models.ImageField("imagen", upload_to='bookflix/static/autores', height_field=None, width_field=None, max_length=None, blank=True, null=True)
    descripcion = models.TextField("descripcion",blank=True, null=True)
    created_date = models.DateTimeField("fecha de creación", default=timezone.now)

    def publish(self):         
        self.save()
    
    def ret(self):
        return self.name

    def __str__(self):         
        return "%s %s" %(self.nombre, self.apellido)
    class Meta:
        verbose_name = "Autor"
        verbose_name_plural = "Autores"


#GÉNERO 
class Genero (models.Model):
    nombre = models.CharField(max_length=50, blank=True, null=True)
    descripcion = models.TextField(("descripcion"),blank=True, null=True)
    created_date = models.DateTimeField(("fecha de creación"), default=timezone.now)

    def __str__(self):         
        return self.nombre

    def publish(self):
        self.published_date = timezone.now()
        self.save()

    class Meta:
        verbose_name = "Género"
        verbose_name_plural = "Géneros"


#EDITORIAL
class Editorial(models.Model):
    nombre= models.CharField("Nombre", max_length=50, primary_key=True)
    descripcion = models.TextField("descripcion",blank=True, null=True)
    email = models.EmailField( max_length=254, blank=True, null=True)
    created_date = models.DateTimeField("",default=timezone.now)

    def publish(self):
        self.published_date = timezone.now()
        self.save()

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Editorial"
        verbose_name_plural = "Editoriales"   


def validateIsbn(value):
    try:
        l= Libro.objects.get(isbn= value)
        raise ValidationError('ISBN en uso por un libro')
    except Libro.DoesNotExist:
        return value

def validateIsbnNum(value):
    if len(value) == 16 and value.isnumeric():
        return value
    else: 
        raise ValidationError('El isbn son 16 numeros')
 

#LIBROS
class Libro (models.Model):
    isbn = models.CharField( max_length=16,primary_key=True, validators =[validateIsbn, validateIsbnNum],default='')
    titulo= models.CharField(('titulo'),max_length=100)
    descripcion = models.TextField(('descripcion'), blank=True, null=True)
    portada= models.ImageField(('portada'), upload_to='portadas_libros', height_field=None, width_field=None, max_length=None, )
    autor= models.ForeignKey(Autor,on_delete=models.CASCADE, verbose_name="autor")
    genero = models.ManyToManyField(Genero, verbose_name="generos")
    editorial = models.ForeignKey(Editorial, on_delete=models.CASCADE)
    mostrar_en_home= models.BooleanField(default=False)
    on_normal = models.BooleanField("ver en normal", default=False)
    on_premium = models.BooleanField("ver en premium",default=False)
    pdf = models.FileField(upload_to='pdf', blank=True, null=True)   #por si en un futuro hacemos que se guarde en la base de datos

    def publish(self):         
        self.save()

    def __str__(self):         
        return self.titulo
    class Meta:
        verbose_name = "Libro"
        verbose_name_plural = "Libros"


#Profile

class Profile(models.Model):
    name= models.CharField("nombre", max_length=50)
    account= models.ForeignKey(Account, on_delete=models.CASCADE, verbose_name="cuenta")
    is_active_now= models.BooleanField("esta activo ahora",default=False)
    hour_activation= models.DateTimeField("hora de activacion", auto_now=False, auto_now_add=False, blank=True, null=True)
    pleasures_gender = models.ManyToManyField(Genero, blank=True, null=True, verbose_name="genero")
    pleasures_author = models.ManyToManyField(Autor, blank=True, null=True, verbose_name="autor")
    pleasures_editorial = models.ManyToManyField(Editorial,blank=True, null=True, verbose_name="editorial")
    
    date_of_creation = models.DateTimeField("fecha de creacion",default=timezone.now)
    
    def publish(self):
        self.save()

    def __str__(self):
        return self.name  
    
    class Meta:
        verbose_name = "Perfil"
        verbose_name_plural = "Perfiles"
        unique_together= ('name', 'account')

