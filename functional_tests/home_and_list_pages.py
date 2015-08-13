# pylint: disable=missing-docstring

ITEM_INPUT_ID = 'id_text'


class HomePage(object):

    def __init__(self, test):
        self.test = test

    def go_to_home_page(self):
        """
        Go to homepage and wait for it to load
        """
        self.test.browser.get(self.test.server_url)
        self.test.wait_for(self.get_item_input)
        return self

    def get_item_input(self):
        """
        Get item inputbox
        """
        return self.test.browser.find_element_by_id(ITEM_INPUT_ID)

    def start_new_list(self, item_text):
        """
        Start new list with a given first item text
        """
        self.go_to_home_page()
        inputbox = self.get_item_input()
        inputbox.send_keys(item_text + '\n')
        list_page = ListPage(self.test)
        list_page.wait_for_new_item_in_list(item_text, 1)
        return list_page

    def go_to_my_lists_page(self):
        """
        Go to user lists page
        """
        self.test.browser.find_element_by_link_text('My lists').click()
        self.test.wait_for(lambda: self.test.assertEqual(
            self.test.browser.find_element_by_tag_name('h1').text,
            'My lists'
        ))


class ListPage(object):

    def __init__(self, test):
        self.test = test

    def get_list_tables_rows(self):
        """
        Find all items of the list on the page
        """
        return self.test.browser.find_elements_by_css_selector(
            '#id_list_table tr'
        )

    def wait_for_new_item_in_list(self, item_text, position):
        """
        Wait for item to appear in the list item table

        :param position: Item position in the table
        """
        expected_row = '{}: {}'.format(position, item_text)
        self.test.wait_for(lambda: self.test.assertIn(
            expected_row,
            [row.text for row in self.get_list_tables_rows()]
        ))

    def get_share_box(self):
        """
        Get list 'Share with' inputbox
        """
        return self.test.browser.find_element_by_css_selector(
            'input[name=email]'
        )

    def get_shared_with_list(self):
        """
        Find all emails of shared with users
        """
        return self.test.browser.find_elements_by_css_selector(
            '.list-share'
        )

    def share_list_with(self, email):
        """
        Share list with given user
        """
        self.get_share_box().send_keys(email + '\n')
        self.test.wait_for(lambda: self.test.assertIn(
            email,
            [item.text for item in self.get_shared_with_list()]
        ))

    def get_item_input(self):
        """
        Get item inputbox
        """
        return self.test.browser.find_element_by_id(ITEM_INPUT_ID)

    def add_new_item(self, item_text):
        """
        Add a new item to the list
        """
        current_pos = len(self.get_list_tables_rows())
        self.get_item_input().send_keys(item_text + '\n')
        self.wait_for_new_item_in_list(item_text, current_pos + 1)

    def get_list_owner(self):
        """
        Get list owner email
        """
        return self.test.browser.find_element_by_id('id_list_owner').text
