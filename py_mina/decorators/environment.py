"""
Loads environment before running task
"""


def environment_task(fn):
	def environment(*args):
		fn(*args)
	return environment


def with_environment(name):
	def wrapper_fn(fn):
		def wrapper_args(*args):
			print('with environment %s' % name)
			print('called function  %s' % fn.__name__)
		return wrapper_args
	return wrapper_fn