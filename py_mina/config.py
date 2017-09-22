"""
Configuration manager
"""


import os
import time
from fabric.api import env
from py_mina.utils import _AttributeDict
import py_mina.state
from py_mina.exceptions import FetchConfigError, EnsureConfigError, BadConfigError


################################################################################
# Default config
################################################################################


config = _AttributeDict({
	'keep_releases': 5,
	'shared_files': [],
	'shared_dirs': [],
	'abort_on_prompts': False,
	'farbric_config_settings': ['user', 'hosts', 'abort_on_prompts']
})


################################################################################
# Configure environment
################################################################################


def check_deploy_config():
	"""
	Ensures required settings is config for deploy and setup tasks
	"""

	required_settings = ['user', 'hosts', 'deploy_to', 'repository', 'branch']
	try:
		for setting in required_settings:
			ensure(setting)
	except EnsureConfigError:
		raise BadConfigError('Bad config! Required settings are %s' % required_settings)


################################################################################
# Helpers
################################################################################


def set(key, value):
	"""
	Set config setting.
	"""

	if key in config.get('farbric_config_settings'):
		env.update({ key: value })
	elif key == 'deploy_to':
		config.update({
			'scm': os.path.join(value, 'scm'), 
			'shared_path': os.path.join(value, 'shared'), 
			'current_path': os.path.join(value, 'current'), 
			'releases_path': os.path.join(value, 'releases'), 
			'build_to': os.path.join(value, 'tmp', 'build-' + str(time.time())),
			})
	else:
		config.update({ key: value })


# Alias to prevent conflict when importing "py_mina.config" and "py_mina.state"
set_config = set


def fetch(key, default_value=None):
	"""
	Fetches config setting by given key.
	Returns default_value if key is missing and default value is provided.
	"""

	if key in config.keys():
		return config.get(key)
	else:
		if default_value != None:
			return default_value
		else:
			raise FetchConfigError('"%s" is not defined' % key)


def ensure(key):
	"""
	Ensures that config contains value for given key.
	"""

	if not key in config.keys():
		raise EnsureConfigError('"%s" must be defined' % key)
