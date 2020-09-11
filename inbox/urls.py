from django.urls import path
from . import views

urlpatterns = [
    path('chat/', views.base_chat, name='chat'),
    path('chat/<str:username>/', views.chat),
    path('chat/delete_message/<str:id_>/', views.delete_chat_message),
    path('chat/animation/me', views.animation),
    path('emojiss/type=<str:cat>/order_by=<str:by>/', views.me_unicodes),
]
