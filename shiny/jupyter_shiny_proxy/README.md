# jupyter-shiny-proxy

**jupyter-shiny-proxy** leverages jupyter-server-proxy to proxy Shiny applications inside a Jupyter server.

![Screenshot](screenshot.png)

If you have a JupyterHub deployment, jupyter-shiny-proxy can take advantage of JupyterHub's existing authenticator and spawner to launch Shiny applications in users' Jupyter environments. You can also run this from within Jupyter.
[RStudio Connect](https://rstudio.com/products/connect/evaluation) and [Shinyapps.io](https://www.shinyapps.io/) are other options from the creator of SHiny.

## Installation

### Pre-reqs

#### Install shiny-server
[Download](https://rstudio.com/products/shiny/download-server/) the corresponding package for your platform.

### Install jupyter-shiny-proxy

Install the library:
```
pip install jupyter-shiny-proxy
```
