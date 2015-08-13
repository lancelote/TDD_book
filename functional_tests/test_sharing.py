# pylint: disable=too-many-instance-attributes, invalid-name
# pylint: disable=missing-docstring

from selenium import webdriver

from .base import FunctionalTest


def quit_if_possible(browser):
    try:
        browser.quit()
    except:
        pass


class SharingTest(FunctionalTest):

    def test_logged_in_users_lists_are_saved_as_my_lists(self):
        # Edith is logged in user
        self.create_pre_authenticated_session('edith@example.com')
        edith_browser = self.browser
        self.addCleanup(lambda: quit_if_possible(edith_browser))

        # Her friend John is also hanging out on the list site
        self.create_pre_authenticated_session('john@example.com')
        john_browser = webdriver.Firefox()
        self.addCleanup(lambda: quit_if_possible(john_browser))

        # Edith goes to the home page and starts a list
        self.browser = edith_browser
        self.browser.get(self.server_url)
        self.get_item_input_box().send_keys('Get help\n')

        # She notices a "Share this list" option
        share_box = self.find_element_by_css_selector_with_delay(
            self.browser, 'input[name=email]'
        )
        self.assertEqual(
            share_box.get_attribute('placeholder'),
            'your-friend@example.com'
        )
