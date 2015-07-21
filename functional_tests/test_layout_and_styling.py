# pylint: disable=too-many-instance-attributes, invalid-name, no-member
# pylint: disable=missing-docstring

from .base import FunctionalTest


class LayoutAndStylingTest(FunctionalTest):

    def test_layout_and_style(self):
        # Edith has heard about a cool new online to-do app. She goes
        # to check out its homepage
        self.browser.get(self.server_url)
        self.browser.set_window_size(1024, 768)

        # She noticed the input box is nicely centered
        input_box = self.get_item_input_box()
        self.assertAlmostEqual(
            input_box.location['x'] + input_box.size['width']/2,
            512,
            delta=5
        )

        # She started a new list and sees the input is nicely centered too
        input_box.send_keys('testing\n')
        input_box = self.get_item_input_box()
        self.assertAlmostEqual(
            input_box.location['x'] + input_box.size['width']/2,
            512,
            delta=5
        )
