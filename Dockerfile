FROM rocker/verse:4.0.1

# set local source.list
RUN mv /etc/apt/sources.list /etc/apt/sources.list.bak
COPY ./linux_source/sources_ubuntu.list /etc/apt/sources.list

# set local cran url
ARG cran_loc
ENV cran_loc https://mirrors.tuna.tsinghua.edu.cn/CRAN/

# install nodejs ---------------------------------------------------------#
RUN apt-get update && \
    apt-get install -y curl cmake && \
    curl -sL https://deb.nodesource.com/setup_10.x -o nodesource_setup.sh && \
    bash nodesource_setup.sh && \
    apt-get install -y nodejs && \
    rm -rf /var/lib/apt/lists/*

# install anaconda3 ------------------------------------------------------#
# https://hub.docker.com/r/continuumio/anaconda3/dockerfile
ENV LANG=C.UTF-8 LC_ALL=C.UTF-8
ENV PATH /opt/conda/bin:$PATH

RUN apt-get update && \
    apt-get install -y wget bzip2 ca-certificates \
    libglib2.0-0 libxext6 libsm6 libxrender1 \
    git mercurial subversion && \
    rm -rf /var/lib/apt/lists/*

RUN wget --quiet https://mirrors.tuna.tsinghua.edu.cn/anaconda/archive/Anaconda3-5.3.1-Linux-x86_64.sh -O ~/anaconda.sh && \
    /bin/bash ~/anaconda.sh -b -p /opt/conda && \
    rm ~/anaconda.sh && \
    ln -s /opt/conda/etc/profile.d/conda.sh /etc/profile.d/conda.sh && \
    echo ". /opt/conda/etc/profile.d/conda.sh" >> ~/.bashrc && \
    echo "conda activate base" >> ~/.bashrc

RUN apt-get install -y curl grep sed dpkg && \
    TINI_VERSION=`curl https://github.com/krallin/tini/releases/latest | grep -o "/v.*\"" | sed 's:^..\(.*\).$:\1:'` && \
    curl -L "https://github.com/krallin/tini/releases/download/v${TINI_VERSION}/tini_${TINI_VERSION}.deb" > tini.deb && \
    dpkg -i tini.deb && \
    rm tini.deb && \
    apt-get clean

ENTRYPOINT [ "/usr/bin/tini", "--" ]
CMD [ "/bin/bash" ]

# install jupyterhub -----------------------------------------------------#
ENV CONDA_DIR /opt/conda

RUN conda install -y --no-deps pip
RUN python3 -m venv ${CONDA_DIR} && \
    pip3 install -i https://pypi.tuna.tsinghua.edu.cn/simple --no-cache-dir \
         dlib xgboost sklearn2pmml sklearn_pandas \
         jupyterhub \
         jupyter-rsession-proxy \
         jupyter_nbextensions_configurator \
         dockerspawner 
RUN npm install -g configurable-http-proxy

# R path -----------------------------------------------------------------#
RUN echo "PATH=${PATH}" >> /usr/local/lib/R/etc/Renviron 
ENV LD_LIBRARY_PATH /usr/local/lib/R/lib

RUN R --quiet -e "install.packages('IRkernel', repos = '$cran_loc')" && \
    R --quiet -e "IRkernel::installspec(user=FALSE)"#, prefix='${CONDA_DIR}/bin' && \
    R --quiet -e "install.packages(c('png', 'reticulate', 'blastula', 'cronR', 'scorecard', 'xgboost'), repos = '$cran_loc')" && \
    rm -rf /tmp/*

# database drivers -------------------------------------------------------#
# r/py packages
RUN R --quiet -e "install.packages(c('odbc', 'RJDBC', 'RPostgres'), repos = '$cran_loc')" && \ 
    rm -rf /tmp/*
    
RUN python3 -m venv ${CONDA_DIR} && \
    pip3 install -i https://pypi.tuna.tsinghua.edu.cn/simple --no-cache-dir \
         sqlalchemy JayDeBeApi psycopg2 cx_Oracle pandas --force

# https://blogs.oracle.com/r/r-to-oracle-database-connectivity:-use-roracle-for-both-performance-and-scalability
RUN mkdir -p /opt/dbjar && \
    mkdir -p /opt/dbjar/hive
ADD ./db/oracle /opt/dbjar/oracle

# install package from local file ---------------------------------------#
# nativeauthenticator 
# https://native-authenticator.readthedocs.io/en/latest/
# RUN git clone https://github.com/jupyterhub/nativeauthenticator.git /tmp/nativeauthenticator
ADD ./jupyter/nativeauthenticator /tmp/nativeauthenticator
RUN pip3 install /tmp/nativeauthenticator

# config ------------------------------------------------------#
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


# create home folder 
RUN useradd -m -d /home/dstudio dstudio
# set the permissions of r-library folder
RUN chmod -R 777 /usr/local/lib/R 
    

EXPOSE 8000
CMD jupyterhub


# docker build -t shichenxie/dstudio .
# docker run -d -p 8000:8000 -v $HOME/docker/dstudio:/home --restart=always --name dstudio shichenxie/dstudio