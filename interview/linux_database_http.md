# Linux & Database & HTTP & ...

## HTTP

### GET与POST区别

### tcp三次招手与四次挥手

### 同源策略

源的含义：协议、域名、端口

### session & cookies

### csrf & xss

### tcp与udp

tcp

1. 属于可靠的数据传输服务，保证数据的交付、数据有序和无误。
2. tcp是面向连接的。tcp在发送数据之前发送方和接受方会进行3次握手，保证连接的可靠性。

udp

1. 不可靠，不对数据完整、有序进行保证
2. 无连接的。直接发送数据，不需要握手。

由于udp发送数据不需要握手，所以udp速度快于tcp。但tcp相较于udp更可靠。

基于udp的应用层协议：dns、rip
基于tcp的应用层协议：http、smtp、telnet、ftp

### restful api基本原理

### 常用 header 和 statsu code

## os

### 死锁、死锁的产生条件和解决方法

- 互斥。某一资源同一时间只能被一个线程获取。
- 占有和等待。某一线程获取了部分资源，并且等待获取其他资源。
- 不可抢占。某一线程获取资源后，除非它本身释放资源，否则其他线程无法获取。
- 循环等待。存在一个循环等待链，上游请求的资源有下游占有

例子：哲学看就餐问题。

常用并且比较合理的解决死锁的方法是

从`占有和等待`去打破，当一个线程获取锁时，为获取锁的动作增加时间限制，如果超过时间限制则释放所有获取的资源。

### 乐观锁和悲观锁

## Datebase

## 数据库设计范式

### 事务、索引

事务：保证多个操作的原子性。多个操作要么都成功执行，要么完全回滚。

### 常见mysql问题

## linux 常用命令

ls

lsof

cp

ln

systemctl

firwall-cmd

ps

kill
