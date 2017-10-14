# Subtasks

Subtasks for most common deploy flows

### git_clone

Execution flow:

1. Clones bare git repository on first deploy to `$deploy_to/scm`
2. Fetches new git commits
3. Clones repository to build directory

### create_shared_paths

Execution flow:

1. Creates shared paths in `$deploy_to/shared`

### link_shared_paths

Execution flow:

1. Links shared paths to build folder

### rollback

Rollbacks latest release (`$latest`) to previous release (`$previous`)

Execution flow:

1. Discovers previous release
2. Sets previous release as current (creates symlink from `$previous` to `$deploy_to/current`)
3. Removes latest release (`$latest`)
