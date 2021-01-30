FROM jupyterhub/jupyterhub:1.2.2

# pkgs
RUN python3 -m pip install --no-cache \
	jupyter_client \
    dockerspawner \
    jupyterhub-idle-culler &&\
    rm -rf /tmp/*

# nativeauthenticator
# RUN git clone https://github.com/jupyterhub/nativeauthenticator.git /tmp/nativeauthenticator
COPY ./nativeauthenticator /tmp/nativeauthenticator
RUN pip install /tmp/nativeauthenticator &&\
    rm -rf /tmp/*

# config -----------------------------------------------------------------#
USER root
RUN mkdir -p /srv/jupyterhub/ &&\
    mkdir -p /opt/jupyterhub/
WORKDIR /srv/jupyterhub

# EXPOSE 8888
COPY ./jupyterhub_config.py /opt/jupyterhub/jupyterhub_config.py
CMD ["jupyterhub", "-f", "/opt/jupyterhub/jupyterhub_config.py"]

# docker build -t shichenxie/dstudio_hub:1.2.2 .
# docker save shichenxie/dstudio_hub:1.2.2 -o ~/Downloads/dstudio_hub.tar