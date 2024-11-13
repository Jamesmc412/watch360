from django.shortcuts import render, redirect, get_object_or_404
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
from .models import YouTubeData, OnlineStatus
from django.views.decorators.http import require_POST
from django.views.decorators.csrf import csrf_exempt
from django.utils import timezone
from datetime import timedelta
from django.shortcuts import get_object_or_404
from django.utils.timezone import now
from django.db.models import F
from datetime import timedelta
from background_task import background
from friendship.models import Friend, FriendshipRequest
from django.http import HttpResponse, JsonResponse
from django.db.models import Q  # Added for search functionality
from friendship.exceptions import AlreadyExistsError
from django.views import View
from django.contrib.auth.mixins import LoginRequiredMixin
from django import forms
from django.contrib.auth.models import User
from .models import Profile

def get_video_data(video_url):
    """Fetch video title and duration from YouTube API."""
    try:
        video_id = video_url.split('v=')[1].split('&')[0] if 'v=' in video_url else None
        if not video_id:
            return None, None, "Invalid YouTube URL"

        api_key = 'AIzaSyB0ck1zWAO-20vOaNRdgYu7-yTNCS0jtZE'  # Replace with your API key
        endpoint = f'https://www.googleapis.com/youtube/v3/videos?part=snippet,contentDetails&id={video_id}&key={api_key}'
        
        response = requests.get(endpoint)
        response.raise_for_status()
        
        data = response.json()
        if data['items']:
            video_title = data['items'][0]['snippet']['title']
            duration = data['items'][0]['contentDetails']['duration']
            duration_seconds = convert_duration_to_seconds(duration)
            return video_title, duration_seconds, None
        return None, None, "Video not found"

    except Exception as e:
        print(f"Error fetching video data: {e}")
        return None, None, "Could not retrieve video data"
    
    
@csrf_exempt  # Ensure AJAX requests work
@login_required
def search_video(request):
    if request.method == "POST":
        try:
            data = json.loads(request.body)
            video_url = data.get("youtube_url")

            if not video_url:
                return JsonResponse({'error': 'YouTube URL is required'}, status=400)

            # Get video data (title and duration)
            video_title, duration, error = get_video_data(video_url)
            if error:
                return JsonResponse({'error': error}, status=400)

            # Delete previous videos of this user
            YouTubeData.objects.filter(user=request.user).delete()

            # Save the new video data
            new_video = YouTubeData.objects.create(
                user=request.user,
                video_url=video_url,
                video_title=video_title,
                duration=duration
            )

            # Schedule deletion based on video duration
            delete_video_task(new_video.id, schedule=timedelta(seconds=duration))

            # Return success response
            return JsonResponse({'message': 'Video scheduled for deletion', 'title': video_title})

        except json.JSONDecodeError:
            return JsonResponse({'error': 'Invalid JSON'}, status=400)

    return JsonResponse({'error': 'Invalid request'}, status=400)


@login_required
def homepage_view(request):
    user = request.user  # Get the logged-in user
    # Retrieve only the videos for the currently logged-in user
    user_videos = YouTubeData.objects.filter(user=request.user).order_by('-added_at')

    # Get all friends of the logged-in user
    friends = Friend.objects.friends(user)
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
        return redirect('login')

    # Create a list of usernames from the friends queryset
    friends_data = []
    for friend in friends:
        online_status = OnlineStatus.objects.filter(user=friend).first()
        latest_video = YouTubeData.objects.filter(user=friend).order_by('-added_at').first()
        friends_data.append({
            'username': friend.username,
            'is_online': online_status.is_online if online_status else False,
            'video': latest_video  # Add the video object to the friend's data
        })
    
    context = {
        'user_videos': user_videos,
        'friends': friends_data,
        'is_online': OnlineStatus.objects.filter(user=user).first().is_online if OnlineStatus.objects.filter(user=user).exists() else False
    }
    
    return render(request, 'watchapp/homepage.html', context)

# Background task to delete video after the duration
@background
def delete_video_task(video_id):
    try:
        video = YouTubeData.objects.get(id=video_id)
        video.delete()
        print(f"Video {video_id} deleted after its duration.")
    except YouTubeData.DoesNotExist:
        print(f"Video {video_id} not found.")

        
@login_required
def check_videos_status(request):
    video_count = YouTubeData.objects.filter(user=request.user).count()
    return JsonResponse({'video_count': video_count})

@login_required
def delete_video(request, video_id):
    video = get_object_or_404(YouTubeData, id=video_id, user=request.user)
    video.delete()  # Delete immediately when requested from the UI
    return redirect('homepage')
    
