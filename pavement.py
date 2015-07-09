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
    sh('python manage.py test lists')


@task
def accept():
    """
    Acceptance tests
    """
    sh('python manage.py test functional_tests')


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
