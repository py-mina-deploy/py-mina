"""
Setup tasks
"""


from __future__ import with_statement
import timeit
import os
import re
from py_mina.config import fetch, ensure, check_config
from fabric.api import run, settings, env, cd, hide
from py_mina.echo import *


################################################################################
# Check
################################################################################


def check_setup_config():
    """
    Checks required config settings for setup task
    """

    check_config(['user', 'hosts', 'deploy_to'])


################################################################################
# Create required and shared 
################################################################################


def create_required_structure():
    """
    Creates required folders (tmp, releases, shared) in `deploy_to` path
    """

    ensure('deploy_to')

    echo_subtask('Creating required structure')

    deploy_to = fetch('deploy_to')

    create_entity(deploy_to, entity_type='directory')

    for required_path in ['shared', 'releases', 'tmp']:
        create_entity(os.path.join(deploy_to, required_path), entity_type='directory')



def create_shared_paths():
    """
    Creates shared dirs and touches shared files
    """

    ensure('shared_path')
    ensure('shared_dirs')
    ensure('shared_files')

    echo_subtask('Creating shared paths')

    shared_path = fetch('shared_path')

    # with cd(shared_path):
    for sdir in fetch('shared_dirs'):
        create_entity(os.path.join(shared_path, sdir), entity_type='directory', protected=True)

    for sfile in fetch('shared_files'):
        directory, filename_ = os.path.split(sfile)

        if directory: 
            run('mkdir -p %s' % os.path.join(shared_path, directory))

        filepath = os.path.join(shared_path, sfile)
        
        create_entity(filepath, protected=True)

        recommendation_tuple = (env.host_string, filepath)
        echo_status('\n=====> Don\'t forget to update shared file:\n[%s] %s\n' % recommendation_tuple, error=True)


def fetch_owner():
    """
    Fetches owner of shared paths
    """

    ensure('user')

    user = fetch('user')
    owner_user = fetch('owner_user', default_value=user)
    owner_group = fetch('owner_group', default_value=user)
    protected_owner_user = fetch('protected_owner_user', default_value=user)
    protected_owner_group = fetch('protected_owner_group', default_value=user)

    return owner_user, owner_group, protected_owner_user, protected_owner_group


def create_entity(entity_path, entity_type = 'file', protected=False):
    """
    Creates directory/file and sets proper `chmod` and `chown` values
    """

    owner_user, owner_group, protected_owner_user, protected_owner_group = fetch_owner()
    protected_owner_tuple = (protected_owner_user, protected_owner_group, entity_path)
    owner_tuple = (owner_user, owner_group, entity_path)
    change_owner_tuple = protected_owner_tuple if protected else owner_tuple

    if entity_type == 'file':
        run('touch %s' % entity_path)
    else:
        run('mkdir -p %s' % entity_path)

    run('chmod u+rwx,g+rx,o-rwx ' + entity_path)
    run('chown -R %s:%s %s' % change_owner_tuple)


################################################################################
# SSH known hosts
################################################################################


def add_repo_to_known_hosts():
    """
    Adds repository host to known hosts if possible
    """

    maybe_repository = fetch('repository', default_value='')

    if maybe_repository:
        # Parse repo host
        repo_host_array = re.compile('(@|://)').split(maybe_repository)
        repo_host_part = repo_host_array[-1] if repo_host_array else ''
        repo_host_match = re.compile(':|\/').split(repo_host_part)
        repo_host = repo_host_match[0] if repo_host_match else ''

        # Exit if no host
        if repo_host == '': 
            return

        # Parse port
        repo_port_match = re.search(r':([0-9]+)', maybe_repository)
        repo_port = repo_port_match.group(1) if bool(repo_port_match) else 22

        echo_subtask('Adding repository to known hosts')

        add_to_known_hosts(repo_host, repo_port)


def add_host_to_known_hosts():
    """
    Adds current host to the known hosts

    `fabric3` library sets to `env.host_string` current host where task is executed
    """

    ensure('hosts')

    echo_subtask('Adding current host to known hosts')

    add_to_known_hosts(env.host_string, env.port)


def add_to_known_hosts(host, port):
    cmd = '''
if ! ssh-keygen -H -F {0} &>/dev/null; then
    ssh-keyscan -t rsa -p {1} -H {0} >> ~/.ssh/known_hosts
fi'''.format(host, port)

    with settings(hide('everything'), warn_only=True):
        run(cmd)
