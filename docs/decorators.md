# Decorators

Defines [task](tasks.md) and modifies execution flow by wrapping function with subtasks/hooks.

## @setup_task

```
from py_mina import *
from py_mina.subtasks import create_shared_paths

@setup_task
def setup_application():
	create_shared_paths()
```

Execution flow:

1. Checks config for required settings
2. Creates required structure/directories (`tmp`, `releases`, `shared`) in `$deploy_to` path
3. Adds repository and current host to `~/.ssh/known_hosts` if possible
4. Executes decorated function (in our case `setup_application`)
5. Prints task execution stats




## @deploy_task

Accepts `on_success` callback as parameter.

```
from py_mina import *
from py_mina.subtasks import git_clone, link_shared_paths

@task
def restart_application():
	run('touch restart.txt')

@deploy_task(on_success=restart_application)
def deploy_application():
	git_clone()
	link_shared_paths()
```

Execution flow:

1. Checks config for required settings
2. Runs [pre_deploy](#pre_deploy) hook
3. Executes decorated function (in our case `deploy_application`) if [pre_deploy](#pre_deploy) hook succeeded 
4. Runs `post_deploy` hook if decorated function (in our case `deploy_application`) execution succeeded
5. Runs [cleanup](#cleanup) hook
6. Runs `on_success` callback if provided and [pre_deploy](#pre_deploy), [post_deploy](#post_deploy) hooks succeeded
7. Prints task execution stats

### Hooks

#### `pre_deploy`

Execution flow:

1. Checks deploy lock and aborts execution if lockfile (`$deploy_to/deploy.lock`) exists
2. Create deploy lockfile because parallel deploys are not allowed
3. Creates build directory (`$deploy_to/tmp/build-$timestamp`)
4. Connects to remote server and computes current release number (`$release_number`)

#### `post_deploy`

Execution flow:

1. Moves build directory to releases path (`$deploy_to/releases/$release_number`)
2. Creates current release symlink in `$deploy_to` path

#### `cleanup`

Execution flow:

1. Cleans up old releases (keeps latest `$keep_releases`, default is `7`)
2. Removes a build directory
3. Unlocks deploy (removes lockfile)




### @task


```
from py_mina import *

@task
def restart_application():
	run('touch restart.txt')
```

Execution flow:

1. Executes decorated function (in our case `restart_application`)
2. Prints task execution stats
