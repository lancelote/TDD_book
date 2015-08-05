# pylint: disable=invalid-name, too-few-public-methods

"""
Authentication logic
"""

import requests

from django.contrib.auth import get_user_model

User = get_user_model()

PERSONA_VERIFY_URL = 'https://verifier.login.persona.org/verify'
DOMAIN = 'localhost'


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
            data={'assertion': assertion, 'audience': DOMAIN}
        )
        if response.ok and response.json()['status'] == 'okay':
            email = response.json()['email']
            try:
                return User.objects.get(email=email)
            except User.DoesNotExist:
                return User.objects.create(email=email)

    @staticmethod
    def get_user(email):
        """
        Get user by email else None
        """
        try:
            return User.objects.get(email=email)
        except User.DoesNotExist:
            return None