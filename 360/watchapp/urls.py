from django.urls import path
from .views import login_view, register_view, homepage_view, settings_view, logout_view, chat_view
from . import views

urlpatterns = [
    path('login/', login_view, name='login'),
    path('register/', register_view, name='register'),
    path('', homepage_view, name='homepage'), 
    path('settings/', settings_view, name='settings'),
    path('logout/', logout_view, name='logout'),
    path('chat/', chat_view, name='chat'),
    path('search/', views.search_users, name='search_users'),    # search task-rj
    #testing django-friendship
    path('users/', views.user_list, name='user_list'),
    path('send-request/<int:user_id>/', views.send_friend_request, name='send_friend_request'),
    path('accept-request/<int:request_id>/', views.accept_friend_request, name='accept_friend_request'),
    path('reject-request/<int:request_id>/', views.reject_friend_request, name='reject_friend_request'),
    path('unfriend/<int:user_id>/', views.unfriend, name='unfriend'),
]
