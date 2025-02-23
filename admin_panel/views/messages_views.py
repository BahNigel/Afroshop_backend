from django.shortcuts import render
from django.db.models import Q
from products.models import ContactUs
from django.contrib.auth.decorators import login_required

@login_required
def contact_messages_list(request):
    search_query = request.GET.get('search', '')  # Get the search query from the URL
    contact_messages = ContactUs.objects.all().order_by('-created_at')  # Fetch all messages
    
    # Apply search filter if any (search by name, email, or subject)
    if search_query:
        contact_messages = contact_messages.filter(
            Q(name__icontains=search_query) |
            Q(email__icontains=search_query) |
            Q(subject__icontains=search_query) |
            Q(message__icontains=search_query)
        )

    context = {
        'contact_messages': contact_messages,  # Ensure correct variable name
        'search_query': search_query,  # Pass the search term to the template
    }

    return render(request, 'pages/messages/message_list.html', context)
