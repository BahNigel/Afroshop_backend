# views.py

from django.shortcuts import render
from django.db.models import Q
from products.models import Payment, Product

def payment_list(request):
    order_id_search = request.GET.get('order_id', '')  # Get the search parameter from the URL
    payments = Payment.objects.all().order_by('-created_at')  # Fetch all payments
    
    # For each payment, fetch the related product details (name and image)
    for payment in payments:
        for item in payment.items:
            try:
                product = Product.objects.get(id=item['id'])
                item['product_name'] = product.name
                item['price'] = product.price
                item['product_image'] = product.image.url if product.image else None  # Assuming the product has an image field
            except Product.DoesNotExist:
                continue

    # Apply search filter if any
    if order_id_search:
        payments = payments.filter(orderId__icontains=order_id_search)
    
    context = {
        'payments': payments,
        'order_id_search': order_id_search,  # Pass the search term to the template
    }
    
    return render(request, 'pages/payments/payment_list.html', context)
