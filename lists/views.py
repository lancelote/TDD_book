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
    lst = List.objects.get(id=list_id)
    return render(request, 'list.html', {'list': lst})


def new_list(request):
    """
    Adds new list
    """
    lst = List.objects.create()
    Item.objects.create(text=request.POST['item_text'], list=lst)
    return redirect('/lists/{0}/'.format(lst.id))


def add_item(request, list_id):
    """
    Adds new item to a existing list
    """
    lst = List.objects.get(id=list_id)
    Item.objects.create(text=request.POST['item_text'], list=lst)
    return redirect('/lists/{0}/'.format(lst.id))
