# Command Line Interface

Commands:

* [Generate deployfile sample](#init)
* [List tasks](#list)
* [Run task](#run)
* [Show version](#version)
* [Show help](#help)

## Parameters

| Name | Default value | Description |
|-|-|-|
| -f | deploy/deploy.py | Deployfile location |

## Commands

Following commands are available for execution

#### init

Creates deployfile sample.

```
$ py_mina [-f FILEPATH] init
```

#### list

Shows available tasks in deployfile.

```
$ py_mina [-f FILEPATH] list
```

#### run

Runs task from deployfile.

```
$ py_mina [-f FILEPATH] run task_name
```

#### version

Shows py_mina version.

```
$ py_mina -v
```

#### help

Shows help for py_mina cli usage.

```
$ py_mina -h
```
