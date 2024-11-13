from django.urls import path
from .views import MyProfile
from . import views

#All the different urls that are needed.
urlpatterns = [
    path('login/', views.login_view, name='login'),
    path('register/', views.register_view, name='register'),
    path('', views.homepage_view, name='homepage'), 
    path('logout/', views.logout_view, name='logout'),
    path('search_video/', views.search_video, name='search_video'),
    path('delete/<int:video_id>/', views.delete_video, name='delete_video'),
    path('check-videos-status/', views.check_videos_status, name='check_videos_status'),
    path('chat/', views.chat_view, name='chat'),
    path('search/', views.search_users, name='search_users'),  
    path('send-request/<int:user_id>/', views.send_friend_request, name='send_friend_request'),
    path('accept-request/<int:request_id>/', views.accept_friend_request, name='accept_friend_request'),
    path('reject-request/<int:request_id>/', views.reject_friend_request, name='reject_friend_request'),
    path('unfriend/<int:user_id>/', views.unfriend, name='unfriend'),
    path('profile/', MyProfile.as_view(), name='profile'),
    path('api/friends-online-status/', views.friends_online_status, name='friends_online_status'), # to fetch the online status of friends for friends cards (james)
    path('api/update-online-status/', views.update_online_status, name='update_online_status'), # to update the online status of the user (james)
]

