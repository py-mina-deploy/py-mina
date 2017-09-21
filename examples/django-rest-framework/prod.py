"""
Production deploy
"""

from py_mina.config import set


################################################################################
# DEPLOY CONFIG
################################################################################


set('user', 'pymina-deploy') # ssh user
set('hosts', ['example.com']) # remote hosts
set('deploy_to', '/var/www/my_drf_app_prod')
set('repository', 'path/to/repo')
set('branch', 'master')


################################################################################
# MUST BE AT THE END OF FILE
################################################################################


from deploy import *
