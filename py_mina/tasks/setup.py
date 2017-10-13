"""
Setup tasks
"""


from __future__ import with_statement
import timeit
import os
import re
from py_mina.config import fetch
from fabric.api import run, settings, env, cd, hide
from py_mina.echo import *


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

	repository = fetch('repository', default_value='')

	if repository and not repository == '':
		# Parse repo host
		
		repo_host_array = re.compile('(@|://)').split(repository)
		repo_host = repo_host_array[-1] if len(repo_host_array) > 0 else ''
		repo_host = re.compile(':|\/').split(repo_host)
		repo_host = repo_host[0] if len(repo_host) > 0 else ''

		# Exit if no host

		if repo_host == '': return

		# Parse port

		repo_port = re.search(r':([0-9]+)', repository)
		repo_port = repo_port.group(1) if bool(repo_port) == True else 22

		# Add

		echo_subtask('Adding repository to known hosts')

		add_to_known_hosts(repo_host, repo_port)


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
fi'''.format(host, port)

	with settings(hide('everything'), warn_only=True):
		run(cmd)


################################################################################
# Print
################################################################################


def print_setup_stats(task_name, **kwargs):
	if 'error' in kwargs:
			echo_comment(('\n[FATAL ERROR]\n\n%s' % kwargs.get('error')), error=True)
			echo_status(('\n=====> Task "%s" failed\n' % task_name), error=True)

	elif 'start_time' in kwargs:
			stop_time = timeit.default_timer()
			delta_time = stop_time - kwargs.get('start_time')

			echo_status('\n=====> Task "%s" finished in %s seconds\n' % (task_name, delta_time))
	
