"""
Decorator for deploy task
"""


from __future__ import with_statement
import timeit
from fabric.api import task, settings
from py_mina.state import state, set_state
from py_mina.exceptions import *
from py_mina.tasks.deploy import *
from py_mina.echo import echo_task

def deploy_task(on_success=None):
	"""
	Deploy task arguments decorator
	"""

	def deploy_task_wrapper(wrapped_function):
		"""
		Deploy task decorator
		"""

		wrapped_function_name = wrapped_function.__name__


		def _pre_deploy():
			try: 
				check_lock()
				lock()
				create_build_path()
				discover_latest_release()
				set_state('pre_deploy', True)
			except Exception as error: 
				set_state('pre_deploy', error)

				raise error # escalate exception to 'deploy' function

		def _deploy(*args):
			if state.get('pre_deploy') == True:
				try:
					with cd(fetch('build_to')):
						wrapped_function(*args)
					set_state('deploy', True)
				except Exception as error: 
					set_state('deploy', error)

					raise error # escalate exception to 'deploy'


		def _post_deploy():
			if state.get('deploy') == True:
				try:
					move_build_to_releases()
					link_release_to_current()
					set_state('post_deploy', True)
				except Exception as error: 
					set_state('post_deploy', error)

					raise error # escalate exception to 'deploy'


		def _finallize_deploy():
			try: 
				cleanup_releases()
				remove_build_path()
				unlock()
				set_state('finallize', True)
			except Exception as error:
				set_state('finallize', error)


		def _on_success_deploy():
			if  state.get('success') == True and callable(on_success):
				try: 
					on_success()
					set_state('on_success', True)
				except Exception as error:
					set_state('on_success', error)


		def deploy(*args):
			"""
			Runs deploy process on remote server
				1) Pre deploy (lock, build path, latest_release)
				2) Deploy
				3) Post deploy (move to releases, link release to current)
				4) Finallize deploy (cleanup, remove build path, unlock)
				5) Runs `on_success` callback function if deploy successfully finished
				6) Shows deploy stats
			"""
			
			echo_task('Running "%s" task' % wrapped_function_name)

			start_time = timeit.default_timer()

			check_deploy_config()

			with settings(colorize_errors=True):
				try:
					_pre_deploy()
					_deploy(*args)
					_post_deploy()
					set_state('success', True)
				except Exception as error:
					echo_comment('\n\n[FATAL ERROR]\n\n%s' % error, error=True)
					set_state('success', error)					
				finally:
					_finallize_deploy()

				_on_success_deploy()
				
				print_deploy_stats(wrapped_function_name, start_time=start_time)

		
		# Copy __name__ and __doc__ from decorated function to decorator function
		deploy.__name__ = wrapped_function_name
		if wrapped_function.__doc__: deploy.__doc__ = wrapped_function.__doc__

		# Decorate with `fabric3` task decorator
		return task(deploy)

	return deploy_task_wrapper