def convert_duration_to_seconds(duration):
    """Convert ISO 8601 duration to seconds."""
    import isodate  # Make sure the 'isodate' library is installed
    try:
        return int(isodate.parse_duration(duration).total_seconds())
    except Exception:
        return 0  # If conversion fails, return 0 seconds

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
            return render(request, 'watchapp/homepage.html', {'video_title': video_title})
        else:
            return render(request, 'watchapp/homepage.html', {'error': 'Could not retrieve the page.'})
    return render(request, 'watchapp/homepage.html')

def chat_view(request):
    return render(request, 'chat.html')


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
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
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
            user = User.objects.create_user(
                username=username, password=password, 
                first_name=first_name, last_name=last_name)
            messages.success(request, 'Registration successful! Redirecting to login...')
            return redirect('login')

    return render(request, 'watchapp/register.html', {'error': error})

def logout_view(request):
    # Clear the session data
    request.session.flush()
    # Redirect to the login page
    return redirect('login')

# View to display all users
@login_required
def user_list(request):
    users = User.objects.exclude(id=request.user.id)
    friends = Friend.objects.friends(request.user)
    friend_requests_sent = Friend.objects.sent_requests(user=request.user)
    friend_requests_received = Friend.objects.unrejected_requests(user=request.user)
    
    context = {
        'users': users,
        'friends': friends,
        'friend_requests_sent': friend_requests_sent,
        'friend_requests_received': friend_requests_received,
    }
    return render(request, 'watchapp/user_list.html', context)

@csrf_exempt
@require_POST
def update_online_status(request):
    
    is_online = request.POST.get('is_online') == 'true';
    
    # Update the online status of the user
    user = request.user
    online_status, created = OnlineStatus.objects.get_or_create(user=user)
    online_status.is_online = is_online
    online_status.save()
    
    return JsonResponse({'status': 'success', 'is_online': online_status.is_online})
        

# View to send a friend request
@login_required
def send_friend_request(request, user_id):
    user = get_object_or_404(User, id=user_id)
    
    # Check if they are already friends
    if Friend.objects.are_friends(request.user, user):
        return JsonResponse({'status': 'already_friends'})

    # Try to send the friend request and catch the AlreadyExistsError
    try:
        Friend.objects.add_friend(
            request.user,           # The sender
            user                    # The recipient
        )
        return JsonResponse({'status': 'success'})
    except AlreadyExistsError:
        return JsonResponse({'status': 'already_requested'})  # Handle the case when the request was already sent

# View to accept a friend request
@login_required
def accept_friend_request(request, request_id):
    friend_request = get_object_or_404(FriendshipRequest, id=request_id)
    
    if friend_request.to_user != request.user:
        return HttpResponse("You don't have permission to accept this request.")
    
    # Accept the request
    friend_request.accept()
    return redirect('user_list')

# View to reject a friend request
@login_required
def reject_friend_request(request, request_id):
    friend_request = get_object_or_404(FriendshipRequest, id=request_id)
    
    if friend_request.to_user != request.user:
        return HttpResponse("You don't have permission to reject this request.")
    
    # Reject the request
    friend_request.reject()
    return redirect('user_list')

# View to unfriend someone
@login_required
def unfriend(request, user_id):
    user = get_object_or_404(User, id=user_id)
    
    # Remove the friendship
    Friend.objects.remove_friend(request.user, user)
    return redirect('user_list')
    
# search taask -rj
@login_required
def search_users(request):
    query = request.GET.get('q', None)
    if query:
        users = User.objects.filter(Q(username__icontains=query)).exclude(id=request.user.id)
        user_data = [{'id': user.id, 'username': user.username} for user in users]  # Include user ID
        return JsonResponse(user_data, safe=False)
    return JsonResponse([], safe=False)

# views.py
class MyProfile(LoginRequiredMixin, View):
    def get(self, request):
        user_form = ProfileUpdateForm(instance=request.user)
        profile_form = ProfileUpdateForm(instance=request.user.profile)
        
        context = {
            'user_form': user_form,
            'profile_form': profile_form
        }
        
        return render(request, 'watchapp/profile.html', context)
    
    def post(self, request):
        user_form = ProfileUpdateForm(request.POST, instance=request.user)
        profile_form = ProfileUpdateForm(request.POST, request.FILES, instance=request.user.profile)

        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()
            messages.success(request, 'Your profile has been updated successfully')
            return redirect('profile')
        else:
            context = {
                'user_form': user_form,
                'profile_form': profile_form
            }
            messages.error(request, 'Error updating your profile')
            return render(request, 'watchapp/profile.html', context)

        
class ProfileUpdateForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['avatar', 'bio']  # Include the bio field here
