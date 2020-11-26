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
    if request.method == 'POST' and request.user.is_superuser:
        jugador = JugadorForm(request.POST)
        if jugador.is_valid():
            jugador.save()
        else:
            print(jugador.errors)
        return redirect('jugadores')
    return render(request, 'jugador/crear_editar_jugador.html')

@login_required
def editar_jugador(request, id):
    jugador = Jugador.objects.get(id=id)
    print(jugador)
    if request.method == 'POST' and request.user.is_superuser:
        jugador = JugadorForm(request.POST, instance=jugador)
        if jugador.is_valid():
            jugador.save()
        else:
            print(jugador.errors)
        return redirect('jugadores')
    return render(request, 'jugador/crear_editar_jugador.html', { 'jugador': jugador, 'action': 'Editar' })

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
    jugador.club = club
    jugador.save()

    club.dinero_invertido = club.dinero_invertido + jugador.costo
    club.save()
    return redirect('jugadores')

@login_required
def vender_jugador(request, id):
    club = Club.objects.get(usuario=request.user)
    jugador = Jugador.objects.get(id=id)
    jugador.club = None
    jugador.save()

    club.dinero_ganado = club.dinero_ganado + jugador.costo
    club.save()
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
