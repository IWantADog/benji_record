# docker commands

常用docker命令

## docker pull imageName:version

## docker images

展示所有的镜像文件

## docker container ls

展示所有的容器，默认只展示运行中的容器。添加`-a`展示所有的容器。

## docker rmi imageName/imageID

根据镜像名或镜像id删除镜像

## docker push username/imageTag

将本地的镜像上传到仓库中

## docker bulid

根据Dockerfile创建镜像。

创建镜像的方式有两种。一是通过docker conmmit创建。二是通过Dockerfile创建。一般推荐编写Dockerfile后使用docker bulid创建，这种方式更加灵活。docker commit一般在docker build出错时使用。

## docker commit

通过一个修改过的容器创建一新镜像。

## docker start imageName/imageId

启动镜像

## docker log imageName/imageId

查看docker的输出日志

## docker attach imageName/imageId

进入运行中的容器

## docker ps

查看运行中的容器

## docker logs continer

查看容器的输出。类似于`tail -f`的功能

## docerk run

`docker run -i -t ubuntu:14.04 /bin/bash`

启动ubuntu:14.04的镜像，启动之后执行/bin/bash命令，打开一个shell。

-t: 选项让Docker分配一个伪终端（pseudo-tty）并绑定到容器的标准输入上。

-i: 让容器的标准输入保持打开。

-d: 让容器以守护态形式运行。容器打开后输入exit按回车退出容器。

还有一些其他的常用的参数：

-v：挂载卷。将宿主文件系统中的文件映射到镜像中，当宿主文件修改时镜像中的文件会同步更新。

—name: 命名容器。

-p：将容器中的端口映射到宿主端口。例如 -p 8080:80，将容器的80端口映射到宿主的8080端口。

当利用 docker run 来创建容器时，Docker 在后台运行的标准操作包括：

- 检查本地是否存在指定的镜像，不存在就从公有仓库下载
- 利用镜像创建并启动一个容器
- 分配一个文件系统，并在只读的镜像层外面挂载一层可读写层
- 从宿主主机配置的网桥接口中桥接一个虚拟接口到容器中去
- 从地址池配置一个 ip 地址给容器
- 执行用户指定的应用程序
- 执行完毕后容器被终止
