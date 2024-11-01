from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login
from .forms import LoginForm
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_POST
from django.contrib.auth.models import User
from django.contrib.auth.hashers import make_password
from django.contrib import messages
from django.contrib.auth import update_session_auth_hash
from friendship.models import Friend, FriendshipRequest
from django.http import HttpResponse, JsonResponse
from django.db.models import Q  # Added for search functionality
from friendship.exceptions import AlreadyExistsError

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
            return redirect('login')

    return render(request, 'watchapp/register.html', {'error': error})

def homepage_view(request):
    # Get all friends of the logged-in user
    friends = Friend.objects.friends(request.user)

    # Get all pending friend requests
    pending_requests = FriendshipRequest.objects.filter(to_user=request.user, rejected__isnull=True)
    # Create a list of pending friend requests
    pending_requests_data = [{'id': req.from_user.id, 'username': req.from_user.username} for req in pending_requests]
    
    # Create a list of usernames from the friends queryset
    friends_data = [{'username': friend.username} for friend in friends]

    return render(request, 'watchapp/homepage.html', {
        "friends": friends_data,
        "pending_requests": pending_requests_data
    })

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
@require_POST
def accept_friend_request(request, request_id):
    try:
        print(f"Attempting to accept friend request with ID: {request_id}")
        pending_requests = FriendshipRequest.objects.filter(to_user=request.user, rejected__isnull=True)
        print(f"Pending requests for {request.user.username}: {[req.id for req in pending_requests]}")
        
        friend_request = FriendshipRequest.objects.get(id=request_id, to_user=request.user)
        friend_request.accept()
        print("Friend request accepted successfully")
        return JsonResponse({'status': 'success'})
    except FriendshipRequest.DoesNotExist:
        print("Friend request does not exist")
        return JsonResponse({'status': 'error', 'message': 'Friend request does not exist'}, status=404)

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