"""
Console output
"""


from fabric.colors import *


def echo_task(message):
	fillment = (len(message) + 14) * '='

	print(yellow('%s' % fillment))
	print(yellow('=====> %s <=====' % message))
	print(yellow('%s' % fillment))


def echo_subtask(message):
	print('')
	print(cyan('-----> %s' % message))


def echo_comment(message):
	print(blue(message))


def echo_danger(message):
	print(red(message))

