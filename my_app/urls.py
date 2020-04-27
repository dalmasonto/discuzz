from django.conf.urls import url
from django.contrib import admin
from django.urls import path
from . import views


urlpatterns = [
    path('', views.home, name='base'),
    path('home/', views.home, name='home'),
    path('signup/', views.signup, name='signup'),
    path('login/', views.user_login, name='login'),
    path('logout/', views.logout_user, name='logout'),
    path('profile/', views.profile, name='profile'),
    path('create/', views.create, name='create'),
    path('join/', views.join, name='join'),
    path('c19/', views.c19, name='c19'),
    path('wnews/', views.wnews, name='wnews'),
    path('about/', views.about, name='about'),
    path('contact/', views.contact, name='contact'),
    path('discuzz/<str:discussion_details>/', views.discuzz, name='discuzz'),
    # path('join/discuzz/<str:discussion_details>/', views.discuzz, name='discuzz2'),
]
