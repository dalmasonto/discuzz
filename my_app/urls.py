from django.conf.urls import url
from django.contrib import admin
from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('new_Search', views.new_search, name='new_Search'),
    path('about_page', views.about_page, name='about_page'),
    path('signup_page', views.signup_page, name='signup_page'),
    path('todos_page', views.todos_page, name='todos_page'),
    path('contacts_page', views.contacts_page, name='contacts_page'),
    path('add_todo_page', views.add_todo_page, name='add_todo_page'),
    path('form_sign_up/', views.form_sign_up, name='add_todo'),
    path('add_todo/', views.add_todo, name='add_todo'),
    path('delete_todo/<int:todo_id>/', views.delete_todo),
    path('delete_contact/<int:contact_id>/', views.delete_contact),
    # path('admin/', admin.site.urls),
]