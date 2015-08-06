# pylint: disable=too-many-instance-attributes, invalid-name
# pylint: disable=missing-docstring

from django.conf import settings
from django.contrib.auth import (
    BACKEND_SESSION_KEY,
    get_user_model,
    SESSION_KEY
)
from django.contrib.sessions.backends.db import SessionStore

from .base import FunctionalTest

User = get_user_model()


class MyListsTest(FunctionalTest):

    def create_ore_authenticated_session(self, email):
        user = User.objects.create(email=email)
        session = SessionStore()
        session[SESSION_KEY] = user.pk
        session[BACKEND_SESSION_KEY] = settings.AUTHENTICATION_BACKENDS[0]
        session.save()

        # To set a coockie we need first visit the domain
        # 404 page will load quickest
        self.browser.get(self.server_url + '/404_no_such_url/')
        self.browser.add_cookie(dict(
            name=settings.SESSION_COOKIE_NAME,
            value=session.session_key,
            path='/',
        ))

    # def test_logged_in_users_lists_are_saved_as_my_lists(self):
    #     email = 'edith@mockmyid.com'
    #     self.browser.get(self.server_url)
    #     self.wait_to_be_logged_out(self.browser, email)
    #
    #     # Edith is a logged-in user
    #     self.create_ore_authenticated_session(email)
    #     self.browser.get(self.server_url)
    #     self.wait_to_be_logged_in(self.browser, email)
