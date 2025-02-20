from django.shortcuts import render
from django.db.models import Sum, Avg
from django.db.models.functions import TruncMonth, TruncWeek, TruncDay
from products.models import Category, Product, Checkout, Payment
from datetime import timedelta

def dashboard(request):
    # Retrieve data for charts and other details
    categories = Category.objects.all()
    products = Product.objects.all()
    checkouts = Checkout.objects.all()
    payments = Payment.objects.all()

    # Prepare data for charts
    category_count_data = {
        'labels': [category.name for category in categories],
        'values': [float(Product.objects.filter(category=category).count()) for category in categories]  # Convert to float
    }

    # Average price data using Avg aggregation
    average_price_data = {
        'labels': [category.name for category in categories],
        'values': [
            float(Product.objects.filter(category=category).aggregate(average_price=Avg('price'))['average_price'] or 0) 
            for category in categories
        ]  # Convert to float
    }

    # Best selling products data
    best_selling_products_data = {
        'labels': [product.name for product in products],
        'values': [float(product.quantity_in_stock) for product in products]  # Convert to float
    }

    # Low stock products data
    low_stock_products_data = {
        'labels': [product.name for product in products],
        'values': [float(product.quantity_in_stock) for product in products if product.quantity_in_stock < 10]  # Convert to float
    }

    # Payment growth by month, week, or day
    payment_growth_data = {
        'labels': [],
        'values': []
    }

    # Annotate by month and get the sum of payments for each month
    payment_months = Payment.objects.annotate(month=TruncMonth('created_at')).values('month').distinct().order_by('month')

    for payment_month in payment_months:
        month = payment_month['month']
        total_payment = Payment.objects.filter(created_at__month=month.month).aggregate(total=Sum('total_price'))['total'] or 0
        
        # Format the month and add it to the chart data
        payment_growth_data['labels'].append(month.strftime('%b %Y'))
        payment_growth_data['values'].append(float(total_payment))  # Convert to float

        # Check for multiple entries in the same month, then group by week or day
        payments_in_month = Payment.objects.filter(created_at__month=month.month)

        # Group by week if there are multiple entries in the same month
        for payment in payments_in_month:
            week_start_date = payment.created_at - timedelta(days=payment.created_at.weekday())
            week_end_date = week_start_date + timedelta(days=6)

            # Check if this week already exists in the data, to avoid duplicate entries
            week_label = f"Week {week_start_date.strftime('%W %Y')}"
            if week_label not in payment_growth_data['labels']:
                week_payment = payments_in_month.filter(created_at__gte=week_start_date, created_at__lte=week_end_date).aggregate(total=Sum('total_price'))['total'] or 0
                payment_growth_data['labels'].append(week_label)
                payment_growth_data['values'].append(float(week_payment))  # Convert to float

            # Optionally, group by day if needed
            day_label = payment.created_at.strftime('%d %b %Y')
            if day_label not in payment_growth_data['labels']:
                day_payment = payments_in_month.filter(created_at__date=payment.created_at.date()).aggregate(total=Sum('total_price'))['total'] or 0
                payment_growth_data['labels'].append(day_label)
                payment_growth_data['values'].append(float(day_payment))  # Convert to float

    context = {
        'categories': categories,
        'products': products,
        'checkouts': checkouts,
        'payments': payments,
        'category_count_data': category_count_data,
        'average_price_data': average_price_data,
        'best_selling_products_data': best_selling_products_data,
        'low_stock_products_data': low_stock_products_data,
        'payment_growth_data': payment_growth_data
    }

    return render(request, 'index.html', context)
