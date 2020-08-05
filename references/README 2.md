# Docker base image of JupyterHub and JupyterLab

JupyterHub is a multi-user server for Jupyter notebooks. JupyterLab is the next
generation web-based user interface for the Jupyter Project.
[jorgklein/jupyterhub][1] is a [Docker][2] base image for [JupyterHub][3] and
[JupyterLab][4]. Images derived from this image can either run as a stand-alone
server, or function as a volume image for your server.

[1]: https://hub.docker.com/r/joergklein/jupyterhub
[2]: https://docker.com
[3]: https://jupyterhub.readthedocs.io/en/stable
[4]: https://jupyterlab.readthedocs.io/en/stable

## Building your JupyterHub image and run the container

Based on this structure, you can easily build an image for your needs. There
are two options for using the image you generated:

- as a stand-alone image
- as a volume image for your webserver

The simplest way to build your own image is to use a Dockerfile. This is only
an example. If you need more software packages you can install them with this
Dockerfile and conda.

### Build the image

The Repo is on https://github.com/joergklein/docker-jupyterhub

```sh
docker build -t jupyterhub .
```

Your JupyterHub with JupyterLab is automatically generated during this build.

### Download the image and run the container

```sh
docker run -p 8000:8000 -d --name jupyterhub joergklein/jupyterhub jupyterhub
```

### Download the image, mount a local data directory and run the container

```sh
docker run -p 8000:8000 -d --name jupyterhub --volume $(pwd)/datasets:/home/admin/data joergklein/jupyterhub jupyterhub
```

- `-p` is used to map your `local port 8000` to the `container port 8000`.
- `-d` is used to run the container in background. JupyterHub will just write
logs so no need to output them in your terminal unless you want to troubleshoot
a server error.
- `--name jupyterhub` names your container jupyterhub.
- `--volume $(pwd)/datasets:/data` mount the local directory /dataset into the container to /data.
- `jupyterhub` the image.
- `jupyterhub` is the last command used to start the jupyterhub server.

and your `JupyterHub` with `Jupyterlab` is now available on
`http://localhost:8000`.

### Start / Stop JupyterHub

```sh
docker start / stop jupyterhub
```

## Configure JupyterHub

### The system user in the container

By default JupyterHub searches for users on the server. In order to be able to
log in to our new JupyterHub server we need to connect to the JupyterHub docker
container and create a new system user with a password.

#### Set the password for the administrator

**Notice** The user admin will be created by the Dockerfile. The reason is to
avoid error messages during the start process.

```sh
docker exec -it jupyterhub bash
passwd admin
```

The command `docker exec -it jupyterhub bash` will spawn a root shell in your
docker container.  **You can use the root shell to create system users in the
container**. These accounts will be used for authentication in JupyterHub's
default configuration.

#### Set users and passwords for the working class heros

```sh
docker exec -it jupyterhub bash
useradd --create-home user1
passwd user1
```

Login as admin and change to `localhost:8000/hub/admin`. In the admin panel you
can change the rights for a basic user.

### Configure jupyterhub_config.py

```sh
# jupyterhub_config.py
c = get_config()

# Change from JupyterHub to JupyterLab
c.Spawner.default_url = '/lab'
c.Spawner.debug = True

# Specify users and admin
c.Authenticator.whitelist = {"admin"}
c.Authenticator.admin_users = {"admin"}
```

### Install new packages
```sh
docker exec -it jupyterhub bash
conda install -c conda-forge <package name>

Example:
conda install -c conda-forge r-kableextra
```
