from fabric.api import task

def launch_task(fn):
	"""
	Decorator for launch task
	"""

	@task
	def launch(*args):
		print('Launch decorator')

		fn(*args)

	return launch
