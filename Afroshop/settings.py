"""
Django settings for Afroshop project.

Generated by 'django-admin startproject' using Django 5.1.3.

For more information on this file, see:
https://docs.djangoproject.com/en/5.1/topics/settings/
"""

from pathlib import Path
import os
from datetime import timedelta
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

# Security settings
SECRET_KEY = os.getenv('SECRET_KEY')  # Use env variable
DEBUG = os.getenv('DJANGO_DEBUG', 'True') == 'True'  # Convert to boolean
ALLOWED_HOSTS = os.getenv('DJANGO_ALLOWED_HOSTS', '*').split(',')

# Application definition
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'corsheaders',
    'user',
    'products',
    'admin_panel',
    'rest_framework.authtoken',
    'rest_framework_simplejwt',
    'storages',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'corsheaders.middleware.CorsMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'Afroshop.urls'
CORS_ALLOW_ALL_ORIGINS = True

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'Afroshop.wsgi.application'
AUTH_USER_MODEL = 'user.User'

# REST Framework Simple JWT Settings
REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': [
        'rest_framework_simplejwt.authentication.JWTAuthentication',
    ],
}

SIMPLE_JWT = {
    'ACCESS_TOKEN_LIFETIME': timedelta(days=90),
    'REFRESH_TOKEN_LIFETIME': timedelta(days=90),
    'ROTATE_REFRESH_TOKENS': False,
    'BLACKLIST_AFTER_ROTATION': False,
    'ALGORITHM': 'HS256',
    'SIGNING_KEY': SECRET_KEY,
}

# Database Configuration
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': os.getenv('DB_NAME', 'afroshop'),
        'USER': os.getenv('DB_USER', 'afroshop'),
        'PASSWORD': os.getenv('DB_PASSWORD'),
        'HOST': os.getenv('DB_HOST', 'afroshop.c7oe6sysycjs.eu-north-1.rds.amazonaws.com'),
        'PORT': os.getenv('DB_PORT', '5432'),
    }
}

# Password Validation
AUTH_PASSWORD_VALIDATORS = [
    {'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator'},
    {'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator'},
    {'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator'},
    {'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator'},
]

# Internationalization
LANGUAGE_CODE = 'en-us'
TIME_ZONE = 'UTC'
USE_I18N = True
USE_TZ = True


AWS_S3 = os.getenv("AWS_S3", "True") == "True"

# AWS S3 Configurations
AWS_ACCESS_KEY_ID = os.getenv("AWS_ACCESS_KEY_ID")  # Set in your environment variables
AWS_SECRET_ACCESS_KEY = os.getenv("AWS_SECRET_ACCESS_KEY")  # Set in your environment variables
AWS_STORAGE_BUCKET_NAME = "afroshop"  # Replace with your bucket name
AWS_S3_REGION_NAME = "us-east-1"  # Change based on your AWS region
AWS_S3_CUSTOM_DOMAIN = f"{AWS_STORAGE_BUCKET_NAME}.s3.amazonaws.com"

# Object parameters (Optional: Set cache control, public access, etc.)
AWS_S3_OBJECT_PARAMETERS = {
    "CacheControl": "max-age=86400",
}

AWS_DEFAULT_ACL = None  # Ensures full public access if needed
AWS_QUERYSTRING_AUTH = False  # Removes authentication query params from URLs

# Enable S3 Storage for both Static and Media Files
DEFAULT_FILE_STORAGE = "storages.backends.s3boto3.S3Boto3Storage"
STATICFILES_STORAGE = "storages.backends.s3boto3.S3Boto3Storage"

# URLs for Static and Media files served from S3
STATIC_URL = f"https://{AWS_S3_CUSTOM_DOMAIN}/static/"
MEDIA_URL = f"https://{AWS_S3_CUSTOM_DOMAIN}/media/"

# No need for local static and media files
STATIC_ROOT = None
MEDIA_ROOT = None

# Default Auto Field
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'
# ssh -i "afroshop.pem" ubuntu@ec2-51-20-107-27.eu-north-1.compute.amazonaws.com
