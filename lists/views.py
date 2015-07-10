"""
App views
"""

from django.shortcuts import redirect, render

from .models import Item, List


def homepage(request):
    """
    Returns homepage
    """
    return render(request, 'home.html')


def view_list(request, list_id):
    """
    Returns list of To-Do items
    """
    items = Item.objects.all()
    return render(request, 'list.html', {'items': items})


def new_list(request):
    """
    Adds new list
    """
    lst = List.objects.create()
    Item.objects.create(text=request.POST['item_text'], list=lst)
    return redirect('/lists/the-only-list-in-the-world/')
