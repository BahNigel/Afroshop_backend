from django.http import Http404
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth.decorators import login_required

from user.models import User

# List of all users
@login_required
def user_list(request):
    # Fetch all users from the User model
    users = User.objects.all()
    return render(request, 'pages/users/user_list.html', {'users': users})

# Create or Edit User (same template)
@login_required
def create_or_edit_user(request, user_id=None):
    if user_id:
        # If we're editing an existing user, fetch the user
        user = User.objects.get(id=user_id)
        if request.method == 'POST':
            # Update user data
            email = request.POST['email']
            password = request.POST.get('password')

            user.email = email
            if password:
                user.set_password(password)
            user.save()
            return redirect('user_list')  # Redirect to user list after saving

    else:
        # If we're creating a new user
        user = None
        if request.method == 'POST':
            # Create a new user
            email = request.POST['email']
            password = request.POST.get('password')
            user = User(email=email)
            if password:
                user.set_password(password)
            user.is_staff = True  # Make sure the user is a superuser
            user.is_superuser = True
            user.save()
            return redirect('user_list')  # Redirect to user list after creating

    return render(request, 'pages/users/create_or_edit_user.html', {'user': user})
# Delete User
@login_required
def delete_user(request, user_id):
    try:
        user = User.objects.get(id=user_id)
        user.delete()
        return redirect('user_list')  # Redirect back to the user list page after deletion
    except User.DoesNotExist:
        raise Http404("User not found")
