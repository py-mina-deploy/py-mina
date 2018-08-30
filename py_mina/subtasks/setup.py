"""
Setup tasks
"""


from __future__ import with_statement
import timeit
import os
import re
from py_mina.config import fetch, ensure, check_config
from fabric.api import run, sudo, settings, env, cd, hide
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

    deploy_to = fetch('deploy_to')

    echo_subtask('Creating required structure')

    create_entity(deploy_to, entity_type='directory', protected=False)

    for required_path in ['shared', 'releases', 'tmp']:
        create_entity(
            '/'.join([deploy_to, required_path]), 
            entity_type='directory', 
            protected=False
        )



def create_shared_paths():
    """
    Creates shared (+protected) files/dirs and sets unix owner/mode
    """

    global shared_path
    shared_path = fetch('shared_path')

    def create_dirs(directories, protected=False):
        global shared_path

        for sdir in directories:
            create_entity(
                '/'.join([shared_path, sdir]), 
                entity_type='directory', 
                protected=protected
            )


    def create_files(files, protected=False):
        global shared_path

        for sfile in files:
            directory, filename_ = os.path.split(sfile)

            if directory: 
                create_entity(
                    '/'.join([shared_path, directory]), 
                    entity_type='directory', 
                    protected=protected
                )

            filepath = '/'.join([shared_path, sfile])
            create_entity(filepath, entity_type='file', protected=protected)

            recommendation_tuple = (env.host_string, filepath)
            echo_status('\n=====> Don\'t forget to update shared file:\n[%s] %s\n' % recommendation_tuple, error=True)


    echo_subtask('Creating shared paths')

    # Shared
    create_dirs(fetch('shared_dirs', default_value=[]), protected=False)
    create_files(fetch('shared_files', default_value=[]), protected=False)

    # Protected
    create_dirs(fetch('protected_shared_dirs', default_value=[]), protected=True)
    create_files(fetch('protected_shared_files', default_value=[]), protected=True)


def create_entity(entity_path, entity_type = 'file', protected=False):
    """
    Creates directory/file and sets proper owner/mode.
    """

    chmod_sudo = 'sudo ' if fetch('sudo_on_chmod') else ''
    chown_sudo = 'sudo ' if fetch('sudo_on_chown') else ''

    def change_owner(owner_triple):
        """
        Changes unix owner/mode
        """

        run(chmod_sudo + 'chmod 0755 ' + entity_path)
        run(chown_sudo + 'chown %s:%s %s' % owner_triple)


    # 1) Create file/directory

    if entity_type == 'file':
        run('touch %s' % entity_path)
    else:
        run('mkdir -p %s' % entity_path)

    # 2) Change owner/mode

    if protected:
        protected_owner_user = fetch('protected_owner_user')
        protected_owner_group = fetch('protected_owner_group')

        change_owner((protected_owner_user, protected_owner_group, entity_path))
    else:
        owner_user = fetch('owner_user', default_value=False)
        owner_group = fetch('owner_group', default_value=False)
        
        if owner_user != False and owner_group != False: 
            change_owner((owner_user, owner_group, entity_path))
        else:
            run(chmod_sudo + 'chmod 0755 ' + entity_path)


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
