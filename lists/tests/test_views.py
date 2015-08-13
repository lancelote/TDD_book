# Turn off (too-many-instance-attributes), (invalid-name),
# (missing-docstring) pylint errors:
# pylint: disable=R0902,C0103,C0111, no-member

"""
Views unit tests
"""

import unittest
from unittest.mock import Mock, patch

from django.contrib.auth import get_user_model, SESSION_KEY
from django.http import HttpRequest
from django.test import TestCase
from django.utils.html import escape

from lists.forms import (
    DUPLICATE_ITEM_ERROR,
    EMPTY_ITEM_ERROR,
    ExistingListItemForm,
    ItemForm,
)
from lists.models import Item, List
from lists.views import new_list

User = get_user_model()


class HomePageTest(TestCase):

    def test_page_renders_home_template(self):
        response = self.client.get('/')
        self.assertTemplateUsed(response, 'home.html')

    def test_home_page_uses_item_form(self):
        response = self.client.get('/')
        self.assertIsInstance(response.context['form'], ItemForm)


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

    def test_can_save_a_POST_request_to_an_existing_list(self):
        _ = List.objects.create()
        correct_list = List.objects.create()

        self.client.post(
            '/lists/{0}/'.format(correct_list.id),
            data={'text': 'A new item for an existing list'}
        )

        self.assertEqual(Item.objects.count(), 1)
        new_item = Item.objects.first()
        self.assertEqual(new_item.text, 'A new item for an existing list')
        self.assertEqual(new_item.list, correct_list)

    def test_POST_redirects_to_list_view(self):
        _ = List.objects.create()
        correct_list = List.objects.create()

        response = self.client.post(
            '/lists/{0}/'.format(correct_list.id),
            data={'text': 'A new item for an existing list'}
        )

        self.assertRedirects(response, '/lists/{0}/'.format(correct_list.id))

    def post_invalid_input(self):
        lst = List.objects.create()
        return self.client.post(
            '/lists/%d/' % (lst.id,),
            data={'text': ''}
        )

    def test_for_invalid_input_nothing_saved_to_db(self):
        self.post_invalid_input()
        self.assertEqual(Item.objects.count(), 0)

    def test_for_invalid_input_renders_list_template(self):
        response = self.post_invalid_input()
        self.assertIsInstance(response.context['form'], ItemForm)

    def test_for_invalid_input_shows_error_on_page(self):
        response = self.post_invalid_input()
        self.assertContains(response, escape(EMPTY_ITEM_ERROR))

    def test_displays_item_forms(self):
        lst = List.objects.create()
        response = self.client.get('/lists/%d/' % (lst.id,))
        self.assertIsInstance(response.context['form'], ExistingListItemForm)
        self.assertContains(response, 'name="text"')

    def test_duplicate_item_validation_errors_end_up_on_list_page(self):
        lst = List.objects.create()
        _ = Item.objects.create(list=lst, text='textey')
        response = self.client.post(
            '/lists/%d/' % (lst.id,),
            data={'text': 'textey'}
        )
        expected_error = escape(DUPLICATE_ITEM_ERROR)
        self.assertContains(response, expected_error)
        self.assertTemplateUsed(response, 'list.html')
        self.assertEqual(Item.objects.all().count(), 1)


class NewListViewIntegratedTest(TestCase):

    def test_saving_a_POST_request(self):
        self.client.post(
            '/lists/new',
            data={'text': 'A new list item'}
        )

        self.assertEqual(Item.objects.count(), 1)
        new_item = Item.objects.first()
        self.assertEqual(new_item.text, 'A new list item')

    def redirects_after_POST(self):
        response = self.client.post(
            '/lists/new',
            data={'text': 'A new list item'}
        )
        new_lst = List.objects.first()

        self.assertRedirects(response, '/lists/{0}/'.format(new_lst.id))

    def test_for_invalid_input_renders_home_template(self):
        response = self.client.post('/lists/new', data={'text': ''})
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'home.html')

    def test_validation_errors_are_shown_on_home_page(self):
        response = self.client.post('/lists/new', data={'text': ''})
        self.assertContains(response, escape(EMPTY_ITEM_ERROR))

    def test_for_individual_input_passes_form_to_template(self):
        response = self.client.post('/lists/new', data={'text': ''})
        self.assertIsInstance(response.context['form'], ItemForm)

    def test_invalid_list_items_are_not_saved(self):
        self.client.post('/lists/new', data={'text': ''})
        self.assertEqual(List.objects.count(), 0)
        self.assertEqual(Item.objects.count(), 0)

    def test_list_owner_is_saved_if_user_is_authenticated(self):
        request = HttpRequest()
        request.user = User.objects.create(email='a@b.com')
        request.POST['text'] = 'new list item'
        new_list(request)
        lst = List.objects.first()
        self.assertEqual(lst.owner, request.user)


