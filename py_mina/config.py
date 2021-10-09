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
    'ask_unlock_if_locked': False,
    'verbose': False,
    'abort_on_prompts': False,
    'sudo_on_chown': False,
    'sudo_on_chmod': False,
    'sudo_on_cleanup_releases': False,
    'farbric_config_settings': ['user', 'hosts', 'abort_on_prompts']
})


################################################################################
# Attributes
################################################################################


def ensure(key):
    """
    Ensures presence of config setting. Prevents from running unnecessary commands,
    before discovering, that config setting is not set
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
    Sets config setting (updates `fabric3` config if necessary)
    """

    if key in config.get('farbric_config_settings'):
        env.update({ key: value })
        config.update({ key: value })
    elif key == 'deploy_to':
        config.update({
            'deploy_to': value, 
            'scm': '/'.join([value, 'scm']), 
            'shared_path': '/'.join([value, 'shared']), 
            'current_path': '/'.join([value, 'current']), 
            'releases_path': '/'.join([value, 'releases']), 
            'build_to': '/'.join([value, 'tmp', 'build-' + str(time.time())]),
        })
    else:
        config.update({ key: value })


# Alias to prevent conflict when importing "py_mina.config" and "py_mina.state" in one file
set_config = set


################################################################################
# Helpers
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
