# Turn off (function-redefined), (no-name-in-module) pylint errors:
# pylint: disable=E0611, E0102

"""
Acceptance tests
"""

from behave import when, then
from selenium import webdriver


@when('I check index page')
def step_impl(context):
    """
    Get index page
    """
    context.browser = webdriver.Firefox()
    context.browser.get('http://localhost:8000')


@then('I see a title "{text}"')
def step_impl(context, text):
    """
    Compare captured output to given string
    """
    assert 'Django' in context.browser.title
