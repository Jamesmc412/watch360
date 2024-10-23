from django.urls import path
from . import views

from django.urls import path
from . import views

urlpatterns = [
    path('login/', views.login_view, name='login'),
    path('register/', views.register_view, name='register'),
    path('', views.home_view, name='homepage'),  # Matches 'homepage'
    path('settings/', views.settings_view, name='settings'),
    path('logout/', views.logout_view, name='logout'),
    path('search_video/', views.search_video, name='search_video'),
    path('delete_video/<int:video_id>/', views.delete_video, name='delete_video'),  # Add this line for deleting videos
]

