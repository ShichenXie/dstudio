FROM jupyterhub/jupyterhub:1.2.2

# pkgs
RUN python3 -m pip install --no-cache \
	jupyter_client==6.1.11 \
    dockerspawner==0.11.1 \
    jupyterhub-idle-culler &&\
    rm -rf /tmp/*

# nativeauthenticator
# RUN git clone https://github.com/jupyterhub/nativeauthenticator.git /tmp/nativeauthenticator
COPY ./nativeauthenticator /tmp/nativeauthenticator
RUN pip install /tmp/nativeauthenticator &&\
    rm -rf /tmp/*

# config -----------------------------------------------------------------#
WORKDIR /
USER root
RUN mkdir -p /srv/jupyterhub/
COPY ./jupyterhub_config.py /srv/jupyterhub/jupyterhub_config.py

# EXPOSE 8888
CMD ["jupyterhub", "-f", "/srv/jupyterhub/jupyterhub_config.py"]
