FROM jupyterhub/jupyterhub:1.3.0

# pkgs
RUN python3 -m pip install --no-cache \
	jupyter_client \
    dockerspawner \
    jupyterhub-idle-culler &&\
    rm -rf /tmp/*

# nativeauthenticator
RUN python3 -m pip install --upgrade https://github.com/jupyterhub/nativeauthenticator/tarball/master &&\
    rm -rf /tmp/*

# config -----------------------------------------------------------------#
USER root
RUN mkdir -p /srv/jupyterhub/ &&\
    mkdir -p /opt/jupyterhub/
WORKDIR /srv/jupyterhub

# EXPOSE 8888
COPY ./jupyterhub_config.py /opt/jupyterhub/jupyterhub_config.py
CMD ["jupyterhub", "-f", "/opt/jupyterhub/jupyterhub_config.py"]

# docker build -t shichenxie/dstudio_hub:1.3.0 .
# docker save shichenxie/dstudio_hub:1.2.2 -o ~/Downloads/dstudio_hub.tar