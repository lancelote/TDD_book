"""
Accounts models
"""

from django.db import models
from django.utils import timezone


class User(models.Model):
    """
    Custom user model
    """

    email = models.EmailField(primary_key=True)
    last_login = models.DateTimeField(default=timezone.now)
    REQUIRED_FIELDS = ()
    USERNAME_FIELD = 'email'

    @staticmethod
    def is_authenticated():
        """
        Check if user is authenticated
        """
        return True
