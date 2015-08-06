# pylint: disable=invalid-name, too-few-public-methods

"""
Authentication logic
"""

import requests

from django.conf import settings
from django.contrib.auth import get_user_model

import logging

# Setup logger
logger = logging.getLogger(__name__)

# Setup user model
User = get_user_model()

PERSONA_VERIFY_URL = 'https://verifier.login.persona.org/verify'


class PersonaAuthenticationBackend(object):
    """
    Custom authentication backend for Mozilla Persona
    """

    @staticmethod
    def authenticate(assertion):
        """
        Send assertion to Persona verifier server and check the response

        :return: User object
        """
        response = requests.post(
            PERSONA_VERIFY_URL,
            data={'assertion': assertion, 'audience': settings.DOMAIN}
        )
        if response.ok and response.json()['status'] == 'okay':
            email = response.json()['email']
            try:
                return User.objects.get(email=email)
            except User.DoesNotExist:
                return User.objects.create(email=email)
        else:
            logger.warning(
                'Persona says no. Json was: {}'.format(response.json())
            )

    @staticmethod
    def get_user(email):
        """
        Get user by email else None
        """
        try:
            return User.objects.get(email=email)
        except User.DoesNotExist:
            return None
