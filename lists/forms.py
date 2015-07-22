# pylint: disable=too-few-public-methods,signature-differs

"""
App forms
"""

from django import forms

from lists.models import Item

EMPTY_LIST_ERROR = 'You cannot have an empty list item!'


class ItemForm(forms.models.ModelForm):
    """
    To-Do item form
    """

    def save(self, for_list):
        self.instance.list = for_list
        return super().save()

    class Meta:
        """
        From parameters
        """
        model = Item
        error_messages = {
            'text': {'required': EMPTY_LIST_ERROR}
        }
        fields = ('text',)
        widgets = {
            'text': forms.fields.TextInput(attrs={
                'placeholder': 'Enter a To-Do item',
                'class': 'form-control input-lg',
            }),
        }
