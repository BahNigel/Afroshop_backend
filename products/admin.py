from django.contrib import admin
from .models import Checkout, ContactUs, Payment, Product, Category, ProductRating

class ProductAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'price', 'category', 'type')  # Remove 'stock' if not in the model
    list_filter = ('category', 'type')
    search_fields = ('name', 'category__name')  # Assuming category is a ForeignKey
    ordering = ('-created_at',)

class CategoryAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'created_at')
    search_fields = ('name',)
    
class CheckoutAdmin(admin.ModelAdmin):
    list_display = ('user', 'cart_items', 'total_price', 'created_at', 'status')
    search_fields = ('user',)
    
class PaymentAdmin(admin.ModelAdmin):
    list_display = ('user', 'items', 'total_price', 'created_at', 'status', 'orderId')
    search_fields = ('user',)
    
class ProductsRatingAdmin(admin.ModelAdmin):
    list_display = ('product', 'user', 'rating', 'review', 'Admin_rating', 'created_at')
    search_fields = ('user',)

admin.site.register(Product, ProductAdmin)
admin.site.register(Category, CategoryAdmin)
admin.site.register(Checkout, CheckoutAdmin)
admin.site.register(Payment, PaymentAdmin)
admin.site.register(ProductRating, ProductsRatingAdmin)
admin.site.register(ContactUs)
