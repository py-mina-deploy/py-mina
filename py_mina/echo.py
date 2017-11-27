"""
Console output
"""


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
