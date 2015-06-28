"""
App models
"""

from django.db import models


class Item(models.Model):
    """
    To-Do item
    """
    text = models.TextField(default='')
