from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.forms import User
from django.contrib.auth.views import LoginView
from django.forms import ModelForm

from .models import *


class UserSignUp(UserCreationForm):
    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'username', 'email', 'password1', 'password2']


class UserLogin(LoginView):
    class Meta:
        fields = ['username', 'password']


class LikeForm(forms.ModelForm):
    class Meta:
        model = Discuzz
        fields = '__all__'
