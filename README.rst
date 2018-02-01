py_mina
=======

**Deployer and server automation tool**

Python library for **deploying** applications on **remote server**.

Inspired by https://github.com/mina-deploy/mina

Documentation
-------------

-  `Getting started <docs/getting-started.md>`__
-  `API Docs <docs/apidocs.md>`__

Examples
--------

In `examples <examples>`__ folder you will find examples of deploying:

-  **frontend** application -
   `reactjs-nodejs <examples/reactjs-nodejs>`__
-  **backend** application -
   `django-rest-framework <examples/django-rest-framework>`__

Usage
-----

1. Create deployfile in ``deploy/deploy.py``
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

::

    $ py_mina init

2. Edit deployfile ``deploy/deploy.py``
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

3. Run ``task`` from deployfile
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

::

    $ py_mina -f deploy/deploy.py run setup
    $ py_mina -f deploy/deploy.py run deploy
