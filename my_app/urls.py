from django.conf.urls import url
from django.contrib import admin
from django.urls import path
from . import views

urlpatterns = [
    # all paths with api as the suffix signify use oi
    path('', views.home, name='base'),
    path('home/', views.home, name='home'),
    path('api/messageUs/', views.api_message_us, name='api/messageUs'),
    path('api/create/topic/homepage/', views.api_home_topic_form, name='api/create/topic/homepage/'),

    path('signup/', views.signup, name='signup'),
    path('login/', views.user_login, name='login'),
    path('logout/', views.logout_user, name='logout'),

    path('profile/', views.profile, name='profile'),
    path('create/', views.create, name='create'),
    path('api/createTopic/', views.api_create_topic, name='api/createTopic'),
    path('api/create/topics_subtopics', views.api_topic_subtopic_render, name='api/create'),
    path('join/', views.join, name='join'),

    path('c19/', views.c19, name='c19'),
    path('wnews/', views.wnews, name='wnews'),
    path('about/', views.about, name='about'),
    path('contact/', views.contact, name='contact'),

    # Normal discuzz form for sending the form to the backend during a discussion
    path('discuzz/<str:discussion_details>/', views.discuzz, name='discuzz'),
    # Another path for ajax/api based form
    path('discuzz_api/<str:discussion_details>', views.reply_api),

    path('api/discuzz/<str:discussion_details>/', views.api_discuzz_details, name='api_discuzz'),
    path('api/all_discussions/', views.api_all_queries, name='api_objects_all'),

    path('like/', views.like, name='like'),
    path('dislike/', views.dislike, name='dislike'),
    path('comment/', views.comments, name='comment'),

    path('prog/', views.progpage, name='prog'),
    # path('join/discuzz/<str:discussion_details>/', views.discuzz, name='discuzz2'),
]
