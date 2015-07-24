# Turn off (too-many-instance-attributes), (invalid-name),
# (missing-docstring) pylint errors:
# pylint: disable=R0902,C0103,C0111

"""
Models unit tests
"""

from django.core.exceptions import ValidationError
from django.test import TestCase

from lists.models import Item, List


class ItemModelTest(TestCase):

    def test_default_text(self):
        item = Item()
        self.assertEqual(item.text, '')

    def test_item_is_related_to_list(self):
        lst = List.objects.create()
        item = Item()
        item.list = lst
        item.save()
        self.assertIn(item, lst.item_set.all())

    def test_cannot_save_empty_list_items(self):
        lst = List.objects.create()
        item = Item.objects.create(list=lst, text='')
        with self.assertRaises(ValidationError):
            item.save()
            item.full_clean()

    def test_duplicate_items_are_invalid(self):
        lst = List.objects.create()
        Item.objects.create(list=lst, text='bla')
        with self.assertRaises(ValidationError):
            item = Item(list=lst, text='bla')
            item.full_clean()

    def test_same_items_can_be_saved_to_different_lists(self):
        list1 = List.objects.create()
        list2 = List.objects.create()
        Item.objects.create(list=list1, text='bla')
        item = Item(list=list2, text='bla')
        try:
            item.full_clean()
        except ValidationError:
            self.fail('Cannot save same item to two different lists')

    def test_list_ordering(self):
        lst = List.objects.create()
        item1 = Item.objects.create(list=lst, text='Item 1')
        item2 = Item.objects.create(list=lst, text='Item 2')
        item3 = Item.objects.create(list=lst, text='Item 3')
        self.assertEqual(
            list(Item.objects.all()),
            [item1, item2, item3]
        )

    def test_string_representation(self):
        item = Item(text='Some text')
        self.assertEqual(str(item), 'Some text')


class ListModelTest(TestCase):

    def test_get_absolute_url(self):
        lst = List.objects.create()
        self.assertEqual(lst.get_absolute_url(), '/lists/%d/' % (lst.id,))
