"""
py_mina CLI commands
"""


import os
from fabric.main import load_fabfile
from fabric.tasks import execute
from fabric.colors import green, red
from py_mina.cli.templates import deploy_file_sample


#
# List
#


def cli_command_list(args):
	"""
	Runs task from deploy file
	"""
	
	filepath = args.get('filename')
	task_name = args.get('task')

	if filepath:
		fullpath = os.path.join(os.path.realpath(os.curdir), filepath)
		docstring, callables, default = load_fabfile(fullpath)

		if not docstring == None:
			print(docstring.rstrip('\n'))

		print('\nAvailable commands:\n')

		for task_name in callables:
			task_desc = callables.get(task_name).__doc__

			if not task_desc == None:
				description = task_desc.lstrip('\n').rstrip('\n')
			else:
				description = '\n'

			print('%s   %s' % (green(task_name), description))


#
# Run
#


def cli_command_run(args):
	"""
	Runs task from deploy file
	"""
	
	filepath = args.get('filename')
	task_name = args.get('task')

	if filepath:
		fullpath = os.path.join(os.path.realpath(os.curdir), filepath)
		docstring, callables, default = load_fabfile(fullpath)

		if task_name in callables:
			execute(callables[task_name])


#
# Init
#


def cli_command_init(args):
	"""
	Creates a sample config file (default path is ./deploy/deploy.py)
	"""

	filepath = args.get('filename')
	staged = args.get('staged')

	if filepath:
		fullpath = os.path.join(os.path.realpath(os.curdir), filepath)
		directory, deployfile = os.path.split(fullpath)

		try:
			# Create deployfile directory if not exists
			if not os.path.exists(directory):
			    os.makedirs(directory)

			# Write template string to file
			with open(filepath, 'w') as f:
				f.write(deploy_file_sample)

			print(green('Deployfile successfully created in %s' % fullpath))

		except Exception as error: 
			print(red(error))
