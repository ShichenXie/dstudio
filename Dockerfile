FROM rocker/verse:3.6.3
# FROM rocker/verse:4.0.3

RUN R --quiet -e "install.packages(c('scorecard', 'xgboost', 'h2o'), repos = 'https://mirrors.tuna.tsinghua.edu.cn/CRAN/')" && \
    rm -rf /tmp/*
  
# set local source.list
RUN mv /etc/apt/sources.list /etc/apt/sources.list.bak
COPY sources.list /etc/apt/sources.list

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

RUN conda install --no-deps pip
RUN python3 -m venv ${CONDA_DIR} && \
    pip3 install -i https://pypi.tuna.tsinghua.edu.cn/simple --no-cache-dir \
         dlib xgboost sklearn2pmml sklearn_pandas \
         jupyterhub \
         jupyter-rsession-proxy \
         jupyter_nbextensions_configurator \
         dockerspawner
RUN npm install -g configurable-http-proxy

# jupyterhub_config
RUN jupyterhub --generate-config
    
# authenticator ----------------------------------------------------------#
# native authenticator
# https://native-authenticator.readthedocs.io/en/latest/quickstart.html
# RUN git clone https://github.com/jupyterhub/nativeauthenticator.git /temp 
ADD nativeauthenticator /tmp/nativeauthenticator
RUN mv /tmp/nativeauthenticator ${CONDA_DIR}/bin/nativeauthenticator && \
    pip3 install -e ${CONDA_DIR}/bin/nativeauthenticator --no-cache-dir 

# R path -----------------------------------------------------------------#
RUN echo "PATH=${PATH}" >> /usr/local/lib/R/etc/Renviron 
ENV LD_LIBRARY_PATH /usr/local/lib/R/lib
RUN chmod -R 777 /usr/local/lib/R

RUN R --quiet -e "install.packages('IRkernel', repos = 'https://mirrors.tuna.tsinghua.edu.cn/CRAN/')" && \
    R --quiet -e "IRkernel::installspec(user=FALSE)"#, prefix='${CONDA_DIR}/bin' && \
    R --quiet -e "install.packages(c('png', 'reticulate', 'blastula', 'cronR'), repos = 'https://mirrors.tuna.tsinghua.edu.cn/CRAN/')" && \
    rm -rf /tmp/*

# database drivers -------------------------------------------------------#
# r/py packages
RUN R --quiet -e "install.packages(c('odbc', 'RJDBC', 'RPostgres'), repos = 'https://mirrors.tuna.tsinghua.edu.cn/CRAN/')" && \ 
    rm -rf /tmp/*
    
RUN python3 -m venv ${CONDA_DIR} && \
    pip3 install -i https://pypi.tuna.tsinghua.edu.cn/simple --no-cache-dir \
         sqlalchemy JayDeBeApi psycopg2 cx_Oracle pandas --force

# https://blogs.oracle.com/r/r-to-oracle-database-connectivity:-use-roracle-for-both-performance-and-scalability
RUN mkdir -p /opt/dbjar && \
    mkdir -p /opt/dbjar/hive
ADD oracle/oracle /opt/dbjar/oracle

# jupyterhub config ------------------------------------------------------#
COPY jupyterhub_config.py /
CMD jupyterhub -f jupyterhub_config.py

# Setup application
RUN useradd --create-home dstudio

EXPOSE 8000
CMD jupyterhub


