"""
Deploy tasks
"""

from __future__ import with_statement
import os
from fabric.colors import red, green, yellow
from fabric.api import *
from fabric.contrib.console import confirm
from py_mina.config import fetch, ensure, set, check_config
from py_mina.state import state
from py_mina.echo import *
from py_mina.subtasks.setup import create_entity

################################################################################
# Config
################################################################################


def check_deploy_config():
    """
    Check required config settings for deploy task
    """

    check_config(['user', 'hosts', 'deploy_to', 'repository', 'branch'])


################################################################################
# [PRE] deploy hooks
################################################################################


def check_lock():
    """
    Aborts deploy if lock file is found
    """
    
    def run_abort():
        abort("Another deploy in progress")


    echo_subtask("Checking `deploy.lock` file presence")

    with settings(hide('warnings'), warn_only=True):
        if run('test -f %s' % '/'.join([fetch('deploy_to'), 'deploy.lock'])).succeeded:
            if fetch('ask_unlock_if_locked', default_value=False):
                if not confirm('Deploy lockfile exists. Continue?'): 
                    run_abort()
            else:
                run_abort()


def lock():
    """
    Locks deploy
    Parallel deploys are not allowed
    """

    ensure('build_to')

    echo_subtask("Creating `deploy.lock` file")

    create_entity(
        '/'.join([fetch('deploy_to'), 'deploy.lock'])
        , entity_type='file', 
        protected=False
    )


def create_build_path():
    """
    Creates tmp dir for building app. 

    Folder will be:
        * deleted -> if build fails
        * moved to releases -> if build succeeds
    """
    
    ensure('build_to')

    echo_subtask("Creating build path")

    with settings(hide('warnings'), warn_only=True):
        build_path = fetch('build_to')

        if run('test -d %s' % build_path).failed:
            create_entity(build_path, entity_type='directory', protected=False)


def discover_latest_release():
    """
    Connects to remote server and discovers next release number
    """

    releases_path = fetch('releases_path')

    echo_subtask("Discovering latest release number")

    # Get latest release number
    with settings(hide('warnings'), warn_only=True):
        if run('test -d %s' % releases_path).failed:
            last_release_number = 0
            create_entity(releases_path, entity_type='directory', protected=False)
        else:
            releases_respond = run('ls -1p %s | sed "s/\///g"' % releases_path)
            releases_dirs = list(filter(lambda x: len(x) != 0, releases_respond.split('\r\n')))

            if len(releases_dirs) > 0:
                last_release_number = max(map(lambda x: int(x), releases_dirs)) or 0
            else:
                last_release_number = 0

    release_number = last_release_number + 1

    # Set release info to config 
    set('release_number', release_number)
    set('release_to', '/'.join([releases_path, str(release_number)]))


################################################################################
# [DEPLOY]
################################################################################


def link_shared_paths():
    """
    Links shared paths to build folder
    """

    global build_to
    build_to = fetch('build_to')

    global shared
    shared = fetch('shared_path')

    def link_dirs(dirs):
        global shared
        global build_to

        for sdir in dirs:
            relative_path = '/'.join(['.', sdir])
            directory, filename_ = os.path.split(relative_path)
            shared_path = '/'.join([shared, sdir])
        
            with cd(build_to):
                create_entity(directory, entity_type='directory', protected=False) # create parent directory
                run('rm -rf %s' % relative_path) # remove directory if it conficts with shared
                run('ln -s %s %s' % (shared_path, relative_path)) # link shared to current folder


    def link_files(files):
        global shared
        global build_to
        
        for sfile in files:
            relative_path = '/'.join(['.', sfile])
            directory, filename_ = os.path.split(relative_path)
            shared_path = '/'.join([shared, sfile])

            with cd(build_to):
                create_entity(directory, entity_type='directory', protected=False) # create parent directory
                run('ln -sf %s %s' % (shared_path, relative_path)) # link shared to current folder


    shared_dirs = fetch('shared_dirs', default_value=[])
    shared_files = fetch('shared_files', default_value=[])
    any_shared_dir = len(shared_dirs) > 0
    any_shared_file = len(shared_files) > 0

    protected_shared_dirs = fetch('protected_shared_dirs', default_value=[])
    protected_shared_files = fetch('protected_shared_files', default_value=[])
    any_protected_shared_dir = len(protected_shared_dirs) > 0
    any_protected_shared_file = len(protected_shared_files) > 0

    if any_shared_dir or any_shared_file or any_protected_shared_dir or any_protected_shared_file: 
        echo_subtask("Linking shared paths")

        if any_shared_dir: link_dirs(shared_dirs)
        if any_shared_file: link_files(shared_files)

        if any_protected_shared_dir: link_dirs(protected_shared_dirs)
        if any_protected_shared_file: link_files(protected_shared_files)


