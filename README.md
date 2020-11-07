
# dstudio

<!-- badges: start -->
<!-- badges: end -->

dstudio 是一个将 rstudio server 和 jupyter notebok 打包在一起的 docker 容器。极大的简化了在线建模分析平台的搭建。部署在服务器上之后，支持多用户通过浏览器远程登陆 R 与 python 环境，一方面可以充分利用服务器的计算资源，另一方面减少了团队内成员配置建模分析环境的烦恼。需要说明的是 [rstudio server 专业版](https://rstudio.com/products/rstudio-server-pro/)提供了更为全面的功能与支持。本项目相对来说功能并没有那么强大，但提供了一个开箱即用的开源免费选项。

# 如何开始

首先需要配置 docker 环境，其安装过程参见[docker 在线文档](https://docs.docker.com/get-started/)。

安装好 docker 之后，在本地新建文件夹作为 docker 容器指向的用户目录。即在本地保存dstudio运行过程中的用户文件，否则docker容器删除之后，用户的建模分析结果就会丢失了。
```
mkdir -p $HOME/docker/dstudio
```

然后在终端运行以下代码，就可以通过浏览器访问 rstudio server 和 jupyter notebook 了。如果部署在本地电脑上，访问地址为`http://localhost:8000/`；如果部署在服务器上，将localhost替换为对应服务器的ip地址。
```
docker run -d -p 8000:8000 -v $HOME/docker/dstudio:/home --restart=always --name dstudio shichenxie/dstudio:0.1.0
```

登陆过程，默认的用户名为 dstudio，该账号为管理员。密码通过点击 Singup 进入注册页面创建。然后点击 Login，回到登陆页输入 dstudio 和你设定的密码。登陆之后，进入了jupyter页面，在右边的New下拉框中选择RStudio进入rstudio server环境。

创建新用户过程，首先新用户进入`http://localhost:8000/`点击Singup，进入注册页面新建用户与密码。然后管理员 dstudio 登陆，进入`http://localhost:8000/hub/authorize`进行审批。由于这里的用户权限管理系统使用的是 [nativeauthenticator](https://native-authenticator.readthedocs.io/en/latest/)，不支持自动创建系统用户，还需要回到终端中输入```docker exec -it dstudio bash```，进入运行的容器中创建系统用户`useradd --create-home test`。为了支持多用户访问 rstudio server，还需要修改文件的权限```chmod -R 777 /tmp/rstudio-server/secure-cookie-key```，该文件只要访问过 rstudio server之后就会自动生成。

修改密码，登陆之后`http://localhost:8000/`，进入`http://localhost:8000/hub/change-password`可以自行修改密码。

# 贡献与参考

如果您对本项目感欢迎使用、star。由于目前还有一些功能可以完善，例如自动创建用户目录，如果您任何想法欢迎讨论，或者直接提交pr。

类似的项目有 [ShinyStudio](https://github.com/dm3ll3n/ShinyStudio)。

