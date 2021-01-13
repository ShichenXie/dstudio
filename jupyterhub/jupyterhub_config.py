# JupyterHub configuration
#
## If you update this file, do not forget to delete the `jupyterhub_data` volume before restarting the jupyterhub service:
##
##     docker volume rm jupyterhub_jupyterhub_data
##
## or, if you changed the COMPOSE_PROJECT_NAME to <name>:
##
##    docker volume rm <name>_jupyterhub_data
##
import os
import sys
from jupyterhub.auth import LocalAuthenticator
from nativeauthenticator import NativeAuthenticator
class LocalNativeAuthenticator(NativeAuthenticator, LocalAuthenticator):
  pass

# jupyterhub_config.py
c = get_config()
## Generic
# c.JupyterHub.ip = '0.0.0.0'
# c.JupyterHub.port = 8888

from jupyter_client.localinterfaces import public_ips
c.JupyterHub.hub_ip = public_ips()[0]
# c.JupyterHub.hub_ip = 'jupyterhub'
# c.JupyterHub.hub_port = 8888

c.JupyterHub.statsd_prefix = 'jupyterhub'
c.Spawner.default_url = '/lab'


# authenticator
c.JupyterHub.authenticator_class = LocalNativeAuthenticator
c.LocalAuthenticator.create_system_users = True
c.LocalAuthenticator.group_whitelist = {'ds'}
c.Authenticator.admin_users = {'dstudio'}
# c.Authenticator.whitelist = {'ds'}
c.Authenticator.check_common_password = True
c.Authenticator.minimum_password_length = 6
c.Authenticator.allowed_failed_logins = 3

## Docker spawner
c.JupyterHub.spawner_class = 'dockerspawner.DockerSpawner'
c.DockerSpawner.image = os.environ['DOCKER_JUPYTERLAB_IMAGE']
# Connect containers to this Docker network
network_name = os.environ['DOCKER_NETWORK_NAME']
c.DockerSpawner.use_internal_ip = True
c.DockerSpawner.network_name = network_name
# Pass the network name as argument to spawned containers
c.DockerSpawner.extra_host_config = { 'network_mode': network_name }
# Remove containers once they are stopped
c.DockerSpawner.remove_containers = True
# For debugging arguments passed to spawned containers
c.DockerSpawner.debug = True
# c.Spawner.cmd = ['jupyter', 'labhub']

# user data persistence
# see https://github.com/jupyterhub/dockerspawner#data-persistence-and-dockerspawner
notebook_dir = os.environ.get('DOCKER_NOTEBOOK_DIR') or '/home/jovyan/work'
c.DockerSpawner.notebook_dir = notebook_dir
c.DockerSpawner.volumes = {os.environ.get('HOST_NOTEBOOK_DIR')+'/{username}': {"bind": notebook_dir, "mode": "rw"}}
# c.DockerSpawner.volumes = { 'jupyterhub-user-{username}': notebook_dir }

# # Other stuff
c.Spawner.cpu_limit = 1
c.Spawner.mem_limit = '2G'

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
