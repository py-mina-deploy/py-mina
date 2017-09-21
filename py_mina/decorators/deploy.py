"""
Decorator for deploy task
"""

from __future__ import with_statement
from fabric.api import task
from py_mina.config import configure
from py_mina.tasks.deploy import *
from py_mina.tasks.git import git_clone


def deploy_task(fn):
	configure()


	@task
	def deploy(*args):
		git_clone()

		fn(*args)


	return deploy
