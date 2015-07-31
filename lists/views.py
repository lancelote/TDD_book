"""
App views
"""

from django.shortcuts import redirect, render

from lists.forms import ExistingListItemForm, ItemForm
from lists.models import List


def homepage(request):
    """
    Returns homepage
    """
    return render(request, 'home.html', {'form': ItemForm()})


def view_list(request, list_id):
    """
    Returns list of To-Do items
    """
    lst = List.objects.get(id=list_id)
    form = ExistingListItemForm(for_list=lst)
    if request.method == 'POST':
        form = ExistingListItemForm(for_list=lst, data=request.POST)
        if form.is_valid():
            form.save()
            return redirect(lst)
    return render(request, 'list.html', {'list': lst, 'form': form})


def new_list(request):
    """
    Adds new list
    """
    form = ItemForm(data=request.POST)
    if form.is_valid():
        lst = List.objects.create()
        form.save(for_list=lst)
        return redirect(lst)
    else:
        return render(request, 'home.html', {'form': form})
