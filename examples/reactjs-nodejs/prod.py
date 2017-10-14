"""
Production
"""


from py_mina import *
from deploy import *


# Settings - connection


set('user', 'deploy')
set('hosts', ['example.com'])


# Settings - application


set('deploy_to', '/var/www/nodejs_app_prod')
set('repository', 'https://github.com/react-boilerplate/react-boilerplate')
set('branch', 'master')
