from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, update_session_auth_hash
from .forms import LoginForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib import messages
from bs4 import BeautifulSoup
import requests
import json
from .models import YouTubeData, OnlineStatus, Profile
from django.views.decorators.csrf import csrf_exempt
from datetime import timedelta
from django.db.models import F, Q # added for search functionality
from background_task import background
from friendship.models import Friend, FriendshipRequest
from django.http import HttpResponse, JsonResponse
from friendship.exceptions import AlreadyExistsError
from django.views import View
from django.contrib.auth.mixins import LoginRequiredMixin
from django import forms
from django.db import transaction
from friendship.exceptions import AlreadyExistsError


def get_video_data(video_url):
    """Fetch video title and duration from YouTube API."""
    try:
        # Extract video ID from URL if it contains 'v=' parameter
        video_id = video_url.split('v=')[1].split('&')[0] if 'v=' in video_url else None
        if not video_id:
            # Return error if video ID cannot be extracted
            return None, None, "Invalid YouTube URL"

        # API endpoint with user's API key and extracted video ID
        api_key = 'AIzaSyB0ck1zWAO-20vOaNRdgYu7-yTNCS0jtZE'  # Replace with your API key
        endpoint = f'https://www.googleapis.com/youtube/v3/videos?part=snippet,contentDetails&id={video_id}&key={api_key}'
        
        # Make API request to fetch video data
        response = requests.get(endpoint)
        response.raise_for_status()  # Raise an error for bad responses
        
        # Parse JSON response
        data = response.json()
        if data['items']:
            # Extract video title and duration if video data is found
            video_title = data['items'][0]['snippet']['title']
            duration = data['items'][0]['contentDetails']['duration']
            duration_seconds = convert_duration_to_seconds(duration)  # Convert duration to seconds
            return video_title, duration_seconds, None
        # Return error if video is not found
        return None, None, "Video not found"

    except Exception as e:
        # Handle and print any error that occurs during the API request
        print(f"Error fetching video data: {e}")
        return None, None, "Could not retrieve video data"


@csrf_exempt  # Exempt from CSRF checks to allow AJAX requests
@login_required  # Require user to be logged in to access this view
def search_video(request):
    if request.method == "POST":
        try:
            # Parse JSON data from the request body
            data = json.loads(request.body)
            video_url = data.get("youtube_url")

            # Check if a YouTube URL is provided
            if not video_url:
                return JsonResponse({'error': 'YouTube URL is required'}, status=400)

            # Retrieve video title and duration using helper function
            vid_title, duration, error = get_video_data(video_url)
            if error:
                # Return an error if video data retrieval fails
                return JsonResponse({'error': error}, status=400)

            # Clear any previous video entries for the current user
            YouTubeData.objects.filter(user=request.user).delete()

            # Create a new video data entry in the database for the user
            new_video = YouTubeData.objects.create(
                user=request.user,
                video_url=video_url,
                video_title=vid_title,
                duration=duration
            )
            
            # Update user's online status with the new video title
            OnlineStatus.objects.filter(user=request.user).update(video_title=new_video, is_online=True)

            # Schedule a task to delete the video after its duration has elapsed
            delete_video_task(new_video.id, schedule=timedelta(seconds=duration))

            # Return success response with video title
            return JsonResponse({'message': 'Video scheduled for deletion', 'title': vid_title})

        except json.JSONDecodeError:
            # Handle invalid JSON data
            return JsonResponse({'error': 'Invalid JSON'}, status=400)

    # Handle non-POST requests
    return JsonResponse({'error': 'Invalid request'}, status=400)



# this function should update the online status of the user for already-registered users (james)
@csrf_exempt
@login_required
def update_online_status(request):
    if request.method == 'POST':
        is_online = request.POST.get('is_online') == 'true'
        try:
            # Update or create the OnlineStatus for the logged-in user
            online_status, created = OnlineStatus.objects.get_or_create(user=request.user)
            online_status.is_online = is_online
            online_status.save()
            return JsonResponse({'status': 'success', 'is_online': online_status.is_online})
        except OnlineStatus.DoesNotExist:
            return JsonResponse({'status': 'error', 'message': 'OnlineStatus not found.'})
    return JsonResponse({'status': 'error', 'message': 'Invalid request method.'})

# Background task to delete video after the specified duration
@background
def delete_video_task(video_id):
    try:
        # Retrieve video by ID and delete it from the database
        video = YouTubeData.objects.get(id=video_id)
        video.delete()
        print(f"Video {video_id} deleted after its duration.")
    except YouTubeData.DoesNotExist:
        # Handle case where video does not exist in the database
        print(f"Video {video_id} not found.")


@login_required  # Ensure the user is authenticated
def check_videos_status(request):
    # Get the count of videos for the logged-in user
    video_count = YouTubeData.objects.filter(user=request.user).count()
    # Return the count as a JSON response
    return JsonResponse({'video_count': video_count})


@login_required  # Ensure the user is authenticated
def delete_video(request, video_id):
    # Retrieve the video by ID for the logged-in user, or return 404 if not found
    video = get_object_or_404(YouTubeData, id=video_id, user=request.user)
    # Delete the video immediately when requested
    video.delete()
    # Redirect the user to the homepage after deletion
    return redirect('homepage')


