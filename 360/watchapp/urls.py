from django.urls import path
from .views import login_view, register_view, homepage_view, settings_view, logout_view
from .views import search_friends, add_friend

urlpatterns = [
    path('login/', login_view, name='login'),
    path('register/', register_view, name='register'),
    path('', homepage_view, name='homepage'), 
    path('settings/', settings_view, name='settings'),
    path('logout/', logout_view, name='logout'),
    path('search/', search_friends, name='search_friends'),
    path('add-friend/<str:username>/', add_friend, name='add_friend'),
]
