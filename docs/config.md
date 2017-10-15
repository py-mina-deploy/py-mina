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

Accepts `default_value` as second parameter to make failsafe

```
from py_mina import fetch

fetch('deploy_to') 
# output: '/var/www/app'

fetch('non_existing')
# raises exception

fetch('non_existing', default_value='some value')
# output: 'some value'
```
