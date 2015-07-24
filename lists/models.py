# pylint: disable=too-few-public-methods, no-member

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

    class Meta:
        """
        Model parameters
        """
        ordering = ('id',)
        unique_together = ('list', 'text',)

    def __str__(self):
        return self.text
