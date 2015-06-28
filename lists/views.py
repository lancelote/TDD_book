"""
App views
"""

from django.shortcuts import redirect, render

from .models import Item


def homepage(request):
    """
    Returns homepage
    """
    if request.method == 'POST':
        Item.objects.create(text=request.POST['item_text'])
        return redirect('/')

    items = Item.objects.all()
    return render(request, 'lists/home.html', {'items': items})
