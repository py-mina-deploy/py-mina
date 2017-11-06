"""
Configuration manager
"""


import os
import time
from fabric.api import env
from py_mina.utils import _AttributeDict
import py_mina.state


################################################################################
# Default config
################################################################################


config = _AttributeDict({
    'keep_releases': 7,
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
    Ensures presence of config setting
    """

    if not key in config.keys():
        raise Exception('"%s" must be defined' % key)


def fetch(key, default_value=None):
    """
    Gets and ensures config setting or returns `default_value` if provided
    """

    if key in config.keys():
        return config.get(key)
    else:
        if default_value != None:
            return default_value
        else:
            raise Exception('"%s" is not defined' % key)


def set(key, value):
    """
    Sets config setting
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


# Alias to prevent conflict when importing "py_mina.config" and "py_mina.state" in one file
set_config = set


################################################################################
# Check
################################################################################


def check_config(required_settings=[]):
    """
    Ensures required settings in cofig
    """

    try:
        for setting in required_settings:
            ensure(setting)
    except EnsureConfigError:
        msg = 'Bad config!\nRequired settings: {0}\nCurrent config: {1}'

        raise Exception(msg.format(required_settings, config))  
