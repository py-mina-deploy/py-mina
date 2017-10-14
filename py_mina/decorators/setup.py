"""
Decorator for setup task
"""


from __future__ import with_statement
import timeit
from fabric.api import task, settings, show, hide
from py_mina.tasks.setup import *
from py_mina.echo import echo_task


def setup_task(wrapped_function):
	"""
	Setup task function decorator
	"""

	wrapped_function_name = wrapped_function.__name__

	def setup(*args):
		"""
		Runs setup process on remote server
			1) check required settings (user, host, deploy_to)
			2) creates required dirs (releases, shared, tmp)   
			3) creates shared dirs and files
			4) adds repo and host to known hosts if possible
			5) runs wrpapped function
		"""

		echo_task('Running "%s" task' % wrapped_function_name)

		start_time = timeit.default_timer()

		check_setup_config()

		with settings(show('debug'), hide('output'), colorize_errors=True):
			try:
				create_required()
				create_shared()
				add_repo_to_known_hosts()
				add_host_to_known_hosts()
				wrapped_function(*args)
				print_setup_stats(wrapped_function_name, start_time=start_time)
			except Exception as e:
				print_setup_stats(wrapped_function_name, error=e, start_time=start_time)

	# Copy __name__ and __doc__ from decorated function to decorator function
	setup.__name__ = wrapped_function_name
	if wrapped_function.__doc__: setup.__doc__ = wrapped_function.__doc__

	# Decorate with `fabric3` task decorator
	return task(setup)
