from django.contrib import admin
from django.urls import include, path

urlpatterns = [
    path('', include('admin_panel.urls')),
    path('admin/', admin.site.urls),
    path('api/', include('products.urls')),
    path('api/', include('user.urls')),
]

# No need to serve media files with static() since they are stored on S3
