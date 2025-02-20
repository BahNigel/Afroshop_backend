# views.py

from django.shortcuts import render
from products.models import Checkout, Product

def checkout_list(request):
    # Get all checkouts for all users (no filter by user)
    checkouts = Checkout.objects.all().order_by('-created_at')
    
    # For each checkout, fetch the related product details (name and image)
    for checkout in checkouts:
        for item in checkout.cart_items:
            try:
                product = Product.objects.get(id=item['id'])
                item['product_name'] = product.name
                item['price'] = product.price
                item['product_image'] = product.image.url if product.image else None 
            except Product.DoesNotExist:
                continue
    
    context = {
        'checkouts': checkouts
    }
    
    return render(request, 'pages/checkouts/checkout_list.html', context)