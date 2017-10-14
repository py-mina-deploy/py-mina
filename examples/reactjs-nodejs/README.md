# Launch application

To launch application we use `monit` daemon (https://mmonit.com/monit/).

Monit configuration and `init.d` script is also included.

> __IMPORTANT__

Monit runs as superuser (root). Its considered a bad practice to use `root` for running webserver, applications, etc. Instead of it, create local non-super user.

__Notice `start_it` function in `init.d/nodeje_app_prod`__

We run our server as non-superuser.

In most cases `$USER` is the same user, you use to connect to remote server over ssh (specified in `prod.py`, in my case `deploy`).

Also you should __allow `$USER` to run `sudo monit` command without prompting sudo password__. 

Run `visudo` command and add the following line:

```
deploy ALL=(ALL) NOPASSWD: /usr/bin/monit
```

## Nginx

Nginx config is also included (see `nginx.conf`). Nginx `upstreams` allows us to use several instances of application (runs on different ports) for better load balancing.
