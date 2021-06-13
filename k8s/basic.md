# Basic k8s

在硬件层面，kubernetes集群有多个node组成，node可以分为两类。

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

k8s能够在，用户能够app运行时在修改app的数量，k8s会自动的增加或减少app的数量。这些也可完全由k8s来控制，比如根据cpu负载、内存、每秒的请求数量等。





