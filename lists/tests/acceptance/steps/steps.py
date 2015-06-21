# Turn off (function-redefined), (no-name-in-module) pylint errors:
# pylint: disable=E0611, E0102

"""
Acceptance tests
"""

from behave import when, then
from nose.tools import (
    assert_in,
    assert_equal
)
from selenium.webdriver.common.keys import Keys


@when('I open an index page')
def step_impl(context):
    """
    Get index page
    """
    context.browser.get('http://localhost:8000')


@then('I see a title says "{text}"')
def step_impl(context, text):
    """
    Check title text
    """
    assert_in(text, context.browser.title)


@then('I see header mention "{text}" lists')
def step_impl(context, text):
    """
    Check page header
    """
    header_text = context.browser.find_element_by_tag_name('h1').text
    assert_in(text, header_text)


@then('I am invited to enter a To-Do item')
def step_impl(context):
    """
    Check if there is a input box to enter new To-Do item
    """
    context.input_box = context.browser.find_element_by_id('id_new_item')
    assert_equal(
        context.input_box.get_attribute('placeholder'),
        'Enter a To-Do item'
    )


@then('I enter "{text}" into a text box')
def step_impl(context, text):
    """
    Input text to input_box
    """
    context.input_box.send_keys(text)


@when('I hit enter')
def step_impl(context):
    """
    Send input_box content to server
    """
    context.input_box.send_keys(Keys.ENTER)


@then('Page updates and now it lists "{text}"')
def step_impl(context, text):
    """
    Check if the page show new To-Do item
    """
    table = context.browser.find_element_by_id('id_list_table')
    rows = table.find_elements_by_tag_name('tr')
    assert_in(text, [row.text for row in rows])
