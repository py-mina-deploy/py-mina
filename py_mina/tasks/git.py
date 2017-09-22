"""
Git tasks
"""


from __future__ import with_statement
import os
from fabric.api import *
from py_mina.config import *


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

	scm = fetch('scm')

	with settings(warn_only=True):
		if run('test -d %s' % scm).failed:
			run('git clone {0} {1} --bare'.format(fetch('repository'), scm))


def fetch_new_commits():
	"""
	Fetches new git commits
	"""

	ensure('scm')
	ensure('repository')
	ensure('branch')

	with cd(fetch('scm')):
		run('git fetch {0} "{1}:{1}" --force'.format(fetch('repository'), fetch('branch')))


def use_git_branch():
	"""
	Clone repository to "build_to"
	"""

	ensure('build_to')
	ensure('scm')
	ensure('branch')

	with cd(fetch('build_to')):
		run('git clone {0} . --recursive --branch {1}'.format(fetch('scm'), fetch('branch')))
		run('rm -rf .git')

