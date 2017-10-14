"""
Production deploy
"""


from py_mina import *
from deploy import *


# Settings - connection


set('user', 'deploy') 
set('hosts', ['example.com'])

 
# Settings - application


set('deploy_to', '/var/www/my_drf_app_prod')
set('repository', 'path/to/repo')
set('branch', 'master')
