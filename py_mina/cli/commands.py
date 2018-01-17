"""
py_mina CLI commands
"""


import os
from fabric.main import load_fabfile
from fabric.tasks import execute
from fabric.colors import green, red
from py_mina.cli.templates import base_template, generate_staged_templates
from py_mina.echo import cli_staged_init_warning


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

	def create_file(filepath, content):
		if filepath:
			fullpath = os.path.join(os.path.realpath(os.curdir), filepath)
			directory, deployfile = os.path.split(fullpath)

			try:
				# Create deployfile directory if not exists
				if not os.path.exists(directory):
				    os.makedirs(directory)

				# Write template string to file
				with open(filepath, 'w') as f:
					f.write(content)

				print(green('Deployfile successfully created in %s' % fullpath))

			except Exception as error: 
				print(red(error))


	staged = args.get('staged')

	if staged == False:
		create_file(args.get('filename'), base_template)
	else:
		default_directory = 'deploy/' if staged == None else staged
		templates_files = generate_staged_templates()

		for template_file_key in templates_files.keys():
			filepath = os.path.join(default_directory, '%s.py' % template_file_key)
			create_file(filepath, templates_files[template_file_key])

		cli_staged_init_warning(default_directory)


