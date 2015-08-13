# Turn off (too-many-instance-attributes), (invalid-name),
# (missing-docstring) pylint errors:
# pylint: disable=R0902,C0103,C0111

"""
Models unit tests
"""

from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError
from django.test import TestCase

from lists.models import Item, List

User = get_user_model()


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

    def test_create_new_creates_list_and_first_item(self):
        List.create_new(first_item_text='new item text')
        new_item = Item.objects.first()
        self.assertEqual(new_item.text, 'new item text')
        new_list = List.objects.first()
        self.assertEqual(new_item.list, new_list)

    def test_create_new_optionally_saves_owner(self):
        user = User.objects.create()
        List.create_new(first_item_text='new item text', owner=user)
        new_list = List.objects.first()
        self.assertEqual(new_list.owner, user)

    def test_lists_can_have_owner(self):
        try:
            List(owner=User())
        except TypeError:
            self.fail('Cannot asign an owner to a list!')

    @staticmethod
    def test_list_owner_is_optional():
        List().full_clean()

    def test_create_returns_new_list_object(self):
        returned = List.create_new(first_item_text='new item text')
        new_list = List.objects.first()
        self.assertEqual(returned, new_list)

    def test_list_name_is_first_item_text(self):
        lst = List.objects.create()
        Item.objects.create(list=lst, text='first item')
        Item.objects.create(list=lst, text='second item')
        self.assertEqual(lst.name, 'first item')

    def test_can_share_with_another_user(self):
        lst = List.objects.create()
        user = User.objects.create(email='a@b.com')
        lst.shared_with.add('a@b.com')
        list_in_db = List.objects.get(id=lst.id)
        self.assertIn(user, list_in_db.shared_with.all())
