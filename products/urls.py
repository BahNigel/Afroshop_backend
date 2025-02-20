# products/urls.py
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import AboutUsViewSet, CategoryViewSet, CheckoutDeleteView, CheckoutItemDeleteView, CheckoutView, ContactUsView, PaymentView, ProductViewSet

router = DefaultRouter()

router = DefaultRouter()
router.register(r'categroys', CategoryViewSet)
router.register(r'products', ProductViewSet)
router.register(r'about_us', AboutUsViewSet, basename='about_us')

urlpatterns = [
    path('', include(router.urls)),
    path('checkout/', CheckoutView.as_view(), name='checkout'),
    path('checkout/<int:checkout_id>/item/<int:item_id>/', CheckoutItemDeleteView.as_view(), name='delete_checkout_item'),
    path('checkout/<int:checkout_id>/', CheckoutDeleteView.as_view(), name='checkout_delete'),
    
    path('order/', PaymentView.as_view(), name='order'),
    path('order/<int:order_id>/', PaymentView.as_view(), name='delete_order'),
    
    path('payments/<int:order_id>/update-status/', PaymentView.as_view(), name='payment-update-status'),
    
    path("contact_us/", ContactUsView.as_view(), name="contact_us"),
]
