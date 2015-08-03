# pylint: disable=too-many-instance-attributes, invalid-name
# pylint: disable=missing-docstring

import sys
import time

from django.contrib.staticfiles.testing import StaticLiveServerTestCase

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions
from selenium.webdriver.support.ui import WebDriverWait


class FunctionalTest(StaticLiveServerTestCase):

    @classmethod
    def setUpClass(cls):
        for arg in sys.argv:
            if 'liveserver' in arg:
                cls.server_url = 'http://' + arg.split('=')[1]
                return
        super().setUpClass()
        cls.server_url = cls.live_server_url

    @classmethod
    def tearDownClass(cls):
        if cls.server_url == cls.live_server_url:
            super().tearDownClass()

    def setUp(self):
        self.browser = webdriver.Firefox()
        self.browser.implicitly_wait(3)

    def tearDown(self):
        self.browser.quit()

    def check_for_row_in_list_table(self, row_text):
        table = self.browser.find_element_by_id('id_list_table')
        rows = table.find_elements_by_tag_name('tr')
        self.assertIn(row_text, [row.text for row in rows])

    def get_item_input_box(self):
        return self.browser.find_element_by_id('id_text')

    @staticmethod
    def find_element_by_css_selector_with_delay(driver, selector, delay=5):
        """
        Simple built-in method breaks travis build

        :param driver: browser driver
        :param selector: string (ex. .has-error)
        :param delay: int (delay duration)
        """
        return WebDriverWait(driver, delay).until(
            expected_conditions.presence_of_element_located(
                (By.CSS_SELECTOR, selector)
            )
        )

    @staticmethod
    def wait_for_element_with_id(driver, element_id, delay=30):
        WebDriverWait(driver, delay).until(
            expected_conditions.presence_of_element_located(
                (By.ID, element_id)
            )
        )

    def switch_to_new_window(self, driver, text_in_title):
        """
        Switch browser window
        """
        retries = 60
        while retries:
            for handle in driver.window_handles:
                driver.switch_to_window(handle)
                if text_in_title in driver.title:
                    return
            retries -= 1
            time.sleep(0.5)
        self.fail('Could not find window!')
