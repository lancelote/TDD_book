# Turn off (too-many-instance-attributes), (invalid-name) and
# (missing-docstring) pylint errors:
# pylint: disable=R0902,C0103,C0111

"""
Unit tests
"""

from django.core.urlresolvers import resolve
from django.test import TestCase
from lists.views import homepage


class HomePageTest(TestCase):

    def test_root_url_resolves_to_home_page_view(self):
        found = resolve('/')
        self.assertEqual(found.func, homepage)
