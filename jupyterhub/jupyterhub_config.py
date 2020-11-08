# jupyterhub_config.py
c = get_config()

c.JupyterHub.ip = '0.0.0.0'
c.JupyterHub.port = 8000
c.JupyterHub.statsd_prefix = 'jupyterhub'

# authenticator
c.JupyterHub.authenticator_class = 'nativeauthenticator.NativeAuthenticator'

# change from JupyterHub to jupyter notebook
c.Spawner.default_url = '/tree'
c.Spawner.debug = True

# Administrators - set of users who can administer the Hub itself
c.Authenticator.admin_users = {"dstudio"}
# c.Authenticator.whitelist = {"dstudio", 'test'}

# c.Authenticator.check_common_password = False
c.Authenticator.minimum_password_length = 6

# c.LocalAuthenticator.group_whitelist = {'ds'}
c.LocalAuthenticator.create_system_users = True
# 
c.PAMAuthenticator.encoding ='utf8'


