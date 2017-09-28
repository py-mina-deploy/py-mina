"""
Console output
"""


from fabric.colors import *


def echo_task(message):
	print(green('-----> %s' % message))


def echo_subtask(message):
	print(yellow('       %s' % message))

