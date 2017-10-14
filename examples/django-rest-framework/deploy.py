"""
Deploy Django Rest Framework 
http://www.django-rest-framework.org/
"""


from py_mina import *
from py_mina.subtasks import git_clone, create_shared_paths, link_shared_paths, rollback_release


# Settings - shared


set('verbose', True)
set('shared_dirs', ['storage', 'env', 'tmp'])
set('shared_files', ['my_drf_app/db_conf.py', 'my_drf_app/custom_conf.py'])


# Tasks


@task
def restart():
	"""
	Restarts application on remote server
	"""

	# read README.md
	run('sudo monit restart -g my_drf_app_prod')


@deploy_task(on_success=restart)
def deploy():
	"""
	Runs deploy process on remote server
	"""

	git_clone()
	link_shared_paths()

	with prefix('source env/bin/activate'):
		# Lock dependencies (example of `packages` file is also included)
		run('pip install pip-tools')
		run('pip-compile --output-file packages.lock packages')
		
		# Install
		run('pip install -r packages.lock')

		# Migrate DB
		run('python ./manage.py makemigrations')
		run('python ./manage.py migrate')


@setup_task
def setup():
	"""
	Runs setup process on remote server
	We use `pyenv` as python version manager and `virtualenv` as python environment manager:

		1) Install `anyenv` (https://github.com/riywo/anyenv)
		2) `anyenv install pyenv`
		3) `pyenv install 3.6.2`
		4) `pyenv local 3.6.2 && pip install virtualenv`
	"""

	create_shared_paths()

	virtualenv_path = os.path.join(fetch('shared_path'), 'env')

	with settings(hide('warnings'), warn_only=True):
		virtualenv_exists = run('test -d %s' % os.path.join(virtualenv_path, 'bin'))

		if virtualenv_exists.failed:
			with prefix('pyenv local 3.6.2'):
				run('virtualenv %s' % virtualenv_path)


@task
def rollback():
	"""
	Rollbacks to previous release
	"""

	rollback_release()
