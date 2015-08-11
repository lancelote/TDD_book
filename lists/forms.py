# pylint: disable=too-few-public-methods,signature-differs

"""
Lists forms
"""

from django import forms
from django.core.exceptions import ValidationError

from lists.models import Item, List

DUPLICATE_ITEM_ERROR = 'You have already got this in your list!'
EMPTY_ITEM_ERROR = 'You cannot have an empty list item!'


class ItemForm(forms.models.ModelForm):
    """
    To-Do item form
    """

    class Meta:
        """
        From parameters
        """
        model = Item
        error_messages = {
            'text': {'required': EMPTY_ITEM_ERROR}
        }
        fields = ('text',)
        widgets = {
            'text': forms.fields.TextInput(attrs={
                'placeholder': 'Enter a To-Do item',
                'class': 'form-control input-lg',
            }),
        }


class NewListForm(ItemForm):
    """
    Creates a new list
    """

    def save(self, owner):
        if owner.is_authenticated():
            return List.create_new(first_item_text=self.cleaned_data['text'], owner=owner)
        else:
            return List.create_new(first_item_text=self.cleaned_data['text'])


class ExistingListItemForm(ItemForm):
    """
    To-Do item form for an existing list
    """

    def __init__(self, for_list, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.instance.list = for_list

    def validate_unique(self):
        try:
            self.instance.validate_unique()
        except ValidationError as error:
            error.error_dict = {'text': [DUPLICATE_ITEM_ERROR]}
            self._update_errors(error)
