"""
Fabric commands to use by fuctional tests on production
"""

from fabric.api import env, run


def _get_base_folder(host):
    """
    Get site base folder
    """
    return '/home/%s/sites/' % (env.user,) + host


def _get_manage_dot_py(host):
    """
    Returns string `virtualenv_path manage.py_path`
    """
    virtualenv_folder = '/home/%s/.virtualenvs/%s' % (env.user, host,)
    return '%s/bin/python %s/manage.py' % (
        virtualenv_folder, _get_base_folder(host),
    )


def reset_database():
    """
    Runs `manage.py flush` to reset the database
    """
    run('{manage_dot_py} flush --noinput'.format(
        manage_dot_py=_get_manage_dot_py(env.host)
    ))


def create_session_on_server(email):
    """
    Runs `manage.py create_session` to create new user session on server
    """
    session_key = run('{manage_dot_py} create_session {email}'.format(
        manage_dot_py=_get_manage_dot_py(env.host),
        email=email,
    ))
    print(session_key)
