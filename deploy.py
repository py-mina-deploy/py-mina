from py_mina import *
from fabric.api import run, cd


################################################################################
# Shared
################################################################################


set('shared_dirs', [
	'frontend/node_modules',
	'frontend/tmp',
	])


set('shared_paths', [
	'frontend/node_modules',
	])


################################################################################
# Tasks
################################################################################


@deploy_task
def deploy():
	with cd('frontend'):
		run('npm -v')


@setup_task
def setup():
	print('setup')


@launch_task
def launch():
	print('launch')
