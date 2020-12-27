# https://github.com/jupyter/docker-stacks
# FROM jupyter/datascience-notebook:r-4.0.3
FROM jupyter/scipy-notebook:399cbb986c6b

WORKDIR /
USER root

# set local source.list
RUN mv /etc/apt/sources.list /etc/apt/sources.list.bak
COPY ./linux_source/sources_ubuntu.list /etc/apt/sources.list

# datascience-notebook without julia =====================================#
# https://github.com/jupyter/docker-stacks/blob/master/datascience-notebook/Dockerfile

# install r/pkgs ---------------------------------------------------------#
RUN apt-get update && \
    apt-get install -y --no-install-recommends \
    fonts-dejavu \
    gfortran \
    gcc && \
    apt-get clean && rm -rf /var/lib/apt/lists/*

USER $NB_UID
RUN conda install --quiet --yes \
    'r-base=4.0.3'  \
    'r-caret' \
    'r-crayon' \
    'r-devtools' \
    'r-forecast*' \ 
    'r-hexbin' \
    'r-htmltools' \
    'r-htmlwidgets' \ 
    'r-irkernel' \
    'r-nycflights13' \
    'r-randomforest' \
    'r-rcurl' \
    'r-rmarkdown' \
    'r-rsqlite' \
    'r-shiny' \
    'r-tidyverse' \
    'rpy2' && \
    conda clean --all -f -y && \
    fix-permissions "${CONDA_DIR}" && \
    fix-permissions "/home/${NB_USER}"

# install rstudio server -------------------------------------------------#
USER root

RUN apt-get update &&\
    apt-get install -y gdebi-core &&\
    wget https://download2.rstudio.org/server/bionic/amd64/rstudio-server-1.2.5042-amd64.deb &&\
    gdebi --non-interactive rstudio-server-1.2.5042-amd64.deb &&\
    rm rstudio-server-1.2.5042-amd64.deb &&\
    apt-get clean && rm -rf /var/lib/apt/lists/*

RUN R --quiet -e "install.packages(c('png', 'reticulate'), repos = 'https://mirrors.tuna.tsinghua.edu.cn/CRAN/')" &&\
    rm -rf /tmp/*

ENV PATH=$PATH:/usr/lib/rstudio-server/bin

# install nodejs/jupyterhub ==============================================#
RUN conda install -c conda-forge jupyterhub=1.2.2 &&\
    conda clean --tarballs -y 
RUN pip install -i https://pypi.tuna.tsinghua.edu.cn/simple --no-cache-dir \
        jupyter_nbextensions_configurator \
        dockerspawner \
        jupyter-rsession-proxy

# nativeauthenticator ----------------------------------------------------#
# https://native-authenticator.readthedocs.io/en/latest/
# RUN git clone https://github.com/jupyterhub/nativeauthenticator.git /tmp/nativeauthenticator
COPY ./nativeauthenticator /tmp/nativeauthenticator
RUN pip install /tmp/nativeauthenticator &&\
    rm -rf /tmp/*
# https://github.com/jtpio/jupyterlab-python-file
RUN jupyter labextension install jupyterlab-python-file 

# config =================================================================#
# create group/user
RUN groupadd -g 200 ds &&\ 
    userdel -r jovyan &&\ 
    useradd -m -g users -G ds -d /home/dstudio dstudio 
    
    
# jupyterhub config
RUN jupyterhub --generate-config
COPY ./config/jupyterhub_config.py /
CMD jupyterhub -f jupyterhub_config.py
# jupyter notebook config # jupyter --paths
RUN jupyter notebook --generate-config
COPY ./config/jupyter_notebook_config.py /opt/conda/etc/jupyter/

# rstudio server config
COPY ./config/rstudio-prefs.json /etc/rstudio/
# COPY ./config/rserver.conf /etc/rstudio/
# R kernel available to jupyter 
# R startup # https://rviews.rstudio.com/2017/04/19/r-for-enterprise-understanding-r-s-startup/
RUN R --quiet -e "IRkernel::installspec(user=FALSE)" &&\
    echo 'options(repos = c(CRAN = "https://cran.rstudio.com/", CRANextra = "https://mirrors.tuna.tsinghua.edu.cn/CRAN/"))' >> /opt/conda/lib/R/etc/Rprofile.site && \
    echo 'RETICULATE_PYTHON = "/opt/conda/bin/python"' >> /opt/conda/lib/R/etc/Renviron.site


# modify r/py folder permissions
RUN chmod -R 775 /opt/conda/lib/R &&\ 
    chmod -R 775 /opt/conda/lib/python* 


EXPOSE 8888
CMD jupyterhub


# notes =================================================================#
# R # /opt/conda/bin/R
# .libPaths(); # /opt/conda/lib/R/library
# python # /opt/conda/bin/python
# import site; site.getsitepackages(); # /opt/conda/lib/python3.8/site-packages

# docker build -t shichenxie/dstudio:0.1.1 .
# mkdir -p $HOME/docker/dstudio_home
# docker run -d -p 8888:8888 -v $HOME/docker/dstudio_home:/home --restart=always --name dstudio shichenxie/dstudio:0.1.1