# https://github.com/jupyter/docker-stacks
FROM jupyter/datascience-notebook:r-4.0.3

WORKDIR /
USER root
RUN userdel -r jovyan

# set local source.list
RUN mv /etc/apt/sources.list /etc/apt/sources.list.bak
COPY ./linux_source/sources_ubuntu.list /etc/apt/sources.list

# install nodejs/jupyterhub ----------------------------------------------#
RUN apt-get update && \
    apt-get install -y cmake && \
    curl -sL https://deb.nodesource.com/setup_10.x -o nodesource_setup.sh && \
    bash nodesource_setup.sh && \
    apt-get install -y nodejs && \
    rm -rf /var/lib/apt/lists/*

RUN pip install -i https://pypi.tuna.tsinghua.edu.cn/simple --no-cache-dir \
        jupyterhub jupyter_nbextensions_configurator dockerspawner 
RUN npm install -g configurable-http-proxy

# nativeauthenticator ----------------------------------------------------#
# https://native-authenticator.readthedocs.io/en/latest/
# RUN git clone https://github.com/jupyterhub/nativeauthenticator.git /tmp/nativeauthenticator
ADD ./nativeauthenticator /tmp/nativeauthenticator
RUN pip install /tmp/nativeauthenticator --no-cache-dir

# config -----------------------------------------------------------------#
# jupyterhub config
RUN jupyterhub --generate-config
COPY ./config/jupyterhub_config.py /
CMD jupyterhub -f jupyterhub_config.py

# jupyter notebook config # jupyter --paths
RUN jupyter notebook --generate-config
COPY ./config/jupyter_notebook_config.py /opt/conda/etc/jupyter/

# create home folder & r folder permissions
RUN groupadd -g 300 ds &&\ 
    useradd -m -g ds -d /home/dstudio dstudio &&\
    chmod -R 775 /opt/conda/lib/R/library

EXPOSE 8888
CMD jupyterhub


# R # /opt/conda/bin/R
# .libPaths(); # /opt/conda/lib/R/library
# python # /opt/conda/bin/python
# import site; site.getsitepackages(); # /opt/conda/lib/python3.8/site-packages

# docker build -t dstudio_jupyter .
# docker run -d -p 8888:8888 --restart=always --name dstudio_jupyter dstudio_jupyter