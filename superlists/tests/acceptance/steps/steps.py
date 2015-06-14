# Turn off (function-redefined), (no-name-in-module) pylint errors:
# pylint: disable=E0611, E0102

"""
Acceptance tests
"""

from behave import when, then
from selenium import webdriver


@when('I open an index page')
def step_impl(context):
    """
    Get index page
    """
    context.browser = webdriver.Firefox()
    context.browser.get('http://localhost:8000')


@then('I see a title says "{text}"')
def step_impl(context, text):
    """
    Compare captured output to given string
    """
    assert 'Django' in context.browser.title


@then('I close an index page')
def step_impl(context):
    """
    Close browser
    """
    context.browser.quit()
