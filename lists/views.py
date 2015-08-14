# pylint: disable=invalid-name

"""
Lists views
"""

from django.contrib.auth import get_user_model
from django.shortcuts import redirect, render
from django.views.generic import FormView, CreateView

from lists.forms import ExistingListItemForm, ItemForm, NewListForm
from lists.models import List

User = get_user_model()


class HomePageView(FormView):
    """
    Homepage view
    """

    template_name = 'home.html'
    form_class = ItemForm


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
    Creates a new list
    """
    form = NewListForm(data=request.POST)
    if form.is_valid():
        lst = form.save(owner=request.user)
        return redirect(lst)
    return render(request, 'home.html', {'form': form})


def my_lists(request, email):
    """
    Render page with all user lists
    """
    owner = User.objects.get(email=email)
    return render(request, 'my_lists.html', {'owner': owner})


def share(request, list_id):
    """
    Add new 'Shared with' user to the given list
    """
    lst = List.objects.get(id=list_id)
    lst.shared_with.add(request.POST['email'])
    return redirect(lst)
