To manually create a virtualenv on MacOS and Linux: 

```
$ python3 -m venv .venv
```

After the init process completes and the virtualenv is created, you can use the following
step to activate your virtualenv.

```
$ source .venv/bin/activate
```

If you are a Windows platform, you would activate the virtualenv like this:

```
% .venv\Scripts\activate.bat 
```

### Using Shipment CLI
Shipment provides with a CLI, providing server,shell and more to come commands

Run this command before we start
```
pip install -e  .
```

#### Develop

The `develop` command starts the development server if a port is busy it will select the next port. This server will continually watch for file changes and reload the server accordingly.

```bash
> shipment server develop
```
#### Start

The `start` command starts a shipment web server of production grade. It's an alias to the [uvicorn](https://www.uvicorn.org/) web server, it contains all of the options available with that server.

```bash
> shipment server start --help
Usage: maps server start [OPTIONS] main:app

Options:
  --port INTEGER                  Bind socket to this port.  [default: 8000]
  --reload                        Enable auto-reload.
  --reload-dir TEXT               Sets reload directories explicitly, instead
                                  of using the current working directory.
  ...
```

#### Shell

The `shell` command is useful for development. It drops you into an python shell with the database connection.

```bash
> shipment server shell
```

By default our shell has logger enabled to disable it we have --nolog option

```bash
> shipment server shell --nolog
```

Shipment shell has autoreload enabled, to disable it run

```
%autoreload 0
```

to enable it again run

```
%autoreload
```

to reload it just once run 

```
%autoreload 2
```


### Without using Shipment CLI

```
$ python3 -m pip install --upgrade -r requirements.txt
```

pip3 freeze > requirements.txt

```
cd src

```

```
uvicorn main:app --reload

```

Enjoy!


## Start Celery

```
$ celery -A workers.celery_worker.celery worker -B --loglevel=info -Q communication,critical,low,shipment,workflow

```

## Start Flower

```
$ celery -A workers.celery_worker.celery flower --port=5555 -Q communication,critical,low,shipment,workflow

```
