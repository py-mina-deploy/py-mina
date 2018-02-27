"""
py_mina CLI commands
"""


import os
import time
from fabric.main import load_fabfile
from fabric.tasks import execute
from fabric.colors import green, red, yellow
from fabric.contrib.console import confirm
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
  Creates init files (default folder path is `deploy/`)
  """
  
  # Show backup message after finish?
  global backup_happened

  def backup_extension(timestamp):
    """
    Generates extenion for backup file
    """

    return str(timestamp) + '.backup'


  def create_or_backup(filepath, content, backup_timestamp = None):
    """
    Creates new file and backups old file if necessary
    """

    if filepath:
      fullpath = os.path.join(os.path.realpath(os.curdir), filepath)
      directory, deployfile = os.path.split(fullpath)
      timestamp = time.time() if backup_timestamp == None else backup_timestamp
      backup_fullpath = "%s.%s" % (fullpath, backup_extension(timestamp))

      try:
        # deployfile directory (create)
        if not os.path.exists(directory):
          os.makedirs(directory)

        # deployfile (backup, create)
        if not os.path.exists(fullpath):
          create_file(filepath, content)
        else:
          if confirm('File %s exists. Backup?' % red(filepath)) == True:
            global backup_happened
            backup_happened = True

            os.rename(fullpath, backup_fullpath)
            print(green('Created backup file %s' % yellow(backup_fullpath)))

          create_file(filepath, content)

      except Exception as error: 
        print(red(error))


  def create_file(filepath, content):
    """
    Writes content to file
    """

    fullpath = os.path.join(os.path.realpath(os.curdir), filepath)

    try:
      with open(filepath, 'w') as f: f.write(content)
      print(green('Deployfile successfully created in %s' % yellow(fullpath)))
    except Exception as error: 
      print(red(error))


  backup_happened = False
  staged = args.get('staged')
  backup_timestamp = time.time()

  if staged == False:
    create_or_backup(args.get('filename'), base_template, backup_timestamp)
  else:
    default_directory = 'deploy/' if staged == None else staged
    templates_files = generate_staged_templates()

    for template_file_key in templates_files.keys():
      filepath = os.path.join(default_directory, '%s.py' % template_file_key)
      create_or_backup(filepath, templates_files[template_file_key], backup_timestamp)

    cli_staged_init_warning(default_directory)

  # show backup message
  if backup_happened:
    print(green('All backuped files has extension ') + red(backup_extension(backup_timestamp)))

