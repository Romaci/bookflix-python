from django.db import models

# Create your models here.

class Usuario (models.Model):
    nombre= models.CharField(max_length=50, blank=True, null=True)
    apellido= models.CharField(max_length=50, blank=True, null=True)
    def publish(self):         
        self.save()
    def __str__(self):         
        return self.nombre

class Autor (models.Model):
    nombre= models.CharField(max_length=50, blank=True, null=True)
    apellido= models.CharField(max_length=50, blank=True, null=True)
    def publish(self):         
        self.save()
    def __str__(self):         
        return "%s %s" %(self.nombre, self.apellido)

class Libro (models.Model):
    titulo= models.CharField(max_length=100, blank=True, null=True)
    autor= models.ForeignKey(Autor,on_delete=models.CASCADE, blank=True, null=True)
    portada=models.ImageField(upload_to='portadas_libros', height_field=None, width_field=None, max_length=None, blank=True, null=True)
    def publish(self):         
        self.save()
    def __str__(self):         
        return self.titulo