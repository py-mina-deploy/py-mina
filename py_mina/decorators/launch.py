from fabric.api import task
from py_mina.exceptions import LaunchSingletonError

# Singleton
__launch_function = None


def get_launcher(): return __launch_function


def launch_task(fn):
	"""
	Decorator for launch task
	"""

	global __launch_function

	if not __launch_function:
		__launch_function = fn

		@task
		def launch(*args):
			fn(*args)

		return launch
	else:
		raise LaunchSingletonError("Launch task is singleton. Only one function can be decorated with @launch_task")
