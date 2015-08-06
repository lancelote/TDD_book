# pylint: disable=too-many-instance-attributes, invalid-name
# pylint: disable=missing-docstring

from django.conf import settings
from django.contrib.auth import (
    get_user_model,
)

from .base import FunctionalTest
from .server_tools import create_session_on_server
from .management.commands.create_session import (
    create_pre_authenticated_session
)

User = get_user_model()


class MyListsTest(FunctionalTest):

    def create_pre_authenticated_session(self, email):
        if self.against_staging:
            session_key = create_session_on_server(
                self.server_host, email
            )
        else:
            session_key = create_pre_authenticated_session(email)

        # To set a coockie we need first visit the domain
        # 404 page will load quickest
        self.browser.get(self.server_url + '/404_no_such_url/')
        self.browser.add_cookie(dict(
            name=settings.SESSION_COOKIE_NAME,
            value=session_key,
            path='/',
        ))

    def test_logged_in_users_lists_are_saved_as_my_lists(self):
        email = 'edith@mockmyid.com'
        self.browser.get(self.server_url)
        self.wait_to_be_logged_out(email)

        # Edith is a logged-in user
        self.create_pre_authenticated_session(email)
        self.browser.get(self.server_url)
        self.wait_to_be_logged_in(email)
