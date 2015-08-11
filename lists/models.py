# pylint: disable=too-few-public-methods, no-member

"""
App models
"""

from django.conf import settings
from django.core.urlresolvers import reverse
from django.db import models


class List(models.Model):
    """
    List of To-Do items
    """

    owner = models.ForeignKey(settings.AUTH_USER_MODEL, blank=True, null=True)

    @property
    def name(self):
        return self.item_set.first().text

    def get_absolute_url(self):
        """
        Redirect to specific view
        """
        return reverse('lists:view_list', args=[self.id])

    @staticmethod
    def create_new(first_item_text, owner=None):
        lst = List.objects.create(owner=owner)
        Item.objects.create(text=first_item_text, list=lst)
        return lst


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
