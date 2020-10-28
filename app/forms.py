from django import forms
from django.contrib.auth.models import User
from .models import *

class UserForm(forms.ModelForm):

    class Meta:
        model = User
        fields = ('username', 'email', 'password')

class JugadorForm(forms.ModelForm):

    class Meta:
        model = Jugador
        fields = '__all__'