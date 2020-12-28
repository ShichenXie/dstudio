FROM rocker/geospatial

ENV NB_USER rstudio
ENV CONDA_DIR /srv/conda

# Set ENV for all programs...
ENV PATH ${CONDA_DIR}/bin:$PATH
# And set ENV for R! It doesn't read from the environment...
RUN echo "PATH=${PATH}" >> /usr/local/lib/R/etc/Renviron

# Add PATH to /etc/profile so it gets picked up by the terminal
RUN echo "PATH=${PATH}" >> /etc/profile
RUN echo "export PATH" >> /etc/profile

# The `rsession` binary that is called by jupyter-rsession-proxy to start R
# doesn't seem to start without this being explicitly set
ENV LD_LIBRARY_PATH /usr/local/lib/R/lib

ENV HOME /home/${NB_USER}
WORKDIR ${HOME}

# Install packages needed by nbpdfexport
# Default fonts seem ok, we just install an emoji font
# Can't use fonts-noto-color-emoji since this is based
# on debian stretch
# tcl/tk needed by vioplot/sm (rocker #316)
RUN apt-get update && \
    apt-get install --yes \
		gdebi-core && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

# Download and install shiny server
RUN wget --no-verbose https://download3.rstudio.org/ubuntu-14.04/x86_64/shiny-server-1.5.12.933-amd64.deb -O ss.deb && \
    gdebi -n ss.deb && \
    rm -f ss.deb

COPY install-miniconda.bash /tmp/install-miniconda.bash
RUN /tmp/install-miniconda.bash

USER ${NB_USER}

RUN pip install --no-cache-dir \
		"notebook>=6" \
		git+https://github.com/ryanlovett/jupyter-shiny-proxy

COPY --chown=${NB_USER} app app

CMD jupyter notebook --ip=*
