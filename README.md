# py_mina

> __Deployer and server automation tool__

Python library for __deploying__ applications on __remote server__.

Inspired by https://github.com/mina-deploy/mina



## Documentation

* [Getting started](docs/getting-started.md)
* [API Docs](docs/apidocs.md)



## Examples

In [examples](examples) folder you will find examples of deploying:

* __frontend__ application - [reactjs-nodejs](examples/reactjs-nodejs)
* __backend__ application - [django-rest-framework](examples/django-rest-framework)



## Usage

#### 1. Create deployfile in `deploy/deploy.py`

```
$ py_mina init
```

#### 2. Edit deployfile `deploy/deploy.py`

#### 3. Run `task` from deployfile

```
$ py_mina -f deploy/deploy.py run setup
$ py_mina -f deploy/deploy.py run deploy
```
