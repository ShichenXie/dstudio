# Configuration file for JupyterHub
import os
import sys
import nativeauthenticator

labimage = os.environ["LAB_IMAGE"]


from dockerspawner import DockerSpawner
ops = ""
for img in labimage.split(","):
    disp = img.split("/")
    disp = disp[1] if len(disp) ==2 else img
    ops += """<option value="{img}">{disp}</option>\n""".format(img=img, disp=disp)
class DemoFormSpawner(DockerSpawner):
    def _options_form_default(self):
        return """
        <label for="stack">Select your desired stack</label>
        <select name="stack" size="1">{stack}</select>
        """.format(stack=ops)

    def options_from_form(self, formdata):
        options = {}
        options['stack'] = formdata['stack']
        container_image = ''.join(formdata['stack'])
        print("SPAWN: " + container_image + " IMAGE" )
        self.container_image = container_image
        return options


c = get_config()  # noqa: F821

# We rely on environment variables to configure JupyterHub so that we
# avoid having to rebuild the JupyterHub container every time we change a
# configuration parameter.

# Spawn single-user servers as Docker containers
# c.JupyterHub.spawner_class = "dockerspawner.DockerSpawner"
c.JupyterHub.spawner_class = DemoFormSpawner

# Spawn containers from this image
# c.DockerSpawner.image = labimage # os.environ["LAB_IMAGE"]

# Connect containers to this Docker network
network_name = os.environ["LAB_NETWORK_NAME"]
c.DockerSpawner.use_internal_ip = True
c.DockerSpawner.network_name = network_name

# Explicitly set notebook directory because we'll be mounting a volume to it.
# Most `jupyter/docker-stacks` *-notebook images run the Notebook server as
# user `jovyan`, and set the notebook directory to `/home/jovyan/work`.
# user data persistence
# see https://github.com/jupyterhub/dockerspawner#data-persistence-and-dockerspawner
lab_work_dir = '/home/jovyan/work' # os.environ.get('DOCKER_NOTEBOOK_DIR') or '/home/jovyan/work' #  
c.DockerSpawner.notebook_dir = lab_work_dir

# Mount the real user's Docker volume on the host to the notebook user's
# notebook directory in the container
# share volume 
lab_share_dir = '/home/jovyan/share'
volumes_dict = {'jupyterlab-share': lab_share_dir}
# user volume
if 'LAB_DIR_HOST' in list(os.environ):
  volumes_dict[os.environ['LAB_DIR_HOST']+'/{username}'] = {"bind": lab_work_dir, "mode": "rw"}
else:
  volumes_dict['jupyterlab-user-{username}'] = lab_work_dir
c.DockerSpawner.volumes = volumes_dict

# Remove containers once they are stopped
def str2bool(v):
  return v.lower() in ("yes", "true", "t", "1", "True", "TRUE")
rmcont = str2bool(os.environ['LAB_CONTAINER_REMOVE']) if 'LAB_CONTAINER_REMOVE' in list(os.environ) else True
c.DockerSpawner.remove = rmcont

# For debugging arguments passed to spawned containers
c.DockerSpawner.debug = True
# c.DockerSpawner.default_url = os.environ['HUB_DEFAULT_URL']

# User containers will access hub by container name on the Docker network
c.JupyterHub.hub_ip = "jupyterhub"
c.JupyterHub.hub_port = 8080

# Persist hub data on volume mounted inside container
c.JupyterHub.cookie_secret_file = "/data/jupyterhub_cookie_secret"
c.JupyterHub.db_url = "sqlite:////data/jupyterhub.sqlite"

# Authenticate users with Native Authenticator
c.JupyterHub.authenticator_class = "nativeauthenticator.NativeAuthenticator"

# Allow anyone to sign-up without approval
c.NativeAuthenticator.open_signup = str2bool(os.environ['HUB_OPEN_SIGNUP'])

# authenticator
c.Authenticator.admin_users = {os.environ['HUB_ADMIN']}
c.NativeAuthenticator.check_common_password = True
c.NativeAuthenticator.minimum_password_length = 6
c.NativeAuthenticator.allowed_failed_logins = 3


# # Other stuff
# c.Spawner.cpu_limit = 1
# c.Spawner.mem_limit = '2G'

# c.Spawner.http_timeout = 600
# c.Spawner.start_timeout = 600
# Services
hub_timeout = '--timeout='+os.environ['HUB_TIMEOUT']
c.JupyterHub.services = [
    {
        'name': 'idle-culler1',
        'admin': True,
        'command': [sys.executable, '-m', 'jupyterhub_idle_culler', hub_timeout],
    }
]