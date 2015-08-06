# pylint: disable=invalid-name

"""
Custom command to create a user session for functional tests
"""

from django.conf import settings
from django.contrib.auth import (
    BACKEND_SESSION_KEY, get_user_model, SESSION_KEY
)
from django.contrib.sessions.backends.db import SessionStore
from django.core.management.base import BaseCommand

User = get_user_model()


class Command(BaseCommand):
    """
    Custom manage.py commands
    """

    def add_arguments(self, parser):
        """
        Parse command arguments
        """
        parser.add_argument('email')

    def handle(self, *args, **options):
        """
        Creates a new session and returns it's key to stdout
        """
        email = options['email']
        session_key = create_pre_authenticated_session(email)
        self.stdout.write(session_key)


def create_pre_authenticated_session(email):
    """
    Creates fixture-like session to pass by authentication system
    """
    user = User.objects.create(email=email)
    session = SessionStore()
    session[SESSION_KEY] = user.pk
    session[BACKEND_SESSION_KEY] = settings.AUTHENTICATION_BACKENDS[0]
    session.save()
    return session.session_key
