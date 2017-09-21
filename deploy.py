from fabric.api import run, cd
from fabric.colors import *
from py_mina import *
from py_mina.tasks import *


################################################################################
# Shared
################################################################################


set('shared_dirs', [
	'frontend/node_modules',
	'frontend/tmp',
	])


set('shared_files', [
	'frontend/test.conf',
	])


################################################################################
# Tasks
################################################################################

# @environment_task
# def node_environment():
# 	run(yellow('echo "NODE_ENVIRONMENT"'))

# @with_environment('node_environment')
@deploy_task
def deploy():
	git_clone()
	link_shared_paths()

	with cd('frontend'):
		run('which node')


@setup_task
def setup():
	print('deploy - setup')


@launch_task
def launch():
	print('launch')
