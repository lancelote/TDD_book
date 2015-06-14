"""
SetUp environment for BDD tests
"""
from behave import use_step_matcher
from selenium import webdriver

# Select default step matcher, possible variants are: ['re', 'parse', 'cfparse']
use_step_matcher('parse')


# Open browser before testing
def before_scenario(context, _):
    context.browser = webdriver.Firefox()


# Close browser after testing
def after_scenario(context, _):
    context.browser.implicitly_wait(100)
    context.browser.quit()
