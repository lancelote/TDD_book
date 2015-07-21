# pylint: disable=no-member

"""
App models
"""

from django.core.urlresolvers import reverse
from django.db import models


class List(models.Model):
    """
    List of To-Do items
    """

    def get_absolute_url(self):
        """
        Redirect to specific view
        """
        return reverse('lists:view_list', args=[self.id])


class Item(models.Model):
    """
    To-Do item
    """
    text = models.TextField(default='')
    list = models.ForeignKey(List, default=None)
