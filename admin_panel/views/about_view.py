from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required

from products.forms import AboutUsForm  # Corrected import for the AboutUsForm
from products.models import AboutUs

@login_required
def about_us_view(request):
    about_us = AboutUs.objects.first()  # Retrieve the only About Us instance
    if not about_us:
        return redirect('edit_about_us')  # Redirect to the edit page if no instance exists
    return render(request, 'pages/about/about_view.html', {'about_us': about_us})

@login_required
def about_us_edit(request):
    about_us = AboutUs.objects.first()  # Get the first About Us instance
    
    if not about_us:
        about_us = AboutUs.objects.create()  # Create a new instance if none exists
    
    if request.method == 'POST':
        form = AboutUsForm(request.POST, request.FILES, instance=about_us)
        if form.is_valid():
            form.save()
            return redirect('about_us')  # Redirect to the About Us view page after saving
    else:
        form = AboutUsForm(instance=about_us)
    
    return render(request, 'pages/about/about_create_edit.html', {'form': form})
