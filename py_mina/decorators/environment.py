"""
Loads environment before running task
"""


def environment_task(fn):
	def environment(*args):
		fn(*args)
	return environment


def with_environment(name):
	def wrapper(fn):
		def wrapper_fn(*args):
			print('with environment %s' % name)
			print('called function  %s' % fn.__name__)
		return wrapper_fn
	return wrapper
