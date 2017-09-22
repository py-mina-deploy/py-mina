"""
Deploy flow for Django Rest Framework (http://www.django-rest-framework.org/)
"""


from fabric.api import run, cd
from py_mina import *
from py_mina.tasks import *


################################################################################
# Shared
################################################################################


set('shared_dirs', [
	'storage',
	'env',
	'tmp',
])


# Don't forget to edit this files on remote server
set('shared_files', [
	'my_drf_app/db_conf.py',
	'my_drf_app/custom_conf.py',
])


################################################################################
# Tasks
################################################################################


# Launch process is described in `README.md`
def launch():
	run('sudo monit restart -g my_drf_app_prod')


@deploy_task(on_launch=launch)
def deploy():
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
	We use `pyenv` as python version manager and `virtualenv` as python environment manager:

		1) Install `anyenv` (https://github.com/riywo/anyenv)
		2) `anyenv install pyenv`
		3) `pyenv install 2.7.2`
		4) `pyenv local 2.7.2 && pip install virtualenv`
	"""

	virtualenv_path = os.path.join(fetch('shared_path'), 'env')

	with settings(warn_only=True):
		virtualenv_exists = run('test -d %s' % os.path.join(virtualenv_path, 'bin'))

		if virtualenv_exists.failed:
			with prefix('pyenv local 2.7.2'):
				run('virtualenv %s' % virtualenv_path)

