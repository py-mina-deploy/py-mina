"""
Deploy flow for NodeJs application (https://github.com/react-boilerplate/react-boilerplate)
"""

from fabric.api import run, cd
from py_mina import *
from py_mina.tasks import *


################################################################################
# Shared
################################################################################


set('shared_dirs', [
	'node_modules',
	'tmp',
])


# set('shared_files', [])


################################################################################
# Tasks
################################################################################


@deploy_task
def deploy():
	git_clone()
	link_shared_paths()

	run('npm install')
	run('npm run build')


# Launch process is described in `README.md`
@launch_task
def launch():
	run('sudo monit restart -g nodejs_app_prod')


@setup_task
def setup():
	pass
