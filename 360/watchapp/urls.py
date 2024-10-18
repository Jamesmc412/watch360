from django.urls import path
from .views import login_view, register_view, homepage_view, settings_view, logout_view

urlpatterns = [
    path('login/', login_view, name='login'),
    path('register/', register_view, name='register'),
    path('', homepage_view, name='homepage'), 
    path('settings/', settings_view, name='settings'),
    path('logout/', logout_view, name='logout'),
]
