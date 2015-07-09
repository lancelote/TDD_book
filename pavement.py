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
    sh('python manage.py test')


@task
def accept():
    """
    Acceptance tests
    """
    sh('python functional_tests.py')


@task
def style():
    """
    Style validation
    """
    sh('pylint lists/ superlists/')


@needs('unit', 'accept', 'style')
@task
def default():
    pass
