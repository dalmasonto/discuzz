from django.urls import path
from . import views

urlpatterns = [

    path('', views.home, name='base'),

    path('home/', views.home, name='home'),

    path('api/users/', views.Api_All_Users.as_view()),
    path('api/users/<str:username>/', views.get_user),

    path('signup/', views.signup, name='signup'),
    path('login/', views.user_login, name='login'),
    path('logout/', views.logout_user, name='logout'),

    path('profile/', views.profile, name='profile'),
    path('profile/notifications/', views.notifications, name='notifications'),
    path('profile/get/notifications/', views.get_notifications),
    path('update/profilepic/', views.profile_pic_update, name='update/profilepic'),
    path('update/details', views.profile, name='update/details'),

    path('api/messageUs/', views.api_message_us),
    path('api/create/topic/', views.api_home_topic_form),

    path('notification/<str:note_ID>/', views.delete_notification),

    path('account/friends/', views.add_friends, name='friends'),

    path('api/send_friend_request/<str:username>/', views.api_add_friend_request),
    path('api/<str:option>/<str:username>/', views.api_add_remove_friend),


]
