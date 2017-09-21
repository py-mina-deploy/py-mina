"""
Decorator for setup task
"""


from fabric.api import task
from py_mina.config import configure
from py_mina.tasks.setup import *


def setup_task(fn):
	configure()


	@task
	def setup(*args):
		with settings(colorize_errors=True):
			create_required()
			create_shared()
			add_repo_to_known_hosts()
			add_host_to_known_hosts()

			fn(*args)


	return setup
