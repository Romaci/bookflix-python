
import os
 
dirname = os.path.dirname(__file__)
 
 
# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
 
 
# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/3.0/howto/deployment/checklist/
 
# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'q^!*1li2c_=2%7up%5bocpnwsu-#ddu^@oup3w=1=5z#+hik6x'
 
# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True
 
ALLOWED_HOSTS = ['127.0.0.1'] #me permite hostear mi pag en el servidor local LO AGREGUÉ YOOOO
 
 
# Application definition
 
INSTALLED_APPS = [
 
    #DJANGO APPS, vienen por defecto
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
 
    #MIS APPS
    
    'appBookflix', #agrego la carpeta en la que voy a trabajar. ESTA LA AGREGUÉ YO. 
    
]
 
MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]
 
ROOT_URLCONF = 'bookflix.urls'
 
TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],#os.path.join(BASE_DIR, 'templates')],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]
 
 
 #AGREGO POR EL ACCOUNT QUE CREE EN MODELS
AUTH_USER_MODEL='appBookflix.Account'
 
WSGI_APPLICATION = 'bookflix.wsgi.application'
 
 
# Database
# https://docs.djangoproject.com/en/3.0/ref/settings/#databases
 
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
    }
}
 
 
# Password validation
# https://docs.djangoproject.com/en/3.0/ref/settings/#auth-password-validators
 
AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]
 
 
# Internationalization
# https://docs.djangoproject.com/en/3.0/topics/i18n/
 
LANGUAGE_CODE = 'es-es'
 
TIME_ZONE = 'UTC' #podría poner la de argentina
 
USE_I18N = True
 
USE_L10N = True
 
USE_TZ = True
 
 
# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/3.0/howto/static-files/
 
 
STATIC_URL = '/static/'
 
MEDIA_URL = '/media/' 
 
STATIC_ROOT = os.path.join(BASE_DIR, 'static_cdn') 
MEDIA_ROOT = os.path.join(BASE_DIR, 'media_cdn')  
STATICFILES_DIRS = [     
    os.path.join(BASE_DIR, 'static'),    #LO AGREGUÉ YO. SON CONSTANTES PARA QUE FUNCIONEN LAS IMAGENES Y SARASA
    os.path.join(BASE_DIR, 'media'), ] #LO AGREGUÉ YO. SON CONSTANTES PARA QUE FUNCIONEN LAS IMAGENES Y SARASA
























