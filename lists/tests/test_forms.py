# pylint: disable=too-many-instance-attributes, invalid-name
# pylint: disable=missing-docstring

from django.test import TestCase

from lists.forms import (
    DUPLICATE_ITEM_ERROR,
    EMPTY_ITEM_ERROR,
    ExistingListItemForm,
    ItemForm
)
from lists.models import Item, List


class ItemFormTest(TestCase):

    def test_form_item_input_has_placeholder_and_css_classes(self):
        form = ItemForm()
        self.assertIn('placeholder="Enter a To-Do item"', form.as_p())
        self.assertIn('class="form-control input-lg"', form.as_p())

    def test_form_validation_for_blank_items(self):
        form = ItemForm(data={'text': ''})
        self.assertFalse(form.is_valid())
        self.assertEqual(form.errors['text'], [EMPTY_ITEM_ERROR])

    def test_form_save_handles_saving_to_a_list(self):
        lst = List.objects.create()
        form = ItemForm(data={'text': 'do me'})
        new_item = form.save(for_list=lst)
        self.assertEqual(new_item, Item.objects.first())
        self.assertEqual(new_item.text, 'do me')
        self.assertEqual(new_item.list, lst)


class ExistingListItemFormTest(TestCase):

    def test_form_renders_item_text_input(self):
        lst = List.objects.create()
        form = ExistingListItemForm(for_list=lst)
        self.assertIn('placeholder="Enter a To-Do item"', form.as_p())

    def test_form_validation_for_blank_items(self):
        lst = List.objects.create()
        form = ExistingListItemForm(for_list=lst, data={'text': ''})
        self.assertFalse(form.is_valid())
        self.assertEqual(form.errors['text'], [EMPTY_ITEM_ERROR])

    def test_form_validation_for_duplicate_items(self):
        lst = List.objects.create()
        Item.objects.create(list=lst, text='No twins!')
        form = ExistingListItemForm(for_list=lst, data={'text': 'No twins!'})
        self.assertFalse(form.is_valid())
        self.assertEqual(form.errors['text'], [DUPLICATE_ITEM_ERROR])

    def test_form_save(self):
        lst = List.objects.create()
        form = ExistingListItemForm(for_list=lst, data={'text': 'hi'})
        item = form.save()
        self.assertEqual(item, Item.objects.all()[0])
