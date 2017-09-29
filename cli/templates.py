"""
Templates
"""

deploy_file_sample = '''
"""
py_mina - Sample deploy file
"""


from fabric.api import *
from py_mina import set, deploy_task, setup_task, ensure
from py_mina.tasks import git_clone, link_shared_paths


# Settings - remote server


set('user', 'deploy')
set('hosts', ['localhost'])


# Settings - deploy


set('deploy_to', '/var/www/example_application')
set('repository', 'https://github.com/py-mina-deploy/py-mina')
set('branch', 'master')
set('shared_dirs', ['logs', 'tmp'])
set('shared_files', [ 'example_config.yml' ])


# Tasks


@task
def restart():
	"""
	Restarts application on remote server
	"""

	print('Restarting application')


@deploy_task(on_launch=restart)
def deploy():
	"""
	Runs deploy process on remote server
	"""

	git_clone()
	link_shared_paths()

	# your deploy commands

	print('Deploying application')

	# on_launch will be called at the end of deploy process


@setup_task
def setup():
	"""
	Runs deploy process on remote server
	"""

	# your setup commands

	print('Deploy setup')
'''