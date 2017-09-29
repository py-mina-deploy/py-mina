#!/usr/bin/env python
"""
Command line interface (CLI) for py_mina
"""


import argparse
from commands import cli_init, cli_setup, cli_run


def run():
	#
	# Arguments parsers
	#


	parser = argparse.ArgumentParser(
		prog='py_mina',
		description='command line interface for py_mina')


	#
	# Options
	#


	parser.add_argument(
		'-v', '--version', 
		action='version', version='%(prog)s 2.0')


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


	commands.add_parser(
		'init', 
		help='creates a sample config file in ./deploy/deploy.py')


	# Setup


	setup_parser = commands.add_parser(
		'setup', 
		help='runs setup process on remote server')


	setup_parser.add_argument(
		'-f', '--filename', 
		help='deploy file to import',
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

	if command == 'init': cli_init(args)
	elif command == 'setup': cli_setup(args)
	elif command == 'run': cli_run(args)
	else: parser.print_help()


# Execute if called from console
if __name__ == '__main__': run()