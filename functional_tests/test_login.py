# pylint: disable=too-many-instance-attributes, invalid-name
# pylint: disable=missing-docstring

from .base import FunctionalTest


class LoginTest(FunctionalTest):

    def test_login_with_persona(self):
        # Edith goes to the awesome superlists site
        # and notices a "Sign in" link for the first time
        self.browser.get(self.server_url)
        self.browser.find_element_by_id('id_login').click()

        # A persona login box appears
        self.switch_to_new_window(self.browser, 'Mozilla Persona')

        # Edith logins with her email address
        self.browser.find_element_by_id(
            'authentication_email'
        ).send_keys('edith@mockmyid.com')
        self.browser.find_element_by_tag_name('button').click()

        # The Persona window closes
        self.switch_to_new_window(self.browser, 'To-Do')

        # She can see that she is logged in
        self.wait_for_element_with_id(self.browser, 'id_logout')
        navbar = self.find_element_by_css_selector_with_delay(
            self.browser, '.navbar'
        )
        self.assertIn('edith@mockmyid.com', navbar.text)
