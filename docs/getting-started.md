# Setting up a project

Let's deploy a project using `py_mina`.

### Step 0: Configure server

Your server needs to be properly configured for py_mina to work. Requirements for py_mina 0.1.4 to work:
- SSH public/private key pair set up
- deploy user to have access to folders where you want to install the application
- deploy user can start/stop/restart application (server, daemon, etc.)
- installed git
- installed python
- installed pip

### Step 1: Create a `deploy/deploy.py`

In your project, type `py_mina init` to create a sample of this file.

    $ py_mina init
    Created deploy/deploy.py.

This is just a python file with tasks! See [How to write your own tasks](writing_your_own_tasks.md) for
more info on what *deploy.py* is. You will want to at least configure your
server:

```python
# deploy/deploy.py
set('user', 'username')
set('hosts', ['your.server.com'])
set('deploy_to', '/var/www/example_application')
...
```

### Step 2: Run 'setup' task

Back at your computer, do `setup` to set up the folder structure in `deploy_to` path.
This will connect to your server via SSH and create the right directories.

    $ py_mina run setup
    -----> Creating required structure

### Step 3: Deploy!

Use `py_mina run deploy` to run the `deploy` task defined in *deploy/deploy.py*.

    $ py_mina run deploy
    =====> Running "deploy" task
           ...
           Lots of things happening...
           ...

### Step 4: Considerations after first deploy

If you changed `shared_files` and `shared_dirs` in your `deploy.py` you have to run `setup` task again. This ensures all needed folders are created.
