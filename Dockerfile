########################################################################
# https://github.com/rocker-org/binder
# https://blog.csdn.net/weixin_41164688/article/details/101067324

FROM shichenxie/scorecard

RUN R --quiet -e "install.packages(c('png', 'reticulate', 'blastula', 'cronR'), repos = 'https://mirrors.tuna.tsinghua.edu.cn/CRAN/')"

# install nodejs #######################################################
RUN apt-get update && \
    apt-get -y install curl && \
    curl -sL https://deb.nodesource.com/setup_10.x -o nodesource_setup.sh && \
    bash nodesource_setup.sh && \
    apt-get -y install nodejs 

# install anaconda3 ####################################################
# https://hub.docker.com/r/continuumio/anaconda3/dockerfile
ENV LANG=C.UTF-8 LC_ALL=C.UTF-8
ENV CONDA_DIR /opt/conda
ENV PATH ${CONDA_DIR}/bin:$PATH

RUN apt-get update --fix-missing && \
    apt-get install -y wget bzip2 ca-certificates \
    libglib2.0-0 libxext6 libsm6 libxrender1 \
    git mercurial subversion

RUN wget --quiet https://mirrors.tuna.tsinghua.edu.cn/anaconda/archive/Anaconda3-5.3.0-Linux-x86_64.sh -O ~/anaconda.sh && \
    /bin/bash ~/anaconda.sh -b -p ${CONDA_DIR} && \
    rm ~/anaconda.sh && \
    ln -s ${CONDA_DIR}/etc/profile.d/conda.sh /etc/profile.d/conda.sh && \
    echo ". ${CONDA_DIR}/etc/profile.d/conda.sh" >> ~/.bashrc && \
    echo "conda activate base" >> ~/.bashrc

RUN apt-get install -y curl grep sed dpkg cmake && \
    TINI_VERSION=`curl https://github.com/krallin/tini/releases/latest | grep -o "/v.*\"" | sed 's:^..\(.*\).$:\1:'` && \
    curl -L "https://github.com/krallin/tini/releases/download/v${TINI_VERSION}/tini_${TINI_VERSION}.deb" > tini.deb && \
    dpkg -i tini.deb && \
    rm tini.deb && \
    apt-get clean

ENTRYPOINT [ "/usr/bin/tini", "--" ]
CMD [ "/bin/bash" ]

# install jupyterhub ####################################################
RUN conda install --no-deps pip
RUN python3 -m venv ${CONDA_DIR} && \
    pip3 install -i https://pypi.tuna.tsinghua.edu.cn/simple --no-cache-dir \
         dlib xgboost sklearn2pmml sklearn_pandas\
         jupyterhub \
         jupyter-rsession-proxy \
         jupyter_nbextensions_configurator \
         dockerspawner
RUN npm install -g configurable-http-proxy

# jupyterhub_config
RUN jupyterhub --generate-config

# 
# ENV JPH_DIR /etc/jupyterhub
# RUN mkdir -p ${JPH_DIR}
# COPY jupyterhub_config.py ${JPH_DIR}/jupyterhub_config.py
# RUN echo jupyterhub -f ${JPH_DIR}/jupyterhub_config.py > jupyterhub.sh && \
#     echo su -l root ${JPH_DIR}/jupyterhub.sh \& >> /etc/rc.local
    
# authenticator  #######################################################
# native authenticator
# https://native-authenticator.readthedocs.io/en/latest/quickstart.html
# RUN git clone https://github.com/jupyterhub/nativeauthenticator.git /temp 
ADD nativeauthenticator /tmp/nativeauthenticator
RUN mv /tmp/nativeauthenticator ${CONDA_DIR}/bin/nativeauthenticator && \
    pip --no-cache-dir install -e ${CONDA_DIR}/bin/nativeauthenticator 

# R path ###############################################################
RUN echo "PATH=${PATH}" >> /usr/local/lib/R/etc/Renviron
ENV LD_LIBRARY_PATH /usr/local/lib/R/lib

RUN R --quiet -e "install.packages('IRkernel', repos = 'https://mirrors.tuna.tsinghua.edu.cn/CRAN/')" && \
    R --quiet -e "IRkernel::installspec(user=FALSE)"#, prefix='${CONDA_DIR}/bin'

RUN R --quiet -e "install.packages(c('odbc', 'sparklyr'), repos = 'https://mirrors.tuna.tsinghua.edu.cn/CRAN/')"


# transwarp odbc driver ################################################
# http://support.transwarp.cn/t/odbc-jdbc/477
COPY inceptor-connector-odbc-5.0.0-1.el6.x86_64.rpm /
RUN apt-get update --fix-missing && \
    apt-get -y install alien && \
    alien -i inceptor-connector-odbc-5.0.0-1.el6.x86_64.rpm
# copy all files to /etc
RUN cp -a /usr/local/inceptor/. /etc/

# jupyterhub config ####################################################
COPY jupyterhub_config.py /
CMD jupyterhub -f jupyterhub_config.py

# Setup application
EXPOSE 8000
CMD jupyterhub


# setting #############################################################
# docker build -t dstudio .
# mkdir -p $HOME/docker/dstudio
# docker run -d -p 8000:8000 -v $HOME/docker/dstudio:/home --restart=always --name dstudio dstudio

# # after launch rstudio in browser, otherwise rstudio cant be entered by multiple uers
# docker exec -it dstudio bash
# chmod -R 777 /tmp/rstudio-server/secure-cookie-key

# Authorization Area
# http://localhost:8000/hub/authorize

# useradd --create-home xieshichen
# passwd xieshichen

# adduser xieshichen # passwd xieshichen
# adduser xieshichen ds
