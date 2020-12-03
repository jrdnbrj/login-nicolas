from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class Club(models.Model):
    id = models.AutoField(primary_key=True)
    nombre = models.CharField(max_length=50, unique=True)
    email = models.EmailField(max_length=50, unique=True, default='')
    pais = models.CharField(max_length=30, default='')
    telefono = models.CharField(max_length=25, null=True, blank=True, default='')
    usuario = models.ForeignKey(User, null=True, blank=True, on_delete=models.SET_NULL, related_name='usuario')

    def __str__(self):
        return self.nombre
        
class Jugador(models.Model):
    id = models.AutoField(primary_key=True)
    nombre = models.CharField(max_length=50)
    edad = models.IntegerField()
    costo = models.DecimalField(decimal_places = 2, max_digits = 15)
    club = models.ForeignKey(Club, null=True, blank=True, on_delete=models.SET_NULL, related_name='club')

    def __str__(self):
        return self.nombre

class Transaccion(models.Model):
    id = models.AutoField(primary_key=True)
    club_origen = models.ForeignKey(Club, null=True, blank=True, on_delete=models.SET_NULL, related_name='club_origen')
    club_destino = models.ForeignKey(Club, null=True, blank=True, on_delete=models.SET_NULL, related_name='club_destino')
    jugador = models.ForeignKey(Jugador, null=True, blank=True, on_delete=models.SET_NULL, related_name='jugador')
    fecha = models.DateTimeField(auto_now_add=True, editable=True)
    costo = models.DecimalField(decimal_places = 2, max_digits = 15)

    def __str__(self):
        return self.jugador.nombre