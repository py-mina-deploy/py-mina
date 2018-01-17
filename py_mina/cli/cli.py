#!/usr/bin/env python
"""
Command line interface (CLI) for py_mina
"""


import argparse
import pkg_resources
from py_mina.cli.commands import *


try:
	version = pkg_resources.require("py_mina")[0].version
except Exception:
	version = '[error]'


def run():
	#
	# Arguments parser
	#


	parser = argparse.ArgumentParser(
		prog='py_mina',
		description='command line interface for py_mina')


	#
	# Options
	#


	parser.add_argument(
		'-v', '--version', 
		action='version', version='py_mina %s' % version)


	parser.add_argument(
		'-f', '--filename',
		metavar='FILEPATH',
		help='deployfile relative location (default: "./deploy/deploy.py")',
		dest='filename', default='./deploy/deploy.py')


	#
	# Commands
	#


	commands = parser.add_subparsers(
		help='',
		dest='command', metavar='<commands>')


	# Init


	init_parser = commands.add_parser(
		'init', 
		help='creates basic deployfile in relative FILEPATH (default: "./deploy/deploy.py")')


	init_parser.add_argument(
		'-s', '--staged', 
		metavar='DIRPATH', nargs='?',
		help='creates "staged deployment" deployfiles in relative DIRPATH (default: "./deploy/")',
		default=False)


	# Run


	run_parser = commands.add_parser(
		'run', 
		help='runs task from deployfile')


	run_parser.add_argument(
		'task',
		help='task to run on remote server')


	# List


	list_parser = commands.add_parser(
		'list', 
		help='lists available tasks in deployfile')


	#---------------------------------------------------------------------------


	args = vars(parser.parse_args())
	command = args.get('command')

	if command == 'init': cli_command_init(args)
	elif command == 'run': cli_command_run(args)
	elif command == 'list': cli_command_list(args)
	else: parser.print_help()
