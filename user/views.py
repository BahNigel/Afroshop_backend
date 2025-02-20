from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework_simplejwt.tokens import RefreshToken  # For JWT token generation
from .serializers import LoginSerializer, RegisterSerializer, UserSerializer
from rest_framework.permissions import AllowAny, IsAuthenticated  # For permission control
from .models import User

# Login View
class LoginView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        print("Login Request Data:", request.data)  # Debug: Log incoming request data
        serializer = LoginSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.validated_data['user']
            
            # Check if user already has a refresh token, if so, use it
            if user.refresh_token:
                refresh = RefreshToken(user.refresh_token)  # Use the existing refresh token
            else:
                # Generate JWT tokens if not set
                refresh = RefreshToken.for_user(user)
                user.refresh_token = str(refresh)  # Save the refresh token to the user's record
                user.save()  # Save the user with the new refresh token
            
            access_token = str(refresh.access_token)  # Access token as string

            return Response({
                'access': access_token,
                'refresh': str(refresh),  # Return both access and refresh tokens
                'user': {
                    'id': user.id,
                    'email': user.email,
                    'first_name': user.first_name,
                    'last_name': user.last_name,
                }
            }, status=status.HTTP_200_OK)
        
        print("Login Validation Errors:", serializer.errors)  # Log validation errors
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# Register View
class RegisterView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        print("Register Request Data:", request.data)  # Debug: Log incoming request data
        serializer = RegisterSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()  # Save the user
            
            # Check if the user already has a refresh token. If not, generate one.
            if user.refresh_token:
                refresh = RefreshToken(user.refresh_token)  # Use the existing refresh token
            else:
                # Generate JWT tokens for the newly created user
                refresh = RefreshToken.for_user(user)
                user.refresh_token = str(refresh)  # Save the refresh token to the user's record
                user.save()  # Save the user with the new refresh token
            
            access_token = str(refresh.access_token)  # Access token as string

            return Response({
                'access': access_token,
                'refresh': str(refresh),  # Return both access and refresh tokens
                'user': {
                    'id': user.id,
                    'email': user.email,
                    'first_name': user.first_name,
                    'last_name': user.last_name,
                }
            }, status=status.HTTP_201_CREATED)
        
        print("Register Validation Errors:", serializer.errors)  # Log validation errors
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    def put(self, request, *args, **kwargs):
        user = request.user  # Get the current logged-in user
        print("Incoming Request Data:", request.data)  # Log incoming request data

        # Extract the data from the 'updatedInfo' key
        updated_info = request.data.get('updatedInfo', {})

        if not updated_info:
            return Response({"error": "No data provided for update"}, status=status.HTTP_400_BAD_REQUEST)

        # Initialize the serializer with the existing user instance and the extracted updated_info
        serializer = UserSerializer(user, data=updated_info, partial=True)

        # Check if the serializer is valid
        if serializer.is_valid():
            # Save the updated user instance
            updated_user = serializer.save()

            # Log the updated user data
            print("Updated User:", updated_user)

            # Return the updated user data in the response
            return Response({
                "message": "User data updated successfully.",
                "user": UserSerializer(updated_user).data  # Send the updated user data
            }, status=status.HTTP_200_OK)
        
        # If the serializer is not valid, return validation errors
        print("Serializer Errors:", serializer.errors)  # Log validation errors
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# View for getting user data
class UserDataView(APIView):
    permission_classes = [IsAuthenticated]  # Ensure the user is authenticated

    def get(self, request):
        user = request.user  # Get the current logged-in user
        serializer = UserSerializer(user)  # Serialize the user data
        return Response({
            'user': serializer.data  # Return serialized user data
        }, status=status.HTTP_200_OK)
