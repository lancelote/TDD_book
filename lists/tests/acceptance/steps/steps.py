# Turn off (function-redefined), (no-name-in-module) pylint errors:
# pylint: disable=E0611, E0102

"""
Acceptance tests
"""

from behave import when, then
from nose.tools import assert_in


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
