"""
Setup tasks
"""


from __future__ import with_statement
import os
from py_mina.config import fetch
from fabric.api import run, settings, env, cd, hide
from py_mina.echo import echo_subtask


################################################################################
# Create required and shared 
################################################################################


def create_required():
	"""
	Creates required folders for deployment
	"""

	echo_subtask('Creating required folders')

	for required_path in ['shared', 'releases', 'tmp']:
		run('mkdir -p %s' % os.path.join(fetch('deploy_to'), required_path))


def create_shared():
	"""
	Creates shared_dirs and touches shared_files
	"""

	echo_subtask('Creating shared paths')

	with cd(fetch('shared_path')):
		for sdir in fetch('shared_dirs'):
			run('mkdir -p %s' % sdir)

		for sfile in fetch('shared_files'):
			directory, filename_ = os.path.split(sfile)

			if directory: 
				run('mkdir -p %s' % directory)

			run('touch ' + sfile)
			run('chmod g+rx,u+rwx ' + sfile)


################################################################################
# SSH known hosts
################################################################################


def add_repo_to_known_hosts():
	"""
	Adds current repo host to the known hosts
	"""

	echo_subtask('Adding repository to known hosts')

	pass
	# repo_host = fetch(:repository).split(%r{@|://}).last.split(%r{:|\/}).first
	# repo_port = /:([0-9]+)/.match(fetch(:repository)) && /:([0-9]+)/.match(fetch(:repository))[1] || '22'

	# next if repo_host == ""


def add_host_to_known_hosts():
	"""
	Adds domain(host) to the known hosts
	"""

	echo_subtask('Adding current host to known hosts')

	add_to_known_hosts(env.host_string, env.port)


def add_to_known_hosts(host, port):
	cmd = '''
	if ! ssh-keygen -H -F {0} &>/dev/null; then
		ssh-keyscan -t rsa -p {1} -H {0} >> ~/.ssh/known_hosts
	fi
	'''.format(host, port)

	with settings(hide('everything'), warn_only=True):
		run(cmd)
