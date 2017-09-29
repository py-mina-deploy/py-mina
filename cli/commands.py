"""
py_mina CLI commands
"""


import os
from fabric.main import load_fabfile
from fabric.colors import green, red
from cli.templates import deploy_file_sample


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
			callables[task_name]()


#
# Init
#


def cli_command_init(args):
	"""
	Creates a sample config file in ./deploy/deploy.py
	"""

	filepath = args.get('filename')

	if filepath:
		fullpath = os.path.join(os.path.realpath(os.curdir), filepath)
		directory, deployfile = os.path.split(fullpath)

		try:
			# Create deployfile directory if not exists
			os.makedirs(directory, exist_ok=True)

			# Write template string to file
			with open(filepath, 'w') as f:
				f.write(deploy_file_sample)

			print(green('Sample deploy file successfully created in %s' % fullpath))

		except Exception as error: 
			print(red(error))

