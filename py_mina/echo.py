"""
Console output
"""


from fabric.colors import *


def echo_task(message):
	print(yellow('=====> %s' % message))


def echo_subtask(message):
	print(cyan('\n-----> %s' % message))


def echo_comment(message):
	print(blue(message))


def echo_danger(message):
	print(red(message))

