from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.forms import User
from django.contrib.auth.views import LoginView

from my_app.models import UserExtension


class UserSignUp(UserCreationForm):
    password1 = forms.CharField(widget=forms.PasswordInput(attrs={'minlength': 9}))
    password2 = forms.CharField(widget=forms.PasswordInput(attrs={'minlength': 9}))

    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'username', 'email', 'password1', 'password2']
        print(fields)


class UserLogin(LoginView):
    class Meta:
        fields = ['username', 'password']


class PicForm(forms.ModelForm):
    class Meta:
        model = UserExtension
        fields = ['style_sheet',
                  'mode_sheet',
                  'profile_pic',
                  'location',
                  'phone_number',
                  'bio',
                  'hobbies',
                  'gender',
                  'programming_languages',
                  ]
