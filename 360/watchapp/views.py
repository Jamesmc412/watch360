from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login
from .forms import LoginForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib.auth.hashers import make_password
from django.contrib import messages
from django.contrib.auth import update_session_auth_hash
from friendship.models import Friend, FriendshipRequest
from django.http import HttpResponse

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
# Get all friends of the logged-in user
    friends = Friend.objects.friends(request.user)

    # Create a list of usernames from the friends queryset
    friends_data = [{'username': friend.username} for friend in friends]

    return render(request, 'watchapp/homepage.html', {"friends": friends_data})

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
    
    if Friend.objects.are_friends(request.user, user):
        return HttpResponse("You are already friends.")
    
    # Send the request
    Friend.objects.add_friend(
        request.user,           # The sender
        user,                   # The recipient
    )
    return redirect('user_list')

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