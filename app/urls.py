from django.urls import path
from .views import *

urlpatterns = [
    path('', index, name='index'),
    path('cuenta/crear', crear_cuenta, name='crear_cuenta'),
    path('cuenta/login', iniciar_sesion, name='iniciar_sesion'),
    path('cuenta/logout', cerrar_sesion, name='cerrar_sesion'),
    #Jugadores
    path('jugadores', jugadores, name='jugadores'),
    path('jugador/nuevo', nuevo_jugador, name='nuevo_jugador'),
    path('jugador/<int:id>/editar', editar_jugador, name='editar_jugador'),

]