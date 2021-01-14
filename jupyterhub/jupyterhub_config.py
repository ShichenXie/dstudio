# JupyterHub configuration
import os
import sys
from jupyterhub.auth import LocalAuthenticator
from nativeauthenticator import NativeAuthenticator
class LocalNativeAuthenticator(NativeAuthenticator, LocalAuthenticator):
  pass

# jupyterhub_config.py
c = get_config()

## Docker spawner
c.JupyterHub.spawner_class = 'dockerspawner.DockerSpawner'
c.DockerSpawner.image = os.environ['DOCKER_JUPYTERLAB_IMAGE']
# # JupyterHub requires a single-user instance of the Notebook server
DOCKER_SPAWN_CMD="start-singleuser.sh --SingleUserNotebookApp.default_url=/lab"
c.DockerSpawner.extra_create_kwargs.update({'command': DOCKER_SPAWN_CMD})
# Connect containers to this Docker network
network_name = os.environ['DOCKER_NETWORK_NAME']
c.DockerSpawner.use_internal_ip = True
c.DockerSpawner.network_name = network_name
c.DockerSpawner.extra_host_config = { 'network_mode': network_name }
# Remove containers once they are stopped
c.DockerSpawner.remove_containers = True
# For debugging arguments passed to spawned containers
c.DockerSpawner.debug = True

# user data persistence
# see https://github.com/jupyterhub/dockerspawner#data-persistence-and-dockerspawner
notebook_dir = os.environ.get('DOCKER_NOTEBOOK_DIR') or '/home/jovyan/work'
c.DockerSpawner.notebook_dir = notebook_dir
# c.DockerSpawner.volumes = {os.environ['HOST_NOTEBOOK_DIR']+'/{username}': {"bind": notebook_dir, "mode": "rw"}}
c.DockerSpawner.volumes = { 'jupyterhub-user-{username}': notebook_dir }


## Generic
# c.JupyterHub.ip = '0.0.0.0'
# c.JupyterHub.port = 8888

# from jupyter_client.localinterfaces import public_ips
# c.JupyterHub.hub_ip = public_ips()[0]
# c.JupyterHub.hub_ip = os.environ['HUB_IP']
# User containers will access hub by container name on the Docker network
c.JupyterHub.hub_ip = os.environ['HUB_IP'] # 'jupyterhub'
c.JupyterHub.hub_port = 8888


# authenticator
c.JupyterHub.authenticator_class = LocalNativeAuthenticator
c.LocalAuthenticator.create_system_users = True
c.LocalAuthenticator.group_whitelist = {'ds'}
c.Authenticator.admin_users = {'dstudio'}
# c.Authenticator.whitelist = {'ds'}
c.Authenticator.check_common_password = True
c.Authenticator.minimum_password_length = 6
c.Authenticator.allowed_failed_logins = 3


# # Other stuff
# c.Spawner.cpu_limit = 1
# c.Spawner.mem_limit = '2G'

# c.Spawner.http_timeout = 600
# c.Spawner.start_timeout = 600
# Services
c.JupyterHub.services = [
    {
        'name': 'idle-culler',
        'admin': True,
        'command': [sys.executable, '-m', 'jupyterhub_idle_culler', '--timeout=3600'],
    }
]
