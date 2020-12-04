from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .forms import *
from .models import *


# Create your views here.
def index(request):
    users = User.objects.all()
    clubes = Club.objects.all()
    return render(request, 'index.html', { 'users': users, 'clubes': clubes })

def crear_cuenta(request):
    if request.method == 'POST':
        user = UserForm(request.POST)
        if user.is_valid():
            user = User.objects.create_user(request.POST['username'], request.POST['email'], request.POST['password'])
            if user is None:
                print('User is None')
                redirect('iniciar_sesion')
            return redirect('iniciar_sesion')
        else:
            print(user.errors)
    return render(request, 'login/crear_cuenta.html')

def iniciar_sesion(request):
    context = {}
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username = username, password = password)
        if user is not None:
            login(request, user)
            return redirect('index')
        else:
            print('Credenciales incorrectas')
            context['msg'] = 'El usuario o la contraseña es incorrecta, por favor vuelva a intentar.'
            context['username'] = username

    return render(request, 'login/iniciar_sesion.html', context)

@login_required
def cerrar_sesion(request):
    logout(request)
    return redirect('index')

# JUGADOR

@login_required
def jugadores(request):
    jugadores = Jugador.objects.all()
    try:
        club = Club.objects.get(usuario=request.user)
    except Club.DoesNotExist:
        club = None
    return render(request, 'jugador/jugadores.html', { 'jugadores': jugadores, 'club': club })

@login_required
def nuevo_jugador(request):
    context = {}
    if request.method == 'POST' and request.user.is_superuser:
        jugador = JugadorForm(request.POST)
        if jugador.is_valid():
            jugador.save()
            return redirect('jugadores')
        else:
            print(jugador.errors)
            context['form'] = jugador
    return render(request, 'jugador/crear_editar_jugador.html', context)

@login_required
def editar_jugador(request, id):
    jugador = Jugador.objects.get(id=id)
    context = { 'jugador': jugador, 'action': 'Editar' }
    if request.method == 'POST' and request.user.is_superuser:
        jugador = JugadorForm(request.POST, instance=jugador)
        if jugador.is_valid():
            jugador.save()
            return redirect('jugadores')
        else:
            print(jugador.errors)
            context['form'] = jugador
    return render(request, 'jugador/crear_editar_jugador.html', context)

@login_required
def eliminar_jugador(request, id):
    if  request.user.is_superuser:
        jugador = Jugador.objects.get(id=id)
        jugador.delete()
    return redirect('jugadores')

@login_required
def comprar_jugador(request, id):
    club = Club.objects.get(usuario=request.user)
    jugador = Jugador.objects.get(id=id)
    transaccion = iniciar_transaccion(jugador.club, club, jugador)
    return redirect('jugadores')

@login_required
def vender_jugador(request, id):
    jugador = Jugador.objects.get(id=id)
    transaccion = iniciar_transaccion(jugador.club, None, jugador)
    return redirect('jugadores')

# CLUB

def clubes(request):
    clubes = Club.objects.all()
    jugadores = Jugador.objects.all()
    return render(request, 'club/clubes.html', { 'clubes': clubes, 'jugadores': jugadores })

@login_required
def nuevo_club(request):
    context = {}
    if request.method == 'POST':
        club = ClubForm(request.POST)
        if club.is_valid():
            club = club.save(commit=False)
            club.usuario = request.user
            club.save()
            usuario = request.user
            usuario.is_superuser = True
            usuario.save()
            return redirect('jugadores')
        else:
            print(club.errors)
            context['form'] = club
    return render(request, 'club/crear_editar_club.html', context)

@login_required
def editar_club(request):
    club = Club.objects.get(usuario=request.user)
    jugadores = Jugador.objects.filter(club=club.id)
    print('Jugadores:', jugadores)
    context = { 
        'action': 'Editar',
        'club': club, 
        'jugadores': jugadores
    }
    if request.method == 'POST':
        club = ClubForm(request.POST, instance=club)
        if club.is_valid():
            club.save()
            return redirect('editar_club')
        else:
            print(club.errors)
            context['form'] = club
    return render(request, 'club/crear_editar_club.html', context)

# Transaccion

def iniciar_transaccion(club_origen, club_destino, jugador):
    transaccion = Transaccion(
        club_origen=club_origen,
        club_destino=club_destino,
        jugador=jugador,
        costo=jugador.costo
    )
    transaccion.save()

    jugador.club = club_destino
    jugador.save()

    return transaccion

# Reporte

def reporte(request):
    clubes = Club.objects.all()
    transacciones = Transaccion.objects.all()
    context = {}
    if request.method == 'POST':
        club = request.POST['club']
        date_from = request.POST['date_from']
        date_to = request.POST['date_to']
        print(club, date_from, date_to)

        club = Club.objects.get(nombre=request.POST['club'])

        if request.POST['date_from']:
            transacciones = transacciones.exclude(fecha__lt=request.POST['date_from'])
        if request.POST['date_to']:
            transacciones = transacciones.exclude(fecha__gt=request.POST['date_to'])
        invertido = transacciones.filter(club_origen=club)
        ganado = transacciones.filter(club_destino=club)

        invertido = [transaccion.costo for transaccion in invertido]
        ganado = [transaccion.costo for transaccion in ganado]
    
        context = {
            'clubes': clubes,
            'club': club,
            'invertido': sum(invertido),
            'ganado': sum(ganado),
            'ganancia': sum(ganado) - sum(invertido)
        }
    context['clubes'] = clubes
    return render(request, 'reporte.html', context)

def buscar_clubes(request):
    return render(request, 'reporte.html', { 'clubes': Club.objects.all()})

def buscar_jugadores(request, orden):
    jugadores = Jugador.objects.all()
    if orden == 'ascendente':
        jugadores = jugadores.order_by('costo')
        context = { 'jugadores': jugadores, 'orden': 'descendente' }
    elif orden == 'descendente':
        jugadores = jugadores.order_by('-costo')
        context = { 'jugadores': jugadores, 'orden': 'ascendente' }
    else:
        context = { 'jugadores': jugadores, 'orden': 'ascendente' }
    return render(request, 'reporte2.html', context)