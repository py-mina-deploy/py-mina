"""
Production deploy
"""

from py_mina import set


# Set deploy config
set('user', 'deploy')
set('hosts', ['agony.wdf.cz'])
set('branch', 'master')
set('repository', 'git@git.wdf.cz:wdf-developers/watermark.git')
set('deploy_to', '/var/www/py-mina-test')


# Import tasks - MUST BE at the END of file
from deploy import *
