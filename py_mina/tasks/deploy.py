from __future__ import with_statement
import os
from fabric.api import *
from py_mina.config import fetch, ensure, set


################################################################################
# Lockfile
################################################################################


def check_lock():
	"""
	Aborts deploy if lock file is found.
	"""

	ensure('deploy_to')
	
	with settings(warn_only=True), cd(fetch('deploy_to')):
		if run('test -f deploy.lock').succeeded:
			abort("Another deploy in progress")


def lock():
	"""
	Locks deploy. Parallel deploys are not allowed.
	"""

	ensure('build_to')

	with cd(fetch('deploy_to')):
		run('touch deploy.lock')


def unlock():
	"""
	Forces a deploy unlock.
	"""

	ensure('deploy_to')

	with cd(fetch('deploy_to')):
		run('rm -f deploy.lock')


################################################################################
# Deploy
################################################################################


def discover_latest_release():
	"""
	Connects to remote server and discovers next release number
	"""

	releases_path = fetch('releases_path')

	# Get release number
	with settings(warn_only=True):
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


def create_build_path():
	"""
	Creates tmp dir for building app. 

	Folder will be:
		* deleted -> if build fails
		* moved to releases -> if build succeeds
	"""
	
	ensure('build_to')

	with settings(warn_only=True):
		build_path = fetch('build_to')

		if run('test -d %s' % build_path).failed:
			run('mkdir -p %s' % build_path)


def link_shared_paths():
	"""
	Links paths set in shared_dirs and shared_files.
	"""

	ensure('build_to')
	ensure('shared_path')
	ensure('shared_dirs')
	ensure('shared_files')

	with cd(fetch('build_to')):
		shared = fetch('shared_path')

		# Shared dirs
		for sdir in fetch('shared_dirs'):
			relative_path = os.path.join('./', sdir)
			relative_path_parent = os.path.join(*relative_path.split('/')[:-1])
			shared_path = os.path.join(shared, sdir)
		
			run('mkdir -p %s' % relative_path_parent)
			run('rm -rf %s' % relative_path)
			run('ln -s "{0}" "{1}"'.format(
				shared_path,
				relative_path)
				)

		# Shared files
		for sfile in fetch('shared_files'):
			relative_path = os.path.join('./', sfile)
			shared_path = os.path.join(shared, sfile)

			run('ln -sf "{0}" "{1}"'.format(
				shared_path,
				relative_path)
				)


def link_release_to_current():
	"""
	Links shared paths to build dir
	"""

	ensure('release_to')
	ensure('current_path')

	release_to = fetch('release_to')

	with cd(release_to):
		run('ln -nfs %s %s' % (release_to, fetch('current_path')))


################################################################################
# POST Deploy
################################################################################


def move_build_to_releases():
	"""
	Moves tmp build folder to releases dir
	"""

	ensure('build_to')
	ensure('release_to')

	run('mv %s %s' % (
		fetch('build_to'), 
		fetch('release_to'))
		)


def remove_build_path():
	"""
	Removes a temporary build dir
	"""
	
	ensure('build_to')

	with settings(hide('stdout', 'warnings'), warn_only=True):
		run('rm -rf %s' % fetch('build_to'))


def cleanup_releases():
	"""
	Clean up old releases.
	"""

	ensure('releases_path')
	ensure('keep_releases')

	releases_count = str(fetch('keep_releases'))

	with cd(fetch('releases_path')):
		cmd = '''
		count=$(ls -A1 | sort -rn | wc -l)
		remove=$((count > %s ? count - %s : 0))
		ls -A1 | sort -rn | tail -n $remove | xargs rm -rf {}
		''' % (releases_count, releases_count)

		run(cmd)

		# run('count=$(ls -A1 | sort -rn | wc -l)')
		# run('remove=$((count > {0} ? count - {0} : 0))'.format(releases_count))
		# run('ls -A1 | sort -rn | tail -n $remove | xargs rm -rf {}')


def rollback():
	"""
	Rollbacks the latest release.
	"""
	
	# ensure('releases_path')
	# ensure('current_path')

	# releases_path = fetch('releases_path')

	# with cd(releases_path):
	# 	# Rollbacking to release: $rollback_release
	# 	run('rollback_release=$(ls -1A | sort -n | tail -n 2 | head -n 1)')
	# 	run('ln -nfs %s/$rollback_release %s' % (releases_path, fetch('current_path')))

	# 	# Deleting current release: $current_release
	# 	run('current_release=$(ls -1A | sort -n | tail -n 1)')
	# 	run('rm -rf %s/$current_release' % releases_path)

