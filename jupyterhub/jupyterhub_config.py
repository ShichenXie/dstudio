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
# Connect containers to this Docker network
network_name = os.environ['DOCKER_NETWORK_NAME']
c.DockerSpawner.use_internal_ip = True
c.DockerSpawner.network_name = network_name
c.DockerSpawner.extra_host_config = { 'network_mode': network_name }
# Remove containers once they are stopped
c.DockerSpawner.remove = True
# For debugging arguments passed to spawned containers
c.DockerSpawner.debug = True
c.DockerSpawner.cmd = 'start-singleuser.sh'
c.DockerSpawner.default_url = os.environ['HUB_DEFAULT_URL']

# user data persistence
# see https://github.com/jupyterhub/dockerspawner#data-persistence-and-dockerspawner
lab_work_dir = '/home/jovyan/work' # os.environ.get('DOCKER_NOTEBOOK_DIR') or '/home/jovyan/work'
c.DockerSpawner.notebook_dir = lab_work_dir

volumes_dict = {}
if 'HOST_WORK_DIR' in list(os.environ):
  volumes_dict[os.environ['HOST_WORK_DIR']+'/{username}'] = {"bind": lab_work_dir, "mode": "rw"}
else:
  volumes_dict['jupyterlab-user-{username}'] = lab_work_dir
if 'LAB_SHARE_DIR' in list(os.environ):
  volumes_dict['jupyterlab-share'] = os.environ['LAB_SHARE_DIR']
c.DockerSpawner.volumes = volumes_dict


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
c.Authenticator.admin_users = {os.environ['HUB_ADMIN_USER']}
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
