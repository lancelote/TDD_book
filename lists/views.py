"""
App views
"""

from django.shortcuts import render


def homepage(request):
    """
    Returns homepage
    """
    return render(request, 'lists/home.html', {
        'new_item_text': request.POST.get('item_text', ''),
    })
