"""
App views
"""

from django.contrib.auth import get_user_model
from django.shortcuts import redirect, render

from lists.forms import ExistingListItemForm, ItemForm
from lists.models import List

User = get_user_model()


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
        lst = List()
        lst.owner = request.user
        lst.save()
        form.save(for_list=lst)
        return redirect(lst)
    else:
        return render(request, 'home.html', {'form': form})


def my_lists(request, email):
    owner = User.objects.get(email=email)
    return render(request, 'my_lists.html', {'owner': owner})
