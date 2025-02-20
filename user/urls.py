from django.urls import path
from .views import LoginView, RegisterView, UserDataView

urlpatterns = [
    path('auth/login/', LoginView.as_view(), name='login'),
    path('auth/register/', RegisterView.as_view(), name='register'),
    path('auth/update/', RegisterView.as_view(), name='update-user'),
    path('auth/user/', UserDataView.as_view(), name='user_data'),
]
