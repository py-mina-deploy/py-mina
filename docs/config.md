# Config

| Name | Type | Default value | Description |
|-|-|-|-|
| user | str | | Remote server ssh user |
| hosts | array[str] | | List of remote hosts |
| deploy_to | str | | Target deploy directory on remote server |
| repository | str | | Git repository endpoint |
| branch | str | | Git branch for deployment |
| shared_files | array | [] | Application shared files |
| shared_dirs | array | [] | Application shared directories |
| owner_user | string | &`user` | Global access owner. CANT access files of protected owner |
| owner_group | string | &`user` | Global access owner. CANT access files of protected owner |
| protected_owner_user | string | &`user` | Protected shared files owner. CAN access files of owner |
| protected_owner_group | string | &`user` | Protected shared files owner. CAN access files of owner |
| sudo_on_chmod | bool | False | Use `sudo` when changing access mode of files |
| sudo_on_chown | bool | False | Use `sudo` when changing owner of files |
| verbose | bool | False | Enables verbose mode |
| abort_on_prompts | bool | True | Aborts execution if prompt occured |

## Set config value - `set`

```
from py_mina import set

set('deploy_to', '/var/www/app')
```

Additional config settings are created when provided `deploy_to` value:

* `build_to` - build folder path (`$deploy_to/tmp/$timestamp`)
* `shared_path` - shared folder path (`$deploy_to/shared`)
* `releases_path` - releases folder path (`$deploy_to/releases`)
* `current_path` - current release symlink path (`$deploy_to/current`)
* `scm` - bare git repository path (`$deploy_to/scm`)

When running [task](tasks.md) decorated with [deploy_task](decorators.md#deploy_task) decorator py_mina
discovers and sets:

* `release_number` - future release number, if deploy will succeed (computed as highest release number in `$deploy_to/releases` + 1)
* `release_to` - future release path (`$deploy_to/releases/$release_number`)


## Get config value - `fetch`

Accepts `default_value` as second parameter for failsafe call.

```
from py_mina import set, fetch

set('deploy_to', '/var/www/app')

fetch('deploy_to') 
# output: '/var/www/app'

fetch('non_existing')
# raises exception

fetch('non_existing', default_value='some value')
# output: 'some value'
```
