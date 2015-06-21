# Turn off (too-many-instance-attributes), (invalid-name) and
# (missing-docstring) pylint errors:
# pylint: disable=R0902,C0103,C0111

"""
Unit tests
"""

from django.core.urlresolvers import resolve
from django.http import HttpRequest
from django.template.loader import render_to_string
from django.test import TestCase

from lists.views import homepage


class HomePageTest(TestCase):

    def test_root_url_resolves_to_home_page_view(self):
        found = resolve('/')

        self.assertEqual(found.func, homepage)

    def test_homepage_returns_correct_html(self):
        request = HttpRequest()
        response = homepage(request)
        expected_html = render_to_string('lists/home.html')

        self.assertEqual(response.content.decode(), expected_html)

    def test_homepage_can_save_a_post_request(self):
        text = 'A new list item'
        request = HttpRequest()
        request.method = 'POST'
        request.POST['item_text'] = text

        response = homepage(request)

        self.assertIn(text, response.content.decode())
        expected_html = render_to_string(
            'lists/home.html',
            {'new_item_text': 'A new list item'}
        )
        self.assertEqual(response.content.decode(), expected_html)
