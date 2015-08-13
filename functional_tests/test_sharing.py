# pylint: disable=too-many-instance-attributes, invalid-name
# pylint: disable=missing-docstring

from selenium import webdriver

from .base import FunctionalTest
from .home_and_list_pages import HomePage


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
        list_page = HomePage(self).start_new_list('Get help')

        # She notices a "Share this list" option
        share_box = list_page.get_share_box()
        self.assertEqual(
            share_box.get_attribute('placeholder'),
            'your-friend@example.com'
        )

        # She shares her list
        # The page updates to say that it's shared with John
        list_page.share_list_with('john@example.com')

        # John now goes to the list page with his browser
        self.browser = john_browser
        HomePage(self).go_to_home_page().go_to_my_lists_page()

        # He sees Edith's list in there
        self.browser.find_element_by_link_text('Get help').click()

        # On the list page, John can see says that it's Edith's list
        self.wait_for(lambda: self.assertEqual(
            list_page.get_list_owner(),
            'edith@example.com'
        ))

        # He adds an item to the list
        list_page.add_new_item('Hi Edith!')

        # When Edith refreshes the page, she sees John addition
        self.browser = edith_browser
        self.browser.refresh()
        list_page.wait_for_new_item_in_list('Hi Edith!', 2)