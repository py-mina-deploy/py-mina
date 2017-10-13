"""
Templates
"""

deploy_file_sample = '''"""
py_mina - deployfile sample
"""

from py_mina import *
from py_mina.tasks import git_clone, link_shared_paths


# Settings - remote server


set('user', 'deploy')
set('hosts', ['localhost'])


# Settings - application


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

	pass


@deploy_task(on_launch=restart)
def deploy():
	"""
	Runs deploy process on remote server
	"""

	git_clone()
	link_shared_paths()


	run('pwd && ls -lah')


@setup_task
def setup():
	"""
	Runs setup process on remote server
	"""

	pass
'''