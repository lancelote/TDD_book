# pylint: disable=too-many-instance-attributes, invalid-name
# pylint: disable=missing-docstring

from .base import FunctionalTest


class ItemValidationTest(FunctionalTest):

    def test_cannot_add_empty_list_items(self):
        # Edith goes to the home page and accidentally tries to submit
        # an empty list item. She hits Enter on the empty input box
        self.browser.get(self.server_url)
        self.get_item_input_box().send_keys('\n')

        # The home page refreshes and there is an error message saying
        # that list items cannot be blank
        error = self.find_element_by_css_selector_with_delay(
            self.browser, '.has-error'
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
        error = self.find_element_by_css_selector_with_delay(
            self.browser, '.has-error'
        )
        self.assertEqual(error.text, 'You cannot have an empty list item!')

        # And she can corrects it by filling soe text in
        self.get_item_input_box().send_keys('Make tea\n')
        self.check_for_row_in_list_table('1: Buy milk')
        self.check_for_row_in_list_table('2: Make tea')

    def test_cannot_add_duplicate_items(self):
        # Edith goes to the homepage and starts a new list
        self.browser.get(self.server_url)
        self.get_item_input_box().send_keys('Buy wellies\n')
        self.check_for_row_in_list_table('1: Buy wellies')

        # She accidentally tries to enter a duplicate item
        self.get_item_input_box().send_keys('Buy wellies\n')

        # She sees a helpful error message
        self.check_for_row_in_list_table('1: Buy wellies')
        error = self.find_element_by_css_selector_with_delay(
            self.browser, '.has-error'
        )
        self.assertEqual(error.text, 'You have already got this in your list!')

    def test_error_message_are_cleared_on_input(self):
        # Edith starts a new list in a way that causes a validation error
        self.browser.get(self.server_url)
        self.get_item_input_box().send_keys('\n')
        error = self.find_element_by_css_selector_with_delay(
            self.browser, '.has-error'
        )
        self.assertTrue(error.is_displayed())

        # She starts typing in the input box to clear the error
        self.get_item_input_box().send_keys('a')

        # She is pleased to see that the error message disappears
        error = self.find_element_by_css_selector_with_delay(
            self.browser, '.has-error'
        )
        self.assertFalse(error.is_displayed())