@patch('lists.views.NewListForm')
class NewListViewUnitTest(unittest.TestCase):

    def setUp(self):
        self.request = HttpRequest()
        self.request.POST['text'] = 'new list item'
        self.request.user = Mock()

    def test_passes_post_data_to_NewListForm(self, mock_new_list_form):
        new_list(self.request)
        mock_new_list_form.assert_called_once_with(data=self.request.POST)

    def test_saves_form_with_owner_if_form_is_valid(self, mock_new_list_form):
        mock_form = mock_new_list_form.return_value
        mock_form.is_valid.return_value = True
        new_list(self.request)
        mock_form.save.assert_called_once_with(owner=self.request.user)

    @patch('lists.views.render')
    def test_renders_homepage_if_form_invalid(
            self, mock_render, mock_new_list_form
    ):
        mock_form = mock_new_list_form.return_value
        mock_form.is_valid.return_value = False

        response = new_list(self.request)

        self.assertEqual(response, mock_render.return_value)
        mock_render.assert_called_once_with(
            self.request, 'home.html', {'form': mock_form}
        )

    def test_does_not_save_if_form_invalid(self, mock_new_list_form):
        mock_form = mock_new_list_form.return_value
        mock_form.is_valid.return_value = False
        new_list(self.request)
        self.assertFalse(mock_form.save.called)

    @patch('lists.views.redirect')
    def test_redirects_to_form_returned_object_if_form_valid(
            self, mock_redirect, mock_new_list_form
    ):
        mock_form = mock_new_list_form.return_value
        mock_form.is_valid.return_value = True

        response = new_list(self.request)
        self.assertEqual(response, mock_redirect.return_value)
        mock_redirect.assert_called_once_with(mock_form.save.return_value)


class LoginViewTest(TestCase):

    @patch('accounts.views.authenticate')
    def test_calls_authenticate_with_assertion_from_post(
            self, mock_authenticate
    ):
        mock_authenticate.return_value = None
        self.client.post('/accounts/login', {'assertion': 'assert this'})
        mock_authenticate.assert_called_once_with(assertion='assert this')

    @patch('accounts.views.authenticate')
    def test_returns_ok_if_user_found(self, mock_authenticate):
        user = User.objects.create(email='a@b.com')
        user.backend = ''
        mock_authenticate.return_value = user
        response = self.client.post('/accounts/login', {'assertion': 'a'})
        self.assertEqual(response.content.decode(), 'OK')

    @patch('accounts.views.authenticate')
    def test_gets_logged_in_session_if_authenticate_returns_a_user(
            self, mock_authenticate
    ):
        user = User.objects.create(email='a@b.com')
        user.backend = ''
        mock_authenticate.return_value = user
        self.client.post('/accounts/login', {'assertion': 'a'})
        self.assertEqual(self.client.session[SESSION_KEY], str(user.pk))

    @patch('accounts.views.authenticate')
    def test_does_not_get_logged_in_if_authenticate_returns_none(
            self, mock_authenticate
    ):
        mock_authenticate.return_value = None
        self.client.post('/accounts/login', {'assertion': 'a'})
        self.assertNotIn(SESSION_KEY, self.client.session)


class MyListsTest(TestCase):

    def test_my_lists_url_renders_my_lists_template(self):
        User.objects.create(email='a@b.com')
        response = self.client.get('/lists/users/a@b.com/')
        self.assertTemplateUsed(response, 'my_lists.html')

    def test_passes_correct_owner_to_template(self):
        User.objects.create(email='wrong@owner.com')
        correct_user = User.objects.create(email='a@b.com')
        response = self.client.get('/lists/users/a@b.com/')
        self.assertEqual(response.context['owner'], correct_user)


class ShareListTest(TestCase):

    def test_sharing_a_list_via_post(self):
        shared_with = User.objects.create(email='share.with@me.com')
        lst = List.objects.create()
        self.client.post(
            '/lists/%d/share' % (lst.id,),
            {'email': 'share.with@me.com'}
        )
        self.assertIn(shared_with, lst.shared_with.all())

    def test_redirects_after_post(self):
        shared_with = User.objects.create(email='share.with@me.com')
        lst = List.objects.create()
        response = self.client.post(
            '/lists/%d/share' % (lst.id,),
            {'email': shared_with.email}
        )
        self.assertRedirects(response, lst.get_absolute_url())
