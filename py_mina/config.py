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
	'verbose': False,
	'farbric_config_settings': ['user', 'hosts', 'abort_on_prompts']
})

################################################################################
# Attributes
################################################################################


def ensure(key):
	"""
	Ensures that config contains value for given key.
	"""

	if not key in config.keys():
		raise EnsureConfigError('"%s" must be defined' % key)


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


def set(key, value):
	"""
	Sets config setting value.
	"""

	if key in config.get('farbric_config_settings'):
		env.update({ key: value })
		config.update({ key: value })
	elif key == 'deploy_to':
		config.update({
			'deploy_to': value, 
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


################################################################################
# Check
################################################################################


def check_deploy_config():
	"""
	Check required settings for deploy
	"""

	check_config(['user', 'hosts', 'deploy_to', 'repository', 'branch'])


def check_setup_config():
	"""
	Check required settings for setup
	"""

	check_config(['user', 'hosts', 'deploy_to'])


def check_config(required_settings=[]):
	"""
	Ensures required settings
	"""

	try:
		for setting in required_settings:
			ensure(setting)
	except EnsureConfigError:
		msg = '''
Bad config! 
Required settings: {0}
Current config: {1}
		'''.format(required_settings, config)

		raise BadConfigError(msg)	