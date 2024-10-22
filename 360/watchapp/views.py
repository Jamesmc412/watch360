from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from .forms import LoginForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib.auth.hashers import make_password
from django.contrib import messages
from django.contrib.auth import update_session_auth_hash
from bs4 import BeautifulSoup
from django.http import JsonResponse
import requests
import json
from .models import YouTubeData
from django.views.decorators.csrf import csrf_exempt



def get_video_title(video_url):
    """Fetch the video title from YouTube API."""
    try:
        # Extract the video ID from the URL
        video_id = video_url.split('v=')[1].split('&')[0] if 'v=' in video_url else None
        if not video_id:
            return "Invalid YouTube URL"

        # Define your YouTube Data API key and endpoint
        api_key = 'AIzaSyB0ck1zWAO-20vOaNRdgYu7-yTNCS0jtZE'  # Replace with your API key
        endpoint = f'https://www.googleapis.com/youtube/v3/videos?part=snippet&id={video_id}&key={api_key}'

        # Make the request to the YouTube Data API
        response = requests.get(endpoint)
        response.raise_for_status()

        # Parse the response and extract the video title
        data = response.json()
        if data['items']:
            return data['items'][0]['snippet']['title']
        return "Video not found"

    except Exception as e:
        print(f"Error fetching video title: {e}")
        return "Could not retrieve title"

@login_required
def search_video(request):
    if request.method == "POST":
        try:
            # Parse the JSON request body
            data = json.loads(request.body)
            video_url = data.get("youtube_url")

            if not video_url:
                return JsonResponse({'error': 'YouTube URL is required'}, status=400)

            # Get the video title using the function above
            video_title = get_video_title(video_url)

            # Save the video for the currently logged-in user
            YouTubeData.objects.create(user=request.user, video_url=video_url, video_title=video_title)

            # Return the video title in the response
            return JsonResponse({'title': video_title})

        except json.JSONDecodeError:
            return JsonResponse({'error': 'Invalid JSON'}, status=400)

    return JsonResponse({'error': 'Invalid request'}, status=400)


@login_required
def home_view(request):
    # Retrieve only the videos for the currently logged-in user
    user_videos = YouTubeData.objects.filter(user=request.user).order_by('-added_at')

    context = {
        'user_videos': user_videos,
    }
    return render(request, 'watchapp/homepage.html', context)


def result(request):
    """Scrape the YouTube page for the video title."""
    if request.method == 'POST':
        youtube_url = request.POST.get('youtube_url')

        # Make a request to the YouTube page
        response = requests.get(youtube_url)
        if response.status_code == 200:
            soup = BeautifulSoup(response.content, 'html.parser')

            # Extract the video title
            title = soup.find('meta', property='og:title')
            video_title = title['content'] if title else 'Title not found'

            # Pass the title to the template
            return render(request, 'watchapp/result.html', {'video_title': video_title})
        else:
            return render(request, 'watchapp/result.html', {'error': 'Could not retrieve the page.'})
    return render(request, 'watchapp/home.html')

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

def homepage(request):
    videos = YouTubeData.objects.all().order_by('-timestamp')  # Get all videos sorted by latest
    return render(request, 'watchapp/homepage.html', {'videos': videos})

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