"""
Task decorator (wrapper for `fabric3` @task decorator)
"""


from __future__ import with_statement
import timeit
import fabric.api
from py_mina.echo import echo_task, print_task_stats


def task(wrapped_function):
	"""
	Task function decorator
	"""

	wrapped_function_name = wrapped_function.__name__


	def task_wrapper(*args):
		"""
		Runs task and prints stats at the end
		"""

		echo_task('Running "%s" task\n' % wrapped_function_name)

		start_time = timeit.default_timer()

		with fabric.api.settings(colorize_errors=True):
			try:
				wrapped_function(*args)
			except Exception as e:
				print_task_stats(wrapped_function_name, start_time, e)

				raise e # escalate exception
			else:
				print_task_stats(wrapped_function_name, start_time)


	# Copy __name__ and __doc__ from decorated function to wrapper function
	task_wrapper.__name__ = wrapped_function_name or 'task'
	if wrapped_function.__doc__: task_wrapper.__doc__ = wrapped_function.__doc__

	# Decorate with `fabric3` task decorator
	return fabric.api.task(task_wrapper)
