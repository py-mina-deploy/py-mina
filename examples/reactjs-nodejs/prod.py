"""
Production deploy
"""


from py_mina import *
from deploy import *


set('user', 'pymina-deploy') # ssh user
set('hosts', ['example.com']) # remote hosts
set('deploy_to', '/var/www/nodejs_app_prod')
set('repository', 'https://github.com/react-boilerplate/react-boilerplate')
set('branch', 'master')