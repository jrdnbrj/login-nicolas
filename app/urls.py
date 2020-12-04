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
    path('jugador/<int:id>/eliminar', eliminar_jugador, name='eliminar_jugador'),
    path('jugador/<int:id>/comprar', comprar_jugador, name='comprar_jugador'),
    path('jugador/<int:id>/vender', vender_jugador, name='vender_jugador'),
    #Clubes
    path('clubes', clubes, name='clubes'),
    path('club/nuevo', nuevo_club, name='nuevo_club'),
    path('club/editar', editar_club, name='editar_club'),
    #Reporte
    path('reporte', reporte, name='reporte'),
    path('clubes/buscar', buscar_clubes, name='buscar_clubes'),
    path('jugadores/buscar/<orden>', buscar_jugadores, name='buscar_jugadores'),
]