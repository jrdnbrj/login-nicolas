from django.db import models

# Create your models here.

class Jugador(models.Model):
    id = models.AutoField(primary_key=True)
    nombre = models.CharField(max_length=50)
    edad = models.IntegerField()
    costo = models.DecimalField(decimal_places = 2, max_digits = 10)

    def __str__(self):
        return self.nombre

class Club(models.Model):
    id = models.AutoField(primary_key=True)
    nombre = models.CharField(max_length=50)
    jugadores = models.ManyToManyField(Jugador, blank=True, related_name='jugadores')

    def __str__(self):
        return self.nombre