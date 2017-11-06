"""
Templates
"""

deploy_file_sample = '''"""
py_mina deployfile sample
"""

from py_mina import *
from py_mina.subtasks import (
    git_clone, 
    create_shared_paths, 
    link_shared_paths, 
    rollback_release, 
    force_unlock,
)


# Settings - connection


set('user', 'deploy')
set('hosts', ['localhost'])


# Settings - application


set('verbose', True)
set('deploy_to', '/var/www/example_application')
set('repository', 'https://github.com/py-mina-deploy/py-mina')
set('branch', 'master')


# Settings - shared


set('shared_dirs', [])
set('shared_files', [])


# Tasks


@task
def restart():
    """
    Restarts application on remote server
    """

    run('touch restart.txt')


@deploy_task(on_success=restart)
def deploy():
    """
    Runs deploy process on remote server
    """

    git_clone()
    link_shared_paths()


@setup_task
def setup():
    """
    Runs setup process on remote server
    """

    create_shared_paths()


@task
def rollback():
    """
    Rollbacks to previous release
    """

    rollback_release()


@task
def unlock():
    """
    Forces lockfile removal when previous deploy failed
    """

    force_unlock()
'''
