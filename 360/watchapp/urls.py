from django.urls import path
from . import views

urlpatterns = [
    path('login/', views.login_view, name='login'),
    path('register/', views.register_view, name='register'),
    path('', views.homepage_view, name='homepage'),  # Ensure only one homepage route
    path('settings/', views.settings_view, name='settings'),
    path('logout/', views.logout_view, name='logout'),
    path('search_video/', views.search_video, name='search_video'),
    path('delete_video/<int:video_id>/', views.delete_video, name='delete_video'),  # Add this line for deleting videos
]
