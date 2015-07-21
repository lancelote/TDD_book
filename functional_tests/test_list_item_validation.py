# pylint: disable=too-many-instance-attributes, invalid-name, no-member
# pylint: disable=missing-docstring

from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions
from selenium.webdriver.support.ui import WebDriverWait

from .base import FunctionalTest


class ItemValidationTest(FunctionalTest):

    def test_cannot_add_empty_list_items(self):
        # Edith goes to the home page and accidentally tries to submit
        # an empty list item. She hits Enter on the empty input box
        self.browser.get(self.server_url)
        self.get_item_input_box().send_keys('\n')

        # The home page refreshes and there is an error message saying
        # that list items cannot be blank
        error = WebDriverWait(self.browser, 5).until(
            expected_conditions.presence_of_element_located(
                (By.CSS_SELECTOR, '.has-error')
            )
        )
        # error = self.browser.find_element_by_css_selector('.has-error')
        self.assertEqual(error.text, 'You cannot have an empty list item!')

        # She tries again with some text for the item which now works
        self.get_item_input_box().send_keys('Buy milk\n')
        self.check_for_row_in_list_table('1: Buy milk')

        # Perversely she now decides to submit a second blank list item
        self.get_item_input_box().send_keys('\n')

        # She receives a similar warning on the list page
        self.check_for_row_in_list_table('1: Buy milk')
        error = WebDriverWait(self.browser, 5).until(
            expected_conditions.presence_of_element_located(
                (By.CSS_SELECTOR, '.has-error')
            )
        )
        self.assertEqual(error.text, 'You cannot have an empty list item!')

        # And she can corrects it by filling soe text in
        self.get_item_input_box().send_keys('Make tea\n')
        self.check_for_row_in_list_table('1: Buy milk')
        self.check_for_row_in_list_table('2: Make tea')
