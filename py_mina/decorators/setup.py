from fabric.api import task
from py_mina.config import configure


def setup_task(fn):
	"""
	Decorator for setup task
	"""

	@task
	def setup(*args):
		configure()
		fn(*args)

	return setup
