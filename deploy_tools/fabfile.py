import random
from fabric.contrib.files import append, exists, sed
from fabric.api import env, local, run

REPO_URL = 'git@github.com:lancelote/TDD_book.git'


def deploy():
    """
    Deploy web site to the server
    """
    site_folder = '/home/%s/sites/%s' % (env.user, env.host,)
    _create_directory_structure_if_necessary(site_folder)
    _get_latest_source(site_folder)
    _update_settings(site_folder, env.host)
    _update_virtualenv(env.user, env.host, site_folder)
    _update_staticfiles(env.user, site_folder, env.host)
    _update_database(env.user, site_folder, env.host)


def _create_directory_structure_if_necessary(site_folder):
    """
    Create a site folder if necessary
    """
    run('mkdir -p %s' % (site_folder,))


def _get_latest_source(site_folder):
    """
    Update git repository or clone it
    """
    if exists(site_folder + '/.git'):
        run('cd %s && git fetch' % (site_folder,))
    else:
        run('git clone %s %s' % (REPO_URL, site_folder,))
    current_commit = local('git log -n 1 --format=%H', capture=True)
    run('cd %s && git reset --hard %s' % (site_folder, current_commit,))


def _update_settings(site_folder, site_name):
    """
    Set up a production settings
    """
    settings_path = site_folder + '/superlists/settings.py'
    sed(
        settings_path,
        "DEBUG = True",
        "DEBUG = False"
    )
    sed(
        settings_path,
        "DOMAIN = 'localhost'",
        "DOMAIN = '%s'" % (site_name,)
    )
    secret_key_file = site_folder + '/superlists/secret_key.py'
    if not exists(secret_key_file):
        chars = 'abcdefghijklmnopqrstuvwxyz0123456789!@#$%^&*(-_=+)'
        key = ''.join(random.SystemRandom().choice(chars) for _ in range(50))
        append(secret_key_file, 'SECRET_KEY = "%s"' % (key,))
    append(settings_path, '\nfrom .secret_key import SECRET_KEY')


def _update_virtualenv(user, site_name, site_folder):
    """
    Update virtualenv or start a new one
    """
    virtualenv_folder = '/home/%s/.virtualenvs/%s' % (user, site_name,)
    if not exists(virtualenv_folder):
        run('virtualenv --python=python3 /home/%s/.virtualenvs/%s' % (
            user, site_name,
        ))
    run('%s/bin/pip install -r %s/requirements.txt' % (
        virtualenv_folder, site_folder,
    ))


def _update_staticfiles(user, site_folder, site_name):
    """
    Update static files
    """
    virtualenv_folder = '/home/%s/.virtualenvs/%s' % (user, site_name,)
    run('cd %s && %s/bin/python3 manage.py collectstatic --noinput' % (
        site_folder, virtualenv_folder,
    ))


def _update_database(user, site_folder, site_name):
    """
    Update database
    """
    virtualenv_folder = '/home/%s/.virtualenvs/%s' % (user, site_name,)
    run('cd %s && %s/bin/python3 manage.py migrate --noinput' % (
        site_folder, virtualenv_folder,
    ))
