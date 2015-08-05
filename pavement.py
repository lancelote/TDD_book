"""
Paver tasks
"""

from paver.tasks import consume_args, task
from paver.easy import call_task, sh


@task
def unit():
    """
    Unit tests
    """
    sh('python manage.py test lists.tests accounts.tests')


@task
@consume_args
def accept(args):
    """
    Acceptance tests
    """
    sh('python manage.py test functional_tests %s' % (', '.join(args),))


@task
def style():
    """
    Style validation
    """
    # ToDo : add deploy folder
    # ToDo : add test coverage
    sh('pylint lists/ superlists/ accounts/ functional_tests/')


@task
def default():
    call_task('unit')
    call_task('accept', args=[''])
    call_task('style')
