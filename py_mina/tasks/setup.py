from __future__ import with_statement
import os
from py_mina.config import fetch
from fabric.api import run, settings, env, cd


################################################################################
# Create required and shared 
################################################################################


def create_required():
	"""
	Creates required folders for deployment
	"""

	for required_path in ['shared', 'releases', 'tmp']:
		run('mkdir -p %s' % os.path.join(fetch('deploy_to'), required_path))


def create_shared():
	"""
	Creates shared_dirs and touches shared_files
	"""

	with cd(fetch('shared_path')):
		for sdir in fetch('shared_dirs'):
			run('mkdir -p %s' % sdir)

		for sfile in fetch('shared_files'):
			path_parent = os.path.join(*sfile.split('/')[:-1])
			run('mkdir -p %s' % path_parent)
			run('touch ' + sfile)
			run('chmod g+rx,u+rwx ' + sfile)


################################################################################
# SSH known hosts
################################################################################


def add_repo_to_known_hosts():
	"""
	Adds current repo host to the known hosts
	"""

	pass
	# repo_host = fetch(:repository).split(%r{@|://}).last.split(%r{:|\/}).first
	# repo_port = /:([0-9]+)/.match(fetch(:repository)) && /:([0-9]+)/.match(fetch(:repository))[1] || '22'

	# next if repo_host == ""


def add_host_to_known_hosts():
	"""
	Adds domain(host) to the known hosts
	"""

	add_to_known_hosts(env.host_string, env.port)


def add_to_known_hosts(host, port):
	cmd = '''
	if ! ssh-keygen -H -F {0} &>/dev/null; then
		ssh-keyscan -t rsa -p {1} -H {0} >> ~/.ssh/known_hosts
	fi
	'''.format(host, port)

	with settings(warn_only=True):
		run(cmd)
