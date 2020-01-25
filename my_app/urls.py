from django.conf.urls import url
from django.contrib import admin
from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('new_Search', views.new_search, name='new_Search'),
    url(r'add_todo/', views.add_todo, name='add_todo'),
    path('delete_todo/<int:todo_id>/', views.delete_todo),
    # path('admin/', admin.site.urls),
]