def convert_duration_to_seconds(duration):
    """Convert ISO 8601 duration format to total seconds."""
    import isodate  # Ensure the 'isodate' library is installed to parse ISO 8601 durations
    try:
        # Parse duration and return it in seconds
        return int(isodate.parse_duration(duration).total_seconds())
    except Exception:
        # Return 0 seconds if parsing fails
        return 0


def result(request):
    """Scrape the YouTube page for the video title."""
    if request.method == 'POST':
        # Get the YouTube URL from the POST request data
        youtube_url = request.POST.get('youtube_url')

        # Make an HTTP request to the YouTube page
        response = requests.get(youtube_url)
        if response.status_code == 200:
            # Parse the page content using BeautifulSoup
            soup = BeautifulSoup(response.content, 'html.parser')

            # Extract the video title from the meta tag
            title = soup.find('meta', property='og:title')
            video_title = title['content'] if title else 'Title not found'

            # Render the homepage template with the extracted video title
            return render(request, 'watchapp/homepage.html', {'video_title': video_title})
        else:
            # Return an error message if page retrieval fails
            return render(request, 'watchapp/homepage.html', {'error': 'Could not retrieve the page.'})
    # Render the homepage template for non-POST requests
    return render(request, 'watchapp/homepage.html')


def chat_view(request):
    # Render the chat page template for chat functionality
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
                
                # Use transaction.atomic to ensure data consistency
                with transaction.atomic():
                    # Update or create the OnlineStatus instance
                    OnlineStatus.objects.update_or_create(
                        user=user,
                        defaults={
                            'video_title': None,
                            'is_online': True
                            }
                    )
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

        # username must be unique
        if User.objects.filter(username=username).exists():
            error = "The username is already taken!"
        # password must be at least 6 characters
        elif len(password) < 6:
            error = "Password must have at least 6 characters."
        elif password != confirm_password:
            error = "Passwords do not match."
        else:
            # Create a new user
            user = User.objects.create_user(
                username=username, password=password, 
                first_name=first_name, last_name=last_name)
            return redirect('login')

    return render(request, 'watchapp/register.html', {'error': error})

@login_required
def homepage_view(request):
    user = request.user  # Get the logged-in user

    # Get all friends of the logged-in user
    friends = Friend.objects.friends(user)

    # Retrieve only the videos for the currently logged-in user
    user_videos = YouTubeData.objects.filter(user=user).order_by('-added_at')

    # Get all pending friend requests
    pending_requests = FriendshipRequest.objects.filter(to_user=request.user, rejected__isnull=True)
    # Create a list of pending friend requests
    pending_requests_data = [{'request_id': req.id, 'id': req.from_user.id, 'username': req.from_user.username} for req in pending_requests]
    
    # Create a list of usernames from the friends queryset
    friends_data = [{'username': friend.username, 'avatar': friend.profile.avatar.url} for friend in friends]

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
        return redirect('login') # Redirect to the login page after updating the user
    
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
        'is_online': OnlineStatus.objects.filter(user=user).first().is_online if OnlineStatus.objects.filter(user=user).exists() else False,
        'pending_requests': pending_requests_data,
    }

    return render(request, 'watchapp/homepage.html', context)

def logout_view(request):
    # when a user logs out, set their online status to False (james)
    OnlineStatus.objects.filter(user=request.user).update(is_online=False) 
    # Clear the session data
    request.session.flush()
    # Redirect to the login page
    return redirect('login')

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
    
    # Handle the case when the request was already sent
    except AlreadyExistsError:
        return JsonResponse({'status': 'already_requested'})  

# View to accept a friend request
@login_required
def accept_friend_request(request, request_id):
    try:
        friend_request = get_object_or_404(FriendshipRequest, id=request_id)
        
        # Make sure the right user is accepting the request
        if friend_request.to_user != request.user:
            return HttpResponse("You don't have permission to accept this request.")
        
        # Accept the request
        friend_request.accept()
        return redirect('homepage')  # Redirect to the homepage
    
    # Handle the case when the request does not exist
    except FriendshipRequest.DoesNotExist:
        return JsonResponse({'status': 'error', 'message': 'Friend request does not exist'}, status=404)

@login_required
def friends_online_status(request):
    friends = Friend.objects.friends(request.user)  # Assuming you're using Django-Friendship
    friends_status = [
        {
            'username': friend.username,
            'is_online': OnlineStatus.objects.filter(user=friend).first().is_online
        }
        for friend in friends
    ]
    return JsonResponse(friends_status, safe=False)

# View to reject a friend request
@login_required
def reject_friend_request(request, request_id):
    try:
        friend_request = get_object_or_404(FriendshipRequest, id=request_id)
        
        # Make sure the correct user is rejecting the request
        if friend_request.to_user != request.user:
            return HttpResponse("You don't have permission to reject this request.")
        
        # Reject the request
        friend_request.reject()
        return redirect('homepage')  # Redirect to the homepage
    
    # Handle the case when the request does not exist
    except FriendshipRequest.DoesNotExist:
        return JsonResponse({'status': 'error', 'message': 'Friend request does not exist'}, status=404)

# View to unfriend someone
@login_required
def unfriend(request, user_id):
    user = get_object_or_404(User, id=user_id)
    
    # Remove the friendship
    Friend.objects.remove_friend(request.user, user)
    return redirect('user_list')
    
# search taask 
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
