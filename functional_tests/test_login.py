# pylint: disable=too-many-instance-attributes, invalid-name
# pylint: disable=missing-docstring

from selenium.webdriver.support.ui import WebDriverWait

from .base import FunctionalTest

TEST_EMAIL = 'edith@mockmyid.com'


class LoginTest(FunctionalTest):

    def wait_for_element_with_id(self, element_id):
        WebDriverWait(self.browser, timeout=30).until(
            lambda b: b.find_element_by_id(element_id),
            'Could not find element with id {}. Page text was:\n{}'.format(
                element_id, self.browser.find_element_by_tag_name('body').text
            )
        )

    def wait_to_be_logged_in(self, email):
        self.wait_for_element_with_id('id_logout')
        navbar = self.browser.find_element_by_css_selector('.navbar')
        self.assertIn(email, navbar.text)

    def wait_to_be_logged_out(self, email):
        self.wait_for_element_with_id('id_login')
        navbar = self.browser.find_element_by_css_selector('.navbar')
        self.assertNotIn(email, navbar.text)

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
        ).send_keys(TEST_EMAIL)
        self.browser.find_element_by_tag_name('button').click()

        # The Persona window closes
        self.switch_to_new_window(self.browser, 'To-Do')

        # She can see that she is logged in
        self.wait_to_be_logged_in(email=TEST_EMAIL)

        # Refreshing the page, she sees it's a real session login,
        # not just a one-off for that page
        self.browser.refresh()
        self.wait_to_be_logged_in(email=TEST_EMAIL)

        # She clicks "logout"
        self.browser.find_element_by_id('id_logout').click()
        self.wait_to_be_logged_out(email=TEST_EMAIL)

        # The "logged out" status also persists after refresh
        self.browser.refresh()
        self.wait_to_be_logged_out(email=TEST_EMAIL)
