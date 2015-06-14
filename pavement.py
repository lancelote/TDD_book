"""
Paver tasks
"""

from paver.tasks import task, needs
from paver.easy import sh


@task
def superlists():
    # Acceptance tests
    sh('behave superlists/tests/acceptance/features/')


@needs('superlists')
@task
def default():
    pass
