"""
Generates py_mina deployfile templates
"""


pymina_head = '''"""
py_mina deployfile
"""\n\n'''


################################################################################
# Settings
################################################################################


def generate_settings(settings_type='global', staged=False):
    if settings_type == 'global': return generate_settings_global(staged)
    if settings_type == 'application': return generate_settings_application(staged)
    if settings_type == 'shared': return generate_settings_shared(staged)
    if settings_type == 'connection': return generate_settings_connection(staged)


def generate_settings_global(staged=False):
    staged_import = ('%s\nfrom py_mina import set\n\n\n' % pymina_head) if staged != False else ''

    return '''{0}# Settings - global


set('verbose', True)
set('keep_releases', 5)
#set('sudo_on_chown', True)
#set('sudo_on_chmod', True)
#set('ask_unlock_if_locked', True)'''.format(staged_import)


def generate_settings_application(staged=False):
    branch = 'master'
    application_name = 'example_application'
    application_string = '%s\'' % application_name

    if staged != False:
        branch = 'master' if staged == 'production' else staged
        application_string = '{0}_{1}'.format(
            application_name, 
            '''%s' % fetch('stage_name')'''
        )

    return '''# Settings - application


set('deploy_to', '/var/www/{0})
set('repository', 'https://github.com/py-mina-deploy/dummy-web-for-deployment')
set('branch', '{1}')'''.format(application_string, branch)


def generate_settings_shared(staged=False):
    return '''# Settings - shared [PUBLIC] files/dirs (application configs, assets, storage, etc.)


set('shared_dirs', [])
set('shared_files', [])


# Settings - explicit owner of [PUBLIC] shared files/dirs


#set('owner_user', 'www-data')
#set('owner_group', 'www-data')


# Settings - protected shared files/dirs (db configs, certificates, keys, etc.)
#          * [PROTECTED] owner config settings are required to be set


#set('protected_shared_dirs', [])
#set('protected_shared_files', [])


# Settings - owner of [PROTECTED] shared files/dirs

#set('protected_owner_user', 'root')
#set('protected_owner_group', 'root')'''


def generate_settings_connection(staged=False):
    staged_name = ("\nset('stage_name', '%s')" % staged) if staged != False else ''

    return '''# Settings - remote server connection


set('user', 'root')
set('hosts', ['localhost']){0}'''.format(staged_name)


################################################################################
# Head and Tasks
################################################################################


def generate_head(staged=False, import_subtasks=False):
    subtasks = '''from py_mina.subtasks import (
    git_clone, 
    create_shared_paths, 
    link_shared_paths, 
    rollback_release, 
    force_unlock,
)'''
    staged_without_subtasks = '''{0}
from py_mina import set, fetch
from tasks import *
import settings'''.format(pymina_head)
    staged_with_subtasks = '''{0}
from py_mina import *
{1}'''.format(pymina_head, subtasks)
    staged_return = staged_with_subtasks if import_subtasks else staged_without_subtasks

    return staged_return if staged else '%s\nfrom py_mina import *\n%s' % (pymina_head, subtasks)



def generate_tasks(staged=False):
    return '''# Tasks


@task
def restart():
    """
    Restarts application on remote server
    """
    
    with cd(fetch('current_path')):
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


################################################################################
# Place template
################################################################################


template_places_2 = '''{0}


{1}'''


template_places_3 = '''{0}


{1}


{2}'''


template_places_4 = '''{0}


{1}


{2}


{3}'''


template_places_5 = '''{0}


{1}


{2}


{3}


{4}'''

template_places_6 = '''{0}


{1}


{2}


{3}


{4}


{5}'''
