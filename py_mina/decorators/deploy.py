"""
Decorator for deploy task
"""


from __future__ import with_statement
from fabric.api import task, settings
from py_mina.config import check_deploy_config
from py_mina.state import state, set_state
from py_mina.utils import print_stats
from py_mina.decorators.launch import get_launcher
from py_mina.exceptions import *
from py_mina.tasks.deploy import *


def deploy_task(fn):
	check_deploy_config()


################################################################################	
# INTERNAL
################################################################################	


	def pre_deploy():
		with settings(abort_exception=PreDeployError):
			try: 
				check_lock()
				lock()
				create_build_path()
				discover_latest_release()

				set_state('pre', True)
			except PreDeployError: 
				set_state('pre', False)


	def post_deploy():
		with settings(abort_exception=PostDeployError):
			try:
				if state.get('deploy') == True:
					move_build_to_releases()
					link_release_to_current()

				set_state('post', True)
			except PostDeployError: 
				set_state('post', False)


	def finallize_deploy():
		with settings(abort_exception=FinallizeDeployError):
			try: 
				if state.get('deploy') == True: cleanup_releases()
				remove_build_path()
				unlock()

				set_state('finallize', True)
			except Exception:
				set_state('finallize', False)


	def launch():
		launcher = get_launcher()

		if callable(launcher):
			with settings(abort_exception=LaunchError):
				try: 
					launcher()

					set_state('launch', True)
				except LaunchError:
					set_state('launch', False)
		

################################################################################	
# Decorator
################################################################################	


	@task
	def deploy(*args):
		"""
		Invokes deploy process:
			1) Pre deploy (lock, build path, latest_release)
			2) Deploy
			3) Post deploy (move to releases, link release to current)
			4) Finallize deploy (cleanup, remove build path, unlock)
			5) Launch application
			6) Show deploy stats
		"""

		ensure('build_to')

		with settings(colorize_errors=True):
			try:
				pre_deploy()

				with cd(fetch('build_to')), settings(abort_exception=DeployError):
					try:
						fn(*args)
						set_state('deploy', True)
					except DeployError: 
						set_state('deploy', False)

				post_deploy()
			finally:
				finallize_deploy()

		# Launch application if build succeeded
		if state.get('deploy') == True and state.get('post') == True: 
			launch()

		# Show deploy stats
		print_stats()


	return deploy
