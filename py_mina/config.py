"""
Configuration manager
"""

import os
import time
from fabric.api import env
from py_mina.utils import _AttributeDict
from py_mina.exceptions import FetchConfigError, EnsureConfigError, BadConfigError

################################################################################
# Default config
################################################################################


config = _AttributeDict({
	'keep_old_releases': 5,
	'shared_paths': [],
	'shared_dirs': [],
})


################################################################################
# Configure environment
################################################################################


def configure():
	# ensure required
	required_settings = ['user', 'hosts', 'deploy_to', 'repository', 'branch']
	try:
		for setting in required_settings:
			ensure(setting)
	except EnsureConfigError:
		raise BadConfigError('Bad config! Required settings are %s' % required_settings)

	# set "fabric" config
	env.user = fetch('user')
	env.hosts = fetch('hosts')

	# set "py_mina" config
	deploy_to = fetch('deploy_to')
	config.update({
		'scm': os.path.join(deploy_to, 'scm'), 
		'shared_path': os.path.join(deploy_to, 'shared'), 
		'current_path': os.path.join(deploy_to, 'current'), 
		'releases_path': os.path.join(deploy_to, 'releases'), 
		'build_to': os.path.join(deploy_to, 'tmp', 'build-' + str(time.time())),
		})


################################################################################
# Helpers
################################################################################


def set(key, value):
	config.update({ key: value })


def fetch(key, default_value=None):
	if key in config.keys():
		return config.get(key)
	else:
		if default_value != None:
			return default_value
		else:
			raise FetchConfigError('"%s" is not defined' % key)


def ensure(key):
	if not key in config.keys():
		raise EnsureConfigError('"%s" must be defined' % key)
