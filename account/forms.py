from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.forms import User
from django.contrib.auth.views import LoginView

from .models import UserExtension


class UserSignUp(UserCreationForm):
    password1 = forms.CharField(widget=forms.PasswordInput(attrs={'minlength': 9}))
    password2 = forms.CharField(widget=forms.PasswordInput(attrs={'minlength': 9}))

    first_name = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control'}))
    last_name = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control'}))
    username = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control'}))
    email = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control'}))

    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'username', 'email', 'password1', 'password2']


class UserLogin(LoginView):
    class Meta:
        fields = ['username', 'password']


class PicForm(forms.ModelForm):
    style_sheet = forms.Select()
    mode_sheet = forms.RadioSelect()
    location = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control'}), label='Location')
    phone_number = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control'}), label='Location:')
    bio = forms.CharField(widget=forms.Textarea(attrs={'class': 'form-control'}))
    hobbies = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control'}))
    gender = forms.Select()
    programming_languages = forms.CheckboxSelectMultiple()

    class Meta:
        model = UserExtension
        fields = ['style_sheet',
                  'mode_sheet',
                  'location',
                  'phone_number',
                  'bio',
                  'hobbies',
                  'gender',
                  'programming_languages',
                  ]
        print(fields)