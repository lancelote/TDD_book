"""
Paver tasks
"""

from paver.tasks import consume_args, task, needs
from paver.easy import sh


@task
def unit():
    """
    Unit tests
    """
    sh('python manage.py test lists')


@task
@consume_args
def accept(args):
    """
    Acceptance tests
    """
    sh('python manage.py test functional_tests {0}'.format(', '.join(args)))


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
