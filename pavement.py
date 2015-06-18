"""
Paver tasks
"""

from paver.tasks import task, needs
from paver.easy import sh


@task
def unit():
    """
    Unit tests
    """
    pass


@task
def accept():
    """
    Acceptance tests
    """
    sh('behave superlists/lists/tests/acceptance/features/')


@task
def style():
    """
    Style validation
    """
    sh('pylint superlists/')


@needs('unit', 'accept', 'style')
@task
def default():
    pass
