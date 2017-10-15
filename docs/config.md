# Config

| Name | Type | Default value | Description |
|-|-|-|-|
| user | str | | Remote server ssh user |
| hosts | array[str] | | List of remote hosts |
| deploy_to | str | | Target deploy directory on remote server |
| repository | str | | Git repository endpoint |
| branch | str | | Git branch for deployment |
| verbose | bool | False | Enables verbose mode |
| abort_on_prompts | bool | False | Aborts execution if prompt occured |

## Set config value

```
from py_mina import set

set('deploy_to', '/var/www/app')
```

## Get config value

```
from py_mina import fetch

fetch('deploy_to') # => /var/www/app
```
