from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as DefaultUserAdmin
from .models import User
from rest_framework_simplejwt.tokens import RefreshToken  # Import JWT token generation

class UserAdmin(DefaultUserAdmin):
    list_display = ('id', 'first_name', 'last_name', 'email', 'is_active', 'is_staff', 'user_token')  # Add 'user_token' here
    search_fields = ('email',)
    ordering = ('-date_joined',)

    def user_token(self, obj):
        # Generate a fresh JWT token for the user
        refresh = RefreshToken.for_user(obj)
        return str(refresh.access_token)  # Return only the access token (can be adjusted as needed)
    
    user_token.short_description = 'User Token'  # Customize the column name in the admin list view

admin.site.register(User, UserAdmin)
