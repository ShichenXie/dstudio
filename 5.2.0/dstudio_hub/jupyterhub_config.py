# Copyright (c) Jupyter Development Team.
# Distributed under the terms of the Modified BSD License.

# Configuration file for JupyterHub
import os

c = get_config()  # noqa: F821

# We rely on environment variables to configure JupyterHub so that we
# avoid having to rebuild the JupyterHub container every time we change a
# configuration parameter.

# Spawn single-user servers as Docker containers
#c.JupyterHub.spawner_class = "dockerspawner.DockerSpawner"

# Spawn containers from this image
# c.DockerSpawner.image = os.environ["LAB_IMAGE_ADMIN"]

# setting image for each user
def image_for_user(user):
    "Given a user, return the right image"""
    if user.name == os.environ.get("JUPYTERHUB_ADMIN"):
        return os.environ["LAB_IMAGE_ADMIN"]
    else:
        return os.environ["LAB_IMAGE_USER"]

from dockerspawner import DockerSpawner
class MyDockerSpawner(DockerSpawner):
    def start(self):
        self.image = image_for_user(self.user)
        return super().start()
c.JupyterHub.spawner_class = MyDockerSpawner


# Connect containers to this Docker network
network_name = os.environ["DOCKER_NETWORK_NAME"]
c.DockerSpawner.use_internal_ip = True
c.DockerSpawner.network_name = network_name

# Explicitly set notebook directory because we'll be mounting a volume to it.
# Most `jupyter/docker-stacks` *-notebook images run the Notebook server as
# user `jovyan`, and set the notebook directory to `/home/jovyan/work`.
# We follow the same convention.
lab_work_dir = "/home/jovyan/work" # os.environ.get("DOCKER_NOTEBOOK_DIR", "/home/jovyan/work")
c.DockerSpawner.notebook_dir = lab_work_dir

# Mount the real user's Docker volume on the host to the notebook user's
# notebook directory in the container
# share volume 
volumes_dict = {'jupyterlab-share': '/home/jovyan/share'}
# user volume
if 'LAB_DIR_HOST' in list(os.environ):
  volumes_dict[os.environ['LAB_DIR_HOST']+'/{username}'] = {"bind": lab_work_dir, "mode": "rw"}
else:
  volumes_dict['jupyterlab-user-{username}'] = lab_work_dir
c.DockerSpawner.volumes = volumes_dict

# Remove containers once they are stopped
def str2bool(v):
  return v.lower() in ("yes", "true", "t", "1", "True", "TRUE")
  
c.DockerSpawner.remove = str2bool(os.environ['LAB_CONTAINER_REMOVE'])

# jupyterhub default url
c.DockerSpawner.default_url = os.environ['HUB_DEFAULT_URL']
# For debugging arguments passed to spawned containers
c.DockerSpawner.debug = True

# User containers will access hub by container name on the Docker network
c.JupyterHub.hub_ip = "jupyterhub"
c.JupyterHub.hub_port = 8080

# Persist hub data on volume mounted inside container
c.JupyterHub.cookie_secret_file = "/data/jupyterhub_cookie_secret"
c.JupyterHub.db_url = "sqlite:////data/jupyterhub.sqlite"

# Allow all signed-up users to login
c.Authenticator.allow_all = True

# Authenticate users with Native Authenticator
import nativeauthenticator
c.JupyterHub.authenticator_class = "nativeauthenticator.NativeAuthenticator"

# Allow anyone to sign-up without approval
c.NativeAuthenticator.open_signup = str2bool(os.environ['HUB_OPEN_SIGNUP'])

# Allowed admins
admin = os.environ.get("JUPYTERHUB_ADMIN")
if admin:
    c.Authenticator.admin_users = [admin]

# Services
import sys
c.JupyterHub.services = [
    {
        "name": "idle-culler",
        "command": [sys.executable, "-m", "jupyterhub_idle_culler", '--timeout='+os.environ['HUB_TIMEOUT']],
    }
]