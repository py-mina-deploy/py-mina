"""
Console output
"""


import os
import timeit
from fabric.colors import *


################################################################################
# Echo
################################################################################


# System


def echo_task(message, error=False):
    color = red if error == True else yellow
    
    print(color('\n=====> %s' % message))


def echo_subtask(message, error=False):
    color = red if error == True else cyan

    print(cyan('\n-----> %s' % message))


# For user


def echo_comment(message, error=False):
    color = red if error == True else blue

    print(color(message))


def echo_status(message, error=False):
    color = red if error == True else green

    print(color(message))


################################################################################
# Print
################################################################################


# Task


def print_task_stats(task_name, start_time, error=None):
    status_tuple = (task_name, time_string(start_time))

    if error:
        echo_comment(('\n[FATAL ERROR]\n\n%s' % error), error=True)
        echo_status(('\n=====> Task "%s" failed %s \n' % status_tuple), error=True)
    else:
        echo_status('\n=====> Task "%s" finished %s \n' % status_tuple)
    

# Helpers


def time_string(start_time):
    stop_time = timeit.default_timer()
    delta_time = stop_time - start_time

    return '(time: %s seconds)' % delta_time


# CLI


def cli_staged_init_warning(default_directory = 'deploy'):
    notifictaion = red('\n[WARNING]\n\nDon\'t forget to specify %s %s' % (white('deployfile FILEPATH (-f)'), red('when running staged deployment')))
    prod_path = white('-f %s' % os.path.join(default_directory, 'production.py'))
    dev_path = white('-f %s' % os.path.join(default_directory, 'dev.py'))

    staged_deploy_notification = '''{0}

Production:
    $ py_mina {1} run setup
    $ py_mina {1} run deploy

Dev:
    $ py_mina {2} run setup
    $ py_mina {2} run deploy'''.format(notifictaion, prod_path, dev_path)

    print(staged_deploy_notification)

    
