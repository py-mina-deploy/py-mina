from fabric.api import task
from py_mina.config import configure


def deploy_task(fn):
	"""
	Decorator for deploy task
	"""
	
	@task
	def deploy(*args):
		configure()
		fn(*args)

	return deploy
