from __future__ import with_statement
import os
from fabric.api import settings, hide, run
from py_mina.config import fetch, set

def git_clone():
	git_latest_release()


def git_latest_release():
	"""
	Connects to remote server and discovers next release number
	"""

	releases_path = fetch('releases_path')

	# Get release number
	with settings(hide('stdout', 'warnings'), warn_only=True):
		if run('test -d %s' % releases_path).failed:
			run('mkdir -p %s' % releases_path)
			last_release_number = 0
		else:
			releases_respond = run('ls -1p %s | sed "s/\///g"' % releases_path)
			releases_dirs = filter(lambda x: len(x) != 0, releases_respond.split('\r\n'))

			if len(releases_dirs) > 0:
				last_release_number = max(map(lambda x: int(x), releases_dirs)) or 0
			else:
				last_release_number = 0

	release_number = last_release_number + 1

	# Set release info to config 
	set('release_number', release_number)
	set('release_to', os.path.join(releases_path, str(release_number)))
