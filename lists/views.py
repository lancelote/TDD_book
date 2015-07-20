"""
App views
"""

from django.core.exceptions import ValidationError
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
    lst = List.objects.get(id=list_id)
    return render(request, 'list.html', {'list': lst})


def new_list(request):
    """
    Adds new list
    """
    lst = List.objects.create()
    item = Item(text=request.POST['item_text'], list=lst)
    try:
        item.full_clean()
        item.save()
    except ValidationError:
        lst.delete()
        error = 'You cannot have an empty list item!'
        return render(request, 'home.html', {'error': error})
    return redirect('/lists/{0}/'.format(lst.id))


def add_item(request, list_id):
    """
    Adds new item to a existing list
    """
    lst = List.objects.get(id=list_id)
    Item.objects.create(text=request.POST['item_text'], list=lst)
    return redirect('/lists/{0}/'.format(lst.id))
