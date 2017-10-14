"""
Git tasks
"""


from __future__ import with_statement
import os
from fabric.api import settings, hide, run, cd
from py_mina.echo import echo_subtask, echo_task
from py_mina.config import fetch, ensure


def git_clone():
	"""
	Clones repository to tmp build dir
	"""

	maybe_clone_git_repository()
	fetch_new_commits()
	use_git_branch()


def maybe_clone_git_repository():
	"""
	Clones bare git repository on first deploy
	"""

	ensure('repository')
	ensure('scm')

	echo_subtask('Ensures git repository presence')

	with settings(hide('warnings'), warn_only=True):

		if run('test -d %s' % fetch('scm')).failed:
			echo_subtask("Cloning bare git repository")

			run('git clone {0} {1} --bare'.format(fetch('repository'), fetch('scm')))


def fetch_new_commits():
	"""
	Fetches new git commits
	"""

	ensure('scm')
	ensure('repository')
	ensure('branch')

	echo_subtask("Fetching new commits")

	with cd(fetch('scm')):
		run('git fetch {0} "{1}:{1}" --force'.format(fetch('repository'), fetch('branch')))


def use_git_branch():
	"""
	Clones repository to build dir
	"""

	ensure('build_to')
	ensure('scm')
	ensure('branch')

	echo_subtask("Copying code from repository to build folder")

	with cd(fetch('build_to')):
		run('git clone {0} . --recursive --branch {1}'.format(fetch('scm'), fetch('branch')))
		run('rm -rf .git')

