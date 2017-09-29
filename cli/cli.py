#!/usr/bin/env python
"""
Command line interface (CLI) for py_mina
"""


import argparse
from cli.commands import cli_command_init, cli_command_run
import pkg_resources

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
		'-q', '--quite', 
		help='don\'t use verbose mode',
		action='store_true')


	#
	# Commands
	#


	commands = parser.add_subparsers(
		help='available commands',
		dest='command', metavar='<command>')


	# Init


	init_parser = commands.add_parser(
		'init', 
		help='creates a sample deploy file')


	init_parser.add_argument(
		'-f', '--filename', 
		help='deploy file to create',
		dest='filename', default='deploy/deploy.py')


	# Run


	run_parser = commands.add_parser(
		'run', 
		help='runs task from deploy file')


	run_parser.add_argument(
		'task',
		help='task to run on remote server')


	run_parser.add_argument(
		'-f', '--filename', 
		help='deploy file to import',
		dest='filename', default='deploy/deploy.py')


	#---------------------------------------------------------------------------

	args = vars(parser.parse_args())
	command = args.get('command')

	if command == 'init': cli_command_init(args)
	elif command == 'run': cli_command_run(args)
	else: parser.print_help()