"""
App models
"""

from django.db import models


class List(models.Model):
    """
    List of To-Do items
    """
    pass


class Item(models.Model):
    """
    To-Do item
    """
    text = models.TextField(default='')
    list = models.ForeignKey(List, default=None)
