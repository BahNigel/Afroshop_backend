from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponse

from products.forms import CategoryForm
from products.models import Category
from django.contrib.auth.decorators import login_required


# Category List View
@login_required
def category_list(request):
    categories = Category.objects.all()
    return render(request, 'pages/categories/category_list.html', {'categories': categories})

# Create category view
@login_required
def category_create(request):
    if request.method == 'POST':
        form = CategoryForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('category_list')
    else:
        form = CategoryForm()
    
    return render(request, 'pages/categories/category_create_edit.html', {'form': form})

# Edit category view
@login_required
def category_edit(request, pk):
    category = get_object_or_404(Category, pk=pk)
    
    if request.method == 'POST':
        form = CategoryForm(request.POST, request.FILES, instance=category)
        if form.is_valid():
            form.save()
            return redirect('category_list')
    else:
        form = CategoryForm(instance=category)
    
    return render(request, 'pages/categories/category_create_edit.html', {'form': form, 'category': category})


# Category Delete View
@login_required
def category_delete(request, pk):
    category = get_object_or_404(Category, pk=pk)
    category.delete()
    return redirect('category_list')  # Redirect to category list after deletion
