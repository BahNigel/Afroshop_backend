from django.urls import path

from admin_panel.views import about_view, messages_views

from .views import category_views
from .views import products_views
from .views import checkout_views
from .views import payment_views
from .views import users_views
from .views import views

urlpatterns = [
    path('', views.dashboard, name='index'),
    path('list/', products_views.product_list, name='product_list'),
    path('create/', products_views.product_create_or_edit, name='product_create'),
    path('edit/<int:pk>/', products_views.product_create_or_edit, name='product_edit'),
    path('delete/<int:pk>/', products_views.product_delete, name='product_delete'),
    
    path('categories/', category_views.category_list, name='category_list'),  # List categories
    path('category/create/', category_views.category_create, name='category_create'),  # Create category
    path('category/edit/<int:pk>/', category_views.category_edit, name='category_edit'),  # Edit category
    path('category/delete/<int:pk>/', category_views.category_delete, name='category_delete'),  # Delete category
    
    path('checkouts/', checkout_views.checkout_list, name='checkout_list'),
    
    path('payments/', payment_views.payment_list, name='payment_list'),
    
    path('users/', users_views.user_list, name='user_list'),
    path('users/create/', users_views.create_or_edit_user, name='create_user'),  # For creating a user
    path('users/edit/<int:user_id>/', users_views.create_or_edit_user, name='edit_user'),  # For editing a user
    path('users/delete/<int:user_id>/', users_views.delete_user, name='delete_user'),
    
    path('contact_us_messages/', messages_views.contact_messages_list, name='contact_us_messages'),
    
    path('about_us', about_view.about_us_view, name='about_us'),
    path('edit_about_us', about_view.about_us_edit, name='edit_about_us'),
]
