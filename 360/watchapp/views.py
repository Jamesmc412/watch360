from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from .forms import LoginForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib.auth.hashers import make_password
from django.contrib import messages
from django.contrib.auth import update_session_auth_hash
from django.http import JsonResponse #search 
from .models import User  # Adjust this to your actual model #search
from .models import Friendship

def login_view(request):
    error = None
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect('homepage')  # Redirect to the home page or dashboard
            else:
                error = "Invalid credentials"
    else:
        form = LoginForm()
    
    return render(request, 'watchapp/login.html', {'form': form, 'error': error})

def register_view(request):
    error = None

    if request.method == 'POST':
        fullname = request.POST['name']
        username = request.POST['username']
        password = request.POST['password']
        confirm_password = request.POST['confirm_password']

        if User.objects.filter(username=username).exists():
            error = "The username is already taken!"
        elif len(password) < 6:
            error = "Password must have at least 6 characters."
        elif password != confirm_password:
            error = "Passwords do not match."
        else:
            # Create a new user
            user = User.objects.create(
                username=username,
                password=make_password(password),
                first_name=fullname
            )
            messages.success(request, 'Registration successful! Redirecting to login...')
            return redirect('login')

    return render(request, 'watchapp/register.html', {'error': error})

def homepage_view(request):
    # Sample data to mimic friend list
    friends = [
        {"name": "Friend 1", "status": "Online", "watching": "?"},
        {"name": "Friend 2", "status": "Offline", "watching": "?"},
        {"name": "Friend 3", "status": "Online", "watching": "?"}
    ]
    return render(request, 'watchapp/homepage.html', {"friends": friends})

def logout_view(request):
    # Clear the session data
    request.session.flush()
    # Redirect to the login page
    return redirect('login')

@login_required
def settings_view(request):
    user = request.user  # Get the logged-in user

    if request.method == 'POST':
        new_username = request.POST.get('changeUsername')
        new_password = request.POST.get('changePassword')

        # Update username if provided
        if new_username:
            user.username = new_username

        # Update password if provided
        if new_password:
            user.set_password(new_password)
            update_session_auth_hash(request, user)  # Keep user logged in after password change

        user.save()
        messages.success(request, 'Settings updated successfully!')
        return redirect('login')

    return render(request, 'watchapp/settings.html', {'user': user})

def search_friends(request):
    if 'query' in request.GET:
        query = request.GET['query']
        users = User.objects.filter(name__icontains=query)  # Searching by name
        results = [{'name': user.name, 'username': user.username} for user in users]
        return JsonResponse(results, safe=False)
    return JsonResponse([], safe=False)

@login_required
def add_friend(request, username):
    if request.method == 'POST':
        try:
            friend = User.objects.get(username=username)
            friendship, created = Friendship.objects.get_or_create(user=request.user, friend=friend)
            if created:
                return JsonResponse({'status': 'Friend request sent.'})
            else:
                return JsonResponse({'status': 'Friend request already sent.'})
        except User.DoesNotExist:
            return JsonResponse({'status': 'User does not exist.'}, status=404)

    return JsonResponse({'status': 'Invalid request.'}, status=400)