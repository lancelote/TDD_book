# Turn off (too-many-instance-attributes), (invalid-name) and
# (missing-docstring) pylint errors:
# pylint: disable=R0902,C0103,C0111

"""
Unit tests
"""

from django.test import TestCase


class SmokeTest(TestCase):

    def test_bad_math(self):
        self.assertEqual(1 + 1, 3)
