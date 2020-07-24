from django.conf.urls import url
from django.contrib import admin
from django.urls import path
from . import views

urlpatterns = [

    path('myadmin/', views.my_admin, name='myadmin'),

    # path('api/create/topic/', views.api_home_topic_form, name='api/create/topic/homepage/'),

    path('read_reply_email_message/<int:_id>/', views.read_reply_email_message),
    path('delete_reply_topic_comment_question/<int:_id>/', views.delete_reply_comment_topic_question),
    path('hide_show_reply_comment/<int:_id>/', views.hide_show_reply_comment_topic_question),

    path('create/', views.create, name='create'),
    path('api/createTopic/', views.api_create_quiz, name='api/createTopic'),
    path('api/create/topics_subtopics/', views.api_topic_subtopic_render, name='api/create'),
    path('Join/', views.join, name='join'),

    path('comments/<str:reply_id>/', views.comments_api),

    path('c19/', views.c19, name='c19'),
    path('wnews/', views.wnews, name='wnews'),
    path('about/', views.about, name='about'),
    path('contact/', views.contact, name='contact'),

    path('trial', views.trial_loader, name='trial'),

    path('discuzz/<str:discussion_details>/', views.discuzz, name='discuzz'),

    path('discuzz_api/<str:discussion_details>/', views.reply_api),

    path('api/discuzz/<str:discussion_details>/', views.api_discuzz_details, name='api_discuzz'),
    path('api/all_discussions/', views.api_all_queries, name='api_objects_all'),
    path('api/all_numbers/', views.api_my_admin, name='api_all_numbers'),
    path('api/participants/<str:discussion_code>/', views.participants),

    path('like/', views.like, name='like'),
    path('dislike/', views.dislike, name='dislike'),
    path('comment/', views.all_comments_api, name='comment'),

    path('api/like/<int:reply_id>/', views.api_like),
    path('api/dislike/<int:reply_id>/', views.api_dislike),
    path('emails/', views.email, name='emails'),

    path('prog/', views.progpage, name='prog'),

    path('api/user-details/<str:username>/', views.get_user_info)

]

urlpatterns += [
    path('api/replies/', views.reply_api),
    path('api/questions/', views.quiz_api),
]
