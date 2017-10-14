"""
Deploy NodeJs application 
https://github.com/react-boilerplate/react-boilerplate
"""


from py_mina import *
from py_mina.tasks import git_clone, create_shared_paths, link_shared_paths, rollback_release


# Settings - shared


set('verbose', True)
set('shared_dirs', ['node_modules', 'tmp'])
set('shared_files', [])


# Tasks


@task
def restart():
	"""
	Restarts application on remote server
	"""

	# read README.md
	run('sudo monit restart -g nodejs_app_prod')


@deploy_task(on_success=restart)
def deploy():
	"""
	Runs deploy process on remote server
	"""

	git_clone()
	link_shared_paths()

	run('npm install')
	run('npm run build')


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
