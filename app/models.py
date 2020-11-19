from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class Club(models.Model):
    id = models.AutoField(primary_key=True)
    nombre = models.CharField(max_length=50)
    usuario = models.ForeignKey(User, null=True, blank=True, on_delete=models.SET_NULL, related_name='usuario')

    def __str__(self):
        return self.nombre
        
class Jugador(models.Model):
    id = models.AutoField(primary_key=True)
    nombre = models.CharField(max_length=50)
    edad = models.IntegerField()
    costo = models.DecimalField(decimal_places = 2, max_digits = 10)
    club = models.ForeignKey(Club, null=True, blank=True, on_delete=models.SET_NULL, related_name='club')

    def __str__(self):
        return self.nombre
