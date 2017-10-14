# Tasks

Task is a function which can be listed and executed in console (by [py_mina CLI](commands.md))

## Define task

Task is defined by wrapping function with py_mina decorator. There are several types of decorators which applies different hooks.

Read [decorators documentation](decorators.md) for more information.

## Writing your own tasks

We use [fabric3](https://github.com/mathiasertl/fabric/) to invoke commands on remote server.
Read [fabric documentation](http://docs.fabfile.org/en/1.13/) and see [examples](../examples) for better understanding.

## List available tasks

```
$ py_mina list
```

See [CLI list command documentation](commands.md#list)

## Run task

```
$ py_mina run task_name
```

See [CLI run command documentation](commands.md#run)

