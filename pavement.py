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


@needs('unit', 'accept')
@task
def default():
    pass
