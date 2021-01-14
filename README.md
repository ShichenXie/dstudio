
# dstudio

<!-- badges: start -->
<!-- badges: end -->

dstudio 是一个将 rstudio server 和 jupyterlab 打包在一起的 docker 容器。极大的简化了在线建模分析平台的搭建。部署在服务器上之后，支持多用户通过浏览器远程登陆 R 与 python 环境，一方面可以充分利用服务器的计算资源，另一方面便于团队内成员建模分析环境的配置与管理。需要说明的是 [rstudio server Pro](https://rstudio.com/products/rstudio-server-pro/) 提供了更为全面的功能与服务。本项目主要是提供了一个开箱即用的免费开源选项。

![login](./img/login.png)

## 如何开始

首先需要配置 docker 环境，其安装过程参见[docker 在线文档](https://docs.docker.com/get-started/)。

安装好 docker 之后下载本项目 repo，在终端中进入本项目文件夹并运行以下代码，就可以通过浏览器访问 rstudio server 和 jupyterlab 了。如果部署在本地电脑上，访问地址为 `http://localhost:8000/`；如果部署在服务器上，将 localhost 替换为对应服务器的ip地址。
```
docker pull shichenxie/dstudio_lab:ds
docker-compose up -d
```

## 登陆过程

默认的用户名为 dstudio，该账号有管理员权限。密码需要通过点击 Signup 进入注册页面创建用户时生成。然后点击 Login，回到登陆页输入 dstudio 和设定的密码。登陆之后进入 jupyterLab 页面，可在下拉菜单 File 中退出登陆 (Log Out)，或进入管理页面 (Hub Control Panel)。该页面对应 url 为 `http://localhost:8000/user/dstudio/lab`，可以将其中最后的 lab 修改为 rstudio 进入 rstudio server 页面。

![jupyter](./img/jupyter.png)
![rstudio](./img/rstudio.png)

## 创建新用户

先由新用户在登陆页面 `http://localhost:8000/` 点击 Signup，进入注册页面新建用户并设定密码，假设新用户名为 test。然后由管理员 dstudio 登陆，并跳转至 `http://localhost:8000/hub/authorize` 页面进行审批，即完成了新用户的创建。

## 修改密码

用原密码登陆之后，进入 `http://localhost:8000/hub/change-password` 页面可以更新密码。

## 贡献与参考

如果您对本项目感兴趣，欢迎star。如果有任何想法可以提交 issue 或者 pr。

本项目适合中小型团队搭建在线建模分析平台，参考了 [defeo/jupyterhub-docker](https://github.com/defeo/jupyterhub-docker) 与 [jupyterhub/jupyterhub-deploy-docker](https://github.com/jupyterhub/jupyterhub-deploy-docker)；对于大型团队需要集群扩展的可以参考 [zero-to-jupyterhub-k8s](https://zero-to-jupyterhub.readthedocs.io/en/stable/) 项目。
类似的项目还有 [ShinyStudio](https://github.com/dm3ll3n/ShinyStudio)，不过是基于  [shinyproxy](https://www.shinyproxy.io/) 开发的。

本项目参考了以下内容或项目：
- [Docker — 从入门到实践](https://yeasy.gitbook.io/docker_practice/)
- [A Docker tutorial for reproducible research.](http://ropenscilabs.github.io/r-docker-tutorial/)
- [Jupyter](https://jupyter.org/), [JupyterHub](https://jupyterhub.readthedocs.io/), [DockerSpawner](https://jupyterhub-dockerspawner.readthedocs.io/)
- [JupyterHub Native Authenticator](https://native-authenticator.readthedocs.io/en/latest/)
- [jupyter-rsession-proxy](https://github.com/jupyterhub/jupyter-rsession-proxy)
- [RStudio Server Pro - Administration Guide](https://docs.rstudio.com/ide/server-pro/latest/)
- [Version-stable Rocker images](https://github.com/rocker-org/rocker-versioned)

