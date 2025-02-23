from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.db.models import Avg, Case, When, FloatField
from products.forms import ProductForm
from products.models import Product, ProductRating, RelatedProductImages
from django.contrib.auth.decorators import login_required


@login_required
def product_list(request):
    products = Product.objects.annotate(
        avg_rating=Avg('ratings__rating'),
        final_rating=Case(
            When(ratings__Admin_rating__isnull=False, then=Avg('ratings__Admin_rating')),
            default=Avg('ratings__rating'),
            output_field=FloatField()
        )
    )

    product_type = request.GET.get('type', None)
    if product_type:
        products = products.filter(type=product_type)

    product_types = Product.TYPE_CHOICES

    return render(request, 'pages/products/product_list.html', {
        'products': products,
        'product_types': product_types,
        'product_type': product_type,
    })


@login_required
def product_create_or_edit(request, pk=None):
    if pk:
        product = get_object_or_404(Product, pk=pk)
        ratings = product.ratings.aggregate(
            avg_rating=Avg('rating'),
            admin_rating=Avg('Admin_rating')
        )
        avg_rating = ratings['avg_rating'] or 0
        admin_rating = ratings['admin_rating'] if ratings['admin_rating'] else None
    else:
        product = None
        avg_rating = None
        admin_rating = None

    if request.method == 'POST':
        form = ProductForm(request.POST, request.FILES, instance=product)
        admin_rating_value = request.POST.get('admin_rating', None)
        related_images = request.FILES.getlist('related_images')
        delete_images = request.POST.getlist('delete_images')

        if form.is_valid():
            # Save or update the product
            product = form.save()

            # Handle deletion of related images
            if delete_images:
                RelatedProductImages.objects.filter(id__in=delete_images).delete()

            # Save new related images
            for image in related_images:
                RelatedProductImages.objects.create(product=product, image=image)

            # If admin_rating is set, update all product ratings with this value
            if admin_rating_value:
                rating, created = ProductRating.objects.update_or_create(
                    product=product,
                    defaults={
                        'Admin_rating': admin_rating_value,
                        'rating': 1
                    }
                )

            messages.success(request, 'Product updated successfully!' if pk else 'Product created successfully!')
            return redirect('product_list')
    else:
        form = ProductForm(instance=product)

    related_images = RelatedProductImages.objects.filter(product=product) if product else []

    action = 'Edit' if pk else 'Create'

    return render(request, 'pages/products/product_create_or_edit.html', {
        'form': form,
        'action': action,
        'product': product,
        'avg_rating': avg_rating,
        'admin_rating': admin_rating,
        'related_images': related_images,
    })

@login_required
def product_delete(request, pk):
    product = get_object_or_404(Product, pk=pk)
    product.delete()
    messages.success(request, 'Product deleted successfully!')
    return redirect('product_list')
