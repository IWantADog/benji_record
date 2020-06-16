# redis

https://redis.io/topics/quickstart

https://github.com/JasonLai256/the-little-redis-book/blob/master/cn/redis.md

https://gist.github.com/tomysmile/1b8a321e7c58499ef9f9441b2faa0aa8

## basic

### database

与你熟悉的关系型数据库一致，Redis有着相同的数据库基本概念，即一个数据库包含一组数据。典型的数据库应用案例是，将一个程序的所有数据组织起来，使之与另一个程序的数据保持独立。

在Redis里，数据库简单的使用一个数字编号来进行辨认，默认数据库的数字编号是0。如果你想切换到一个不同的数据库，你可以使用select命令来实现。在命令行界面里键入select 1，Redis应该会回复一条OK的信息，然后命令行界面里的提示符会变成类似redis 127.0.0.1:6379[1]>这样。如果你想切换回默认数据库，只要在命令行界面键入select 0即可。

### concept

Keys：标识数据块。

Values：是关联于关键字的实际值，可以是字符串、整数、序列化对象（使用JSON、XML或其他格式）。在大多数情况下，__Redis会把值看做是一个字节序列，而不会关注它们实质上是什么__。注意，不同的Redis载体处理序列化会有所不同（一些会让你自己决定）。

redis不支持通过值查询。当出现这样的问题时，需要重新建模。

对于持久化，默认情况下，Redis会根据已变更的关键字数量来进行判断，然后在磁盘里创建数据库的快照（snapshot）。你可以对此进行设置，如果X个关键字已变更，那么每隔Y秒存储数据库一次。默认情况下，如果1000个或更多的关键字已变更，Redis会每隔60秒存储数据库；而如果9个或更少的关键字已变更，Redis会每隔15分钟存储数据库

redis很快

## 数据结构

redis中每个命令都相对应于一种特定的数据结构。

### Strings

- set
- get
- strlen
- getrange `<key> <start> <end>`
- append `<key> <value>`
- incr、decr
- incrby、decrby
- setbit、getbit

[redis bitmap](http://blog.getspool.com/2011/11/29/fast-easy-realtime-metrics-using-redis-bitmaps/)

### Hashes

散列数据结构很像字符串数据结构。两者的区别在于，散列数据结构提供了一个额外的间接层：一个域（Field）

field(将value划分为不同的部分，从使用的角度按属性理解比较贴切)

- hset
- hget
- hmset(同时设置多个域的值)
- hmget（同时获取多个域）
- hgetall （获取所有域的值）
- hkeys（获取所有的域）
- hdel（删除指定的域）

### Lists

对于一个给定的关键字，列表数据结构让你可以存储和处理一组值。你可以添加一个值到列表里、获取列表的第一个值或最后一个值以及用给定的索引来处理值

- lpush
- ltrim

### Sets

集合。

- sadd（向集合增加数据）
- sismember（检查某元素是否属于一个集合）
- sinter（集合的交集？）

### Sorted Sets

分类集合数据结构就类似于集合数据结构，主要区分是标记（score）的概念。标记提供了排序（sorting）和秩划分（ranking）的功能。

- zadd
- zcount
- zrevrank

## 使用数据结构

### 数据交互和流水线（Round Trips and Pipelining）

redis是单线程的。

Redis还支持流水线功能。通常情况下，当一个客户端发送请求到Redis后，在发送下一个请求之前必须等待Redis的答复。使用流水线功能，你可以发送多个请求，而不需要等待Redis响应。这不但减少了网络开销，还能获得性能上的显著提高。

### 事务（Transactions）

虽然这些都很有用，但在实际开发时，往往会需要运行具有原子性的一组命令。若要这样做，首先要执行multi命令，紧随其后的是所有你想要执行的命令（作为事务的一部分），最后执行exec命令去实际执行命令，或者使用discard命令放弃执行命令。

```sql
multi
hincrby groups:1percent balance -9000000000
hincrby groups:99percent balance 9000000000
exec
```

`watch` and `keys`

## 超越数据结构

### 使用期限（Expiration）

```sql
-- 30秒后删除掉关键字（包括其关联的值）
expire pages:about 30
-- 在2012年12月31日上午12点删除掉关键字
expireat pages:about 1356933600s
```

```sql
--  查看一个关键字能够存活多久
ttl pages:about
-- 删除关键字的使用期限
persist pages:about
```

```sql
-- setex命令让你可以在一个单独的原子命令里设置一个字符串值，同时里指定一个生存期。
setex pages:about 30 '<h1>about us</h1>'
```

### 发布和订阅（Publication and Subscriptions）

Redis的列表数据结构有blpop和brpop命令，能从列表里返回且删除第一个（或最后一个）元素，或者被堵塞，直到有一个元素可供操作。这可以用来实现一个简单的队列。

```sql
-- 在A客户端中订阅一个频道
subscribe warnings

-- 在B客户端中向频道中发送数据 A客户端会收到发送的信息
publish warnings "it's over 9000!"
```

你可以订阅多个频道（subscribe channel1 channel2 ...），订阅一组基于模式的频道（psubscribe warnings:*），以及使用unsubscribe和punsubscribe命令停止监听一个或多个频道，或一个频道模式。

### 监控和延迟日志（Monitor and Slow Log）

monitor命令是一个优秀的调试工具，可以让你查看Redis正在做什么。

slowlog

### 排序（Sort）

内容较复杂。[参见原文](https://github.com/JasonLai256/the-little-redis-book/blob/master/cn/redis.md#%E6%8E%92%E5%BA%8Fsort)

## 第5章 - 管理

内容较为琐碎。[原文连接](https://github.com/JasonLai256/the-little-redis-book/blob/master/cn/redis.md#%E7%AC%AC5%E7%AB%A0---%E7%AE%A1%E7%90%86)

## basic commends

resid-server --version

info

## redis config path when install redis via brew

/usr/local/etc/redis.conf
