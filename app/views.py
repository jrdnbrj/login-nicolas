from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .forms import *
from .models import *

# Create your views here.
def index(request):
    users = User.objects.all()
    return render(request, 'index.html', { 'users': users })

def crear_cuenta(request):
    if request.method == 'POST':
        user = UserForm(request.POST)
        if user.is_valid():
            print('valid')
            user = User.objects.create_user(request.POST['username'], request.POST['email'], request.POST['password'])
            if user is None:
                print('User is None')
            redirect('iniciar_sesion')
        else:
            print('not valid')
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
    return render(request, 'jugador/jugadores.html', { 'jugadores': jugadores })

@login_required
def nuevo_jugador(request):
    context = {}
    if request.method == 'POST' and request.user.is_superuser:
        jugador = JugadorForm(request.POST)
        if jugador.is_valid():
            jugador.save()
        else:
            print(jugador.errors)
        return redirect('jugadores')
    return render(request, 'jugador/crear_editar_jugador.html', {})

@login_required
def editar_jugador(request, id):
    context = {}
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