################################################################################
# [POST] deploy hooks
################################################################################


def move_build_to_releases():
    """
    Moves current build folder to releases path
    """

    ensure('build_to')
    ensure('release_to')

    echo_subtask('Moving from build path to release path')

    run('mv %s %s' % (fetch('build_to'), fetch('release_to')))


def link_release_to_current():
    """
    Creates current release symlink in `deploy_to` path
    """

    ensure('current_path')

    release_to = fetch('release_to')

    echo_subtask("Linking release to current")

    with cd(release_to):
        run('ln -nfs %s %s' % (release_to, fetch('current_path')))


################################################################################
# [FINALIZE] deploy hooks
################################################################################

def cleanup_releases():
    """
    Cleans up old releases
    """

    ensure('releases_path')

    releases_count = str(fetch('keep_releases'))

    echo_subtask("Cleaning up old realeses. Keeping latest %s" % releases_count)

    with cd(fetch('releases_path')), show('debug'):
        cmd = '''
count=$(ls -A1 | sort -rn | wc -l)
remove=$((count > %s ? count - %s : 0))
ls -A1 | sort -rn | tail -n $remove | xargs rm -rf {}'''

        run(cmd % (releases_count, releases_count))


def remove_build_path():
    """
    Removes a temporary build dir
    """
    
    echo_subtask("Removing build path")

    with settings(hide('stdout', 'warnings'), warn_only=True):
        builds_path = '/'.join([fetch('deploy_to'), 'tmp', 'build-*'])

        run('rm -rf %s' % builds_path)


def force_unlock():
    """
    Forces a deploy unlock
    """

    echo_subtask("Removing `deploy.lock` file")

    run('rm -f %s' % '/'.join([fetch('deploy_to'), 'deploy.lock']))


################################################################################
# Rollback release
################################################################################


def rollback_release():
    """
    Rollbacks latest release
    """
    
    ensure('current_path')

    releases_path = fetch('releases_path')

    with(settings(show('debug'))):
        with cd(releases_path):
            echo_subtask('Finding previous release for rollback')
            rollback_release_number = run('ls -1A | sort -n | tail -n 2 | head -n 1')

            if int(rollback_release_number) > 0:
                echo_subtask('Linking previous release to current')
                run('ln -nfs %s/%s %s' % (releases_path, rollback_release_number, fetch('current_path')))

                echo_subtask('Finding latest release')
                current_release = run('ls -1A | sort -n | tail -n 1')

                if int(current_release) > 0:
                    echo_subtask('Removing latest release')
                    run('rm -rf %s/%s' % (releases_path, current_release))
                else:
                    abort('Can\'t find latest release for remove.')
            else:
                abort('Can\'t find previous release for rollback.')


################################################################################
# Print
################################################################################


def get_error_states():
    def find_error_states(x):
        if x == 'success': return False
        
        return state.get(x) not in [True, None]

    return list(filter(find_error_states, state.keys()))


def print_verbose():
    print(yellow('\n=====> Verbose subtasks stats\n'))

    subtask_states = ['pre_deploy', 'deploy', 'post_deploy', 'finalize', 'on_success']

    for subtask_state_name in subtask_states:
        state_value = state.get(subtask_state_name)

        if state_value == None:
            print_value = white('not invoked')
        elif state_value == True:
            print_value = green('success')
        else:
            print_value = red('failed')

        print('%s - %s' % (yellow('* %s' % subtask_state_name), print_value))


def print_deploy_stats(task_name, start_time):
    if fetch('verbose') == True:
        print_verbose()

    error_states = get_error_states()

    if error_states:
        echo_task('Deploy errors', error=True)

        for error_state in error_states:
            echo_comment(('\n[ERROR]\n%s' % state.get(error_state)), error=True)

    if state.get('success'):
        print(yellow('\n-----> Release number: %s' % fetch('release_number')))

    print_stats_args = [task_name, start_time]
    if state.get('success') != True: print_stats_args.append(True)
    print_task_stats(*print_stats_args)
