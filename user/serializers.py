from rest_framework import serializers
from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError
from django.contrib.auth import authenticate
from user.models import User


class LoginSerializer(serializers.Serializer):
    username = serializers.CharField()  # Can be email or username
    password = serializers.CharField(write_only=True)

    def validate(self, data):
        username = data['username']
        password = data['password']
        print("now: ", data)

        # Authenticate using email or first_name
        if '@' in username and '.' in username:
            # Attempt to authenticate using email
            user = authenticate(email=username, password=password)
        else:
            # Attempt to authenticate using first_name
            try:
                user_obj = User.objects.get(first_name=username)
                print('last 1: ', data)
                user = authenticate(email=user_obj.email, password=password)
                print('last 2: ', data)
            except User.DoesNotExist:
                print('last 3: ', data)
                user = None

        if not user:
            raise serializers.ValidationError('Invalid credentials')
        
        if not user.is_active:
            raise serializers.ValidationError('User account is disabled')

        data['user'] = user
        return data



class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)
    username = serializers.CharField(write_only=True)  # Incoming username field

    class Meta:
        model = User
        fields = ['username', 'email', 'first_name', 'last_name', 'password']

    def validate(self, data):
        # Ensure that the username is not empty and map to first_name
        if 'username' in data:
            data['first_name'] = data.pop('username')  # Assign the username to first_name

        # If `last_name` is not provided, set it to an empty string
        if 'last_name' not in data:
            data['last_name'] = ''

        if 'email' not in data:
            raise serializers.ValidationError("Email is required")

        return data

    def create(self, validated_data):
        # Create the user object with the provided validated data
        user = User.objects.create_user(
            email=validated_data['email'],
            first_name=validated_data['first_name'],
            last_name=validated_data['last_name'],  # Allow empty string if not provided
            password=validated_data['password']
        )
        return user
    
class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['email', 'first_name', 'last_name']

    def update(self, instance, validated_data):
        # Ensure you update the fields properly
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()
        return instance