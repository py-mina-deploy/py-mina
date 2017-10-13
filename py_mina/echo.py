"""
Console output
"""


from fabric.colors import *


################################################################################
# Head (system defined)
################################################################################


def echo_task(message, error=False):
	color = red if error == True else yellow
	
	print(color('\n=====> %s' % message))


def echo_subtask(message, error=False):
	color = red if error == True else cyan

	print(cyan('\n-----> %s' % message))


################################################################################
# Body (user defined)
################################################################################


def echo_comment(message, error=False):
	color = red if error == True else blue

	print(color(message))


def echo_status(message, error=False):
	color = red if error == True else green

	print(color(message))