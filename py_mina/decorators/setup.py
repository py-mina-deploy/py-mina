"""
Decorator for setup task
"""


from __future__ import with_statement
import timeit
from fabric.api import task, settings, show, with_settings
from py_mina.config import check_setup_config
from py_mina.tasks.setup import *
from py_mina.echo import echo_task


def setup_task(fn):
	"""
	Setup task function decorator
	"""

	task_name = fn.__name__

	def setup(*args):
		"""
		Runs setup process on remote server
		"""

		echo_task('Running "%s" task' % fn.__name__)

		start_time = timeit.default_timer()

		check_setup_config()

		with settings(show('debug'), hide('output'), colorize_errors=True):
			try:
				create_required()
				create_shared()
				add_repo_to_known_hosts()
				add_host_to_known_hosts()
				fn(*args)
				print_setup_stats(task_name, start_time=start_time)

			except Exception as e:
				print_setup_stats(task_name, error=e.message)

	# Copy __name__ and __doc__ from decorated function to decorator function
	setup.__name__ = task_name
	if fn.__doc__: setup.__doc__ = fn.__doc__

	# Decorate with "fabric" @task decorator
	return task(setup)
