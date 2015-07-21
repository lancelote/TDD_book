"""
App forms
"""

from django import forms

from lists.models import Item

EMPTY_LIST_ERROR = 'You cannot have an empty list item'


class ItemForm(forms.models.ModelForm):

    class Meta:
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
