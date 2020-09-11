from django.urls import path
from . import views

from django.contrib.auth import views as auth_views

urlpatterns = [

    path('', views.home, name='base'),

    path('home/', views.home, name='home'),

    path('signup/', views.signup, name='signup'),
    path('login/', views.user_login, name='login'),
    path('logout/', views.logout_user, name='logout'),

    path('profile/', views.profile, name='profile'),
    path('accounts/profile/', views.profile),
    path('profile/notifications/', views.notifications, name='notifications'),
    path('profile/get/notifications/', views.get_notifications),
    path('update/profilepic/', views.profile_pic_update, name='update/profilepic'),
    path('update/details', views.profile, name='update/details'),

    path('api/messageUs/', views.api_message_us),
    path('api/create/topic/', views.api_home_topic_form),

    path('notification/delete/<str:note_ID>/', views.delete_notification),

    path('account/friends/', views.add_friends, name='friends'),

    path('api/send_friend_request/<str:username>/', views.api_add_friend_request),
    path('api/add/<str:username>/<str:notification_ID>/', views.api_add_remove_friend),
    path('api/remove/<str:username>/<str:notification_ID>/', views.api_add_remove_friend),

]

urlpatterns += [
    path('api/users/', views.Api_All_Users.as_view()),
    path('api/users/<str:user_name>/', views.Api_User_Details.as_view()),
]

urlpatterns += [
    path('password-reset/',
         auth_views.PasswordResetView.as_view(template_name='account/password/password_reset.html'),
         name='password_reset'),
    path('password-reset/done/',
         auth_views.PasswordResetDoneView.as_view(template_name='account/password/password_reset_done.html'),
         name='password_reset_done'),
    path('password-reset-confirm/<uidb64>/<token>/',
         auth_views.PasswordResetConfirmView.as_view(template_name='account/password/password_reset_confirm.html'),
         name='password_reset_confirm'),
    path('password-reset-complete/',
         auth_views.PasswordResetCompleteView.as_view(template_name='account/password/password_reset_complete.html'),
         name='password_reset_complete'),
]
