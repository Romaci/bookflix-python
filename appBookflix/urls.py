from django.urls import path, include 
from .views import *
from django.conf.urls.static import static 
from django.conf import settings 
from django.contrib import admin 
from django.conf.urls import url

urlpatterns = [path('', welcome, name='welcome'),
path('login/', login, name='login'),
]   + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)