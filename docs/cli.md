# Command Line Interface

Commands:

* [Generate deployfile sample](#init)
* [List tasks](#list)
* [Run task](#run)
* [Show version](#version)
* [Show help](#help)

## Global parameters

| Name | Default value | Description |
|-|-|-|
| -f | `./deploy/deploy.py` | Deployfile path |
| -h | | Show help for command which is placed before. Position is important. For example `py_mina run -h` will show help for [`run`](#run) command |

## Commands

Following commands are available for execution

#### init

| Name | Default value | Description |
|-|-|-|
| -s, --staged | `./deploy/` | Path for staged deploy initialization (creates multiple files). Ignores `-f` parameter |

Deploy config file/files initialization.

```
$ py_mina [-f FILEPATH] init [-s DIRPATH]
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
