# Turn off (too-many-instance-attributes), (invalid-name),
# (missing-docstring) and (no-member) pylint errors:
# pylint: disable=R0902,C0103,C0111,E1101

"""
Unit tests
"""

from django.core.urlresolvers import resolve
from django.http import HttpRequest
from django.template.loader import render_to_string
from django.test import TestCase

from lists.models import Item, List
from lists.views import homepage


class HomePageTest(TestCase):

    def test_root_url_resolves_to_home_page_view(self):
        found = resolve('/')
        self.assertEqual(found.func, homepage)

    def test_home_page_returns_correct_html(self):
        request = HttpRequest()
        response = homepage(request)
        expected_html = render_to_string('home.html')
        self.assertEqual(response.content.decode(), expected_html)


class ListAndItemModelTest(TestCase):

    def test_saving_and_retrieving_items(self):
        lst = List()
        lst.save()

        first_item = Item()
        first_item.text = 'The first (ever) list item'
        first_item.list = lst
        first_item.save()

        second_item = Item()
        second_item.text = 'Item the second'
        second_item.list = lst
        second_item.save()

        saved_list = List.objects.first()
        self.assertEqual(saved_list, lst)

        saved_items = Item.objects.all()
        self.assertEqual(saved_items.count(), 2)

        first_saved_item = saved_items[0]
        second_saved_item = saved_items[1]
        self.assertEqual(first_saved_item.text, 'The first (ever) list item')
        self.assertEqual(first_saved_item.list, lst)
        self.assertEqual(second_saved_item.text, 'Item the second')
        self.assertEqual(second_saved_item.list, lst)


class ListViewTest(TestCase):

    def test_uses_list_template(self):
        lst = List.objects.create()
        response = self.client.get('/lists/{0}/'.format(lst.id))
        self.assertTemplateUsed(response, 'list.html')

    def test_displays_only_items_for_that_list(self):
        correct_list = List.objects.create()
        Item.objects.create(text='Item 1', list=correct_list)
        Item.objects.create(text='Item 2', list=correct_list)
        another_list = List.objects.create()
        Item.objects.create(text='Another Item 1', list=another_list)
        Item.objects.create(text='Another Item 2', list=another_list)

        response = self.client.get('/lists/{0}/'.format(correct_list.id))

        self.assertContains(response, 'Item 1')
        self.assertContains(response, 'Item 2')
        self.assertNotContains(response, 'Another Item 1')
        self.assertNotContains(response, 'Another Item 2')

    def test_passes_correct_list_to_template(self):
        _ = List.objects.create()
        correct_list = List.objects.create()

        response = self.client.get('/lists/{0}/'.format(correct_list.id))

        self.assertEqual(response.context['list'], correct_list)


class NewListTest(TestCase):

    def test_saving_a_POST_request(self):
        self.client.post(
            '/lists/new',
            data={'item_text': 'A new list item'}
        )

        self.assertEqual(Item.objects.count(), 1)
        new_item = Item.objects.first()
        self.assertEqual(new_item.text, 'A new list item')

    def redirects_after_POST(self):
        response = self.client.post(
            '/lists/new',
            data={'item_text': 'A new list item'}
        )
        new_list = List.objects.first()

        self.assertRedirects(response, '/lists/{0}/'.format(new_list.id))


class NewItemTest(TestCase):

    def test_can_save_a_POST_request_to_an_existing_list(self):
        _ = List.objects.create()
        correct_list = List.objects.create()

        self.client.post(
            '/lists/{0}/add_item'.format(correct_list.id),
            data={'item_text': 'A new item for an existing list'}
        )

        self.assertEqual(Item.objects.count(), 1)
        new_item = Item.objects.first()
        self.assertEqual(new_item.text, 'A new item for an existing list')
        self.assertEqual(new_item.list, correct_list)

    def test_redirects_to_list_view(self):
        _ = List.objects.create()
        correct_list = List.objects.create()

        response = self.client.post(
            '/lists/{0}/add_item'.format(correct_list.id),
            data={'item_text': 'A new item for an existing list'}
        )

        self.assertRedirects(response, '/lists/{0}/'.format(correct_list.id))