# Launch application

To launch application we use `monit` daemon (https://mmonit.com/monit/).
Monit configuration is also included (see `monit.conf`).

> __IMPORTANT__

Monit runs as superuser (root). Its considered a bad practice to use `root` for running webserver, applications, etc. Instead of it, create local non-super user.

__Notice `start program` section of `monit.conf`__

We use `su -l {user}` to run our nodejs server as non-superuser.

In most cases `{user}` is the same user, you use to connect to remote server over ssh (specified in `prod.py`, in my case `pymina-deploy`).

Also you should __allow `{user}` to run `sudo monit` command without prompting password__. 

Run `visudo` command and add the following line:

```
pymina-deploy ALL=(ALL) NOPASSWD: /usr/bin/monit
```


## Run `react-boilerplate`

https://github.com/react-boilerplate/react-boilerplate

__To be able write `PID` of nodejs server and log `stdout` and `stderr`__ you should edit `start:prod` script in `packages.json`


```
{
	"name": "react-boilerplate",

	....


	"scripts": {

		...
	
		"start:prod": "(cross-env NODE_ENV=production node server) > tmp/stdout.log 2> tmp/stderr.log & echo $! >> tmp/pid",

		...

	},

	....
}
```


Fork https://github.com/react-boilerplate/react-boilerplate, edit `packages.json` and start your career as __Vlad, The Deployer__!


## Nginx

Nginx config is also included (see `nginx.conf`). Nginx `upstreams` allows us to use several instances of application (runs on different ports) for better load balancing.