from py_mina import set
from deploy import *

set('user', 'deploy')
set('hosts', ['agony.wdf.cz'])
set('branch', 'master')
# set('repository', 'git@git.wdf.cz:wdf-developers/watermark.git')
set('deploy_to', '/var/www/py-mina-test')
