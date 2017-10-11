# py-mina

> __Deployer and server automation tool__

Python library for __deploying__ applications on __remote server__. Based on [Fabric](http://www.fabfile.org/) library which handles ssh connections to remote server.

Inspired by https://github.com/mina-deploy/mina

## Documentation

* [Getting started](docs/getting-started.md)
* [API Docs](docs/apidocs.md)

## Examples

In [examples](examples) folder you will find examples of deploying:

* __frontend__ application - [reactjs-nodejs](examples/reactjs-nodejs)
* __backend__ application - [django-rest-framework](examples/django-rest-framework)


## Usage

#### 1. Create deployfile

```
$ py_mina init
```

will generate following file in `deploy/deploy.py`:

```
from py_mina import *
from py_mina.tasks import git_clone, link_shared_paths


# Settings - remote server


set('user', 'deploy')
set('hosts', ['localhost'])


# Settings - application


set('deploy_to', '/var/www/example_application')
set('repository', 'https://github.com/py-mina-deploy/py-mina')
set('branch', 'master')
set('shared_dirs', ['logs', 'tmp'])
set('shared_files', [ 'example_config.yml' ])


# Tasks


@task
def restart():
	"""
	Restarts application on remote server
	"""

	run('echo "Restarting application"')


@deploy_task(on_launch=restart)
def deploy():
	"""
	Runs deploy process on remote server
	"""

	git_clone()
	link_shared_paths()

	run('echo "Deploying application"')

	# ... your deploy commands ...


@setup_task
def setup():
	"""
	Runs setup process on remote server
	"""

	run('echo "Deploy setup"')

	# ... your setup commands ...
```

#### 2. Run `task` from deployfile

```
$ py_mina -f deploy/deploy.py run setup
$ py_mina -f deploy/deploy.py run deploy
```