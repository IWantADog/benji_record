# Basic k8s


## k8s大致的情况

在硬件层面，kubernetes集群由多个node组成，node可以分为两类。

- master node: 负责`kubernetes control plane`，其负责管理整个kubernetes系统。
- worker node: 运行实际的application

control plane（master node）的构成
- kubernetes Api Server: 
- Scheduler: 为applicaiton调度分配node
- Controller Manager: 负责cluster层面的逻辑，比如复制组件、跟踪worker node、处理异常等情况。
- etcd: 可靠的分布式数据存储，保存集群的配置信息

worker nodel的构成
- 容器: Docker，rkt，或者其他。
- kubelet: 负责与API server通信，控制本node中的容器。
- kubernetes service proxy: 控制各个application容器之间的网络通信

一旦application开始运行，k8s会始终保证application的状态符合配置文件中定义的。例如配置中指明某个application有5个实例，那么k8s会始终保持5个实例正在运行中。如果某个实例崩溃或是故障，k8s会自动重启它。
同样如果某个`worker node`无法使用，k8s会将该node上的容器全部转移到另一个可用的node上。

用户能够app运行时在修改app的数量，k8s会自动的增加或减少app的数量。这些也可完全由k8s来控制，比如根据cpu负载、内存、每秒的请求数量等。

使用容器而不将app部署在某个指定的node上，使用户在任何时候能够自由地移动app。部署在cluster中的app能够被k8s合理的组合使所有的资源被合理的使用。

## 关于容器

linux control groups & linux namespaces

## 关于pod

pod是一组相关容器的组合体。pod中的容器运行在`同一个node`上，并且拥有相同的`linux namespace`。

每一个pod像是一个独立的逻辑上的机器，拥有自己的IP、hostname、process。

一个pod中的所有container运行在同一个`logic machine`，而不同pod的container，即使运行在同一个node，也表现为运行在不同的logic machine。

每个pod都有各自的ip，即使不同的pod位于不同的node。他们依然可以相互通讯。

通常情况下每个pod只应该包含一个`container`。一个重要的原因是当多个`container`包含在一个`pod`中时，这些`container`只能运行在一个`worker`上。
> 虽然pod内部支持运行多个container，为了保持简单，应该尽量保证一个pod只包含一个container。

### 当使用kubelet run后发生了什么
输入`kubelet`后，
1. 向`kubernetes api server`发送`rest http request`创建了`ReplicationController`。
2. `ReplicationController`创建一个pod
3. `Scheduler`将pod分配到一个合适的node
4. node上的kubelet识别到被分配给自己，之后委托docker拉取指定的`image`。image下载完成之后，运行container。

__pod被分配的ip地址都属于内部ip，外部无法直接访问__。为了使pod能够被外部访问，需要一个`Service`。创建一个`LoadBalancer-Type service`，之后就可通过这个`load balancer`的`public ip`访问到内部的pod。

### 为什么使用pod

对比多个`applicaton`运行在同一个`container`和运行多个`container`的利弊。
- 多个`application`运行在一个container管理十分不便。
    - 例如其中的一个app需要升级、或是修改依赖项。必须重新部署镜像时，也可能对其他的app造成影响，并且也需要重启其他的app。
    - 某个app崩溃了，需要自己实现重启的逻辑。
    - 当所有的app输出日志到标准输出时，所有的日志都混在一起难以分辨。

由于多个app部署在同一个container中的管理问题。而当多个相关的容器需要统一管理时，就需要新的概念--pod。

### 理解pod内部container的部分隔离

k8s通过配置`Docker`使一个`pod`中的所有`container`共享一个linux namespace。

由于一个pod的所有container在相同的`Networks` & `UTS` namespace，所以他们共享相同的`hostname` & `network interfaces`。

并且所有在同一个`IPC`namespace下的所有`container`能够通过`IPC`相互通讯。
> [IPC: interprocessing communication](https://tldp.org/LDP/tlk/ipc/ipc.html)

### 如何合理地使用pod

为什么每个pod最好只包含一个container？

1. 不能合理使用node资源。一个pod只会运行在一个worker上，如果一个pod内部运行多个app，则只会使用一个node的资源。
2. 无法合理的横向扩展。一个pod中的多个app，对于横向扩展的需求不同。

何时应该在一个pod中使用多个`container`?

类似于存在一`main container`和多个`support container`的结构。support的功能可能类似于日志收集、文件下载和存储等。
> 书中这里提到了`sidecar`

## 关于`ReplicationControllers`

`ReplicationControllers`负责管理pod，当使用`kubelet run`时可以指定pod的数量，如果不指定pod的数量，默认只会创建一个pod。而且当pod由于意外挂起时，`rc`会自动创建一个新的pod代替旧的。


## 关于Service的功能

pod是易变的，可能随时挂起。当新的pod被创建时，pod会获得一个新的ip地址。如果直接通过pod的ip连接pod，会导致新建pod之后原有的ip完全不可用。

Service就提供了这样的功能。在Service的整个声明周期中它始终有一个静态ip。当需要连接一个pod时，间接通过Service访问pod。Service始终保证pod可以被访问，而无论pod具体在哪里。

Service还能为多个pod同时提供服务，当一个请求进来时会被转接到某一个pod上。

## 水平扩展replicas的数量

`kubectl scale rc test --replicas=3`

__用户无法也不能直接指定`kubernetes`该做些什么。用户只能告诉k8s一个期望的状态，k8s自己决定如何达到指定的状态。这是k8s的基本准则。__


## k8s常规使用

kubectl cluster-info

kubectl get nodes/pods

kubectl describe pod/nodes/svc

kubectl expose rc

k run test --image=benjilee5453/test --port=5000 
k expose pod test --type NodePort --port 8080
> 这里的port指的是需要绑定的pod的端口。
minikube service hello-minikube --url

source <(kubectl completion zsh) # zsh kubuctl 命令自动补全