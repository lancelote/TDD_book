"""
Server tools to used by functional tests
"""

import subprocess
from os import path

THIS_FOLDER = path.abspath(path.dirname(__file__))


def create_session_on_server(host, email):
    """
    Run fabric to create user session on server
    """
    return subprocess.check_output(
        [
            'fab',
            'create_session_on_server:email=%s' % (email,),
            '--host=%s' % (host,),
            '--hide=everything,status',
        ],
        cwd=THIS_FOLDER
    ).decode().strip()


def reset_database(host):
    """
    Run fabric to reset the database
    """
    subprocess.check_call(
        ['fab', 'reset_database', '--host=%s' % (host,)],
        cwd=THIS_FOLDER
    )
