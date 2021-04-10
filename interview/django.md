# django

## ORM

[what is orm](https://en.wikipedia.org/wiki/Object%E2%80%93relational_mapping)

## wsgi

1. wsgi不是一个框架、一个python模块、一个服务器、一个API接口、或是软件应用。wsgi只是一种接口规范，关于server与application通讯的接口规范。如果application是按照wsgi编写的，该application就能在所有支持wsgi的server上运行。

2. wsgi分为server侧和application侧。server侧需要调用一个application侧提供的可调用对象。

3. wsgi application能够被叠放，在叠放的applicaion之间需要中间层(middleware)。中间层必须在两侧都实现wsgi规范。

4. wsgi server的工作仅是接受client的请求，再将其发送给application，最后将application的回应返回给client。其他的具体操作由application和middleware完成。

常用的uwsgi server

- uWSGI

    `uwsgi (all lowercase)` is the native binary protocol that `uWSGI` uses to communicate with other servers.

    `uWSGI` is often used for serving Python web applications in conjunction with web servers such as `Cherokee` and `Nginx`, which offer direct support for `uWSGI's` native uwsgi protocol.For example, data may flow like this: `HTTP client ↔ Nginx ↔ uWSGI ↔ Python app.`

- gunicorn
    pass

## 一个请求从进入http server到django经历了什么。django的请求的生命周期

客户端请求 - 》 http server（nginx）-》 wsgi server -》 middler -》 django路由选择 -》 http响应

## django的中间件工作原理

pass

## 使用django ORM进行查询的例子

pass

## functon base view 和 class base view

常用的class base view如：

ListView、DetailView、FormView、CreateView、UpdateView、DeleteView

## class base view 中`get_queryset` & `get_context_data` & `get_object`的作用

get_queryset: 返回视图需要的所有对象。比如某个view获取所有的人员信息，`get_queryset`返回所有的所有的人员对象

get_context_data: 获取渲染模版需要的信息。

get_object: 返回单一对象。比如某个view展示某个人员的信息，`get_object`就通过id找到员工的对象

## django模型继承

混入 minxin

ContextMinxin

TemplateMinxin

SingalObjectMinxin

MultipleObjectMinxin

FormMinxin

## Django中常用的组件及用途

auth: 用户组件包含django的用户、权限等相关模型

admin: django只带的数据管理后台，便于对模型的数据进行修改。也可接受定制开发，比如修改页面样式、控件类型、增加额外批量修改数据的方法

message:

## django的request是什么时候创建的

## django manager 与 queryset

## select_related和prefetch_related

## 列举Django orm中使用纯sql的方法

## queryset object 的values和values_list

## 如何使用django orm批量创建数据

## django orm中field的on_delete的用途

## 如何通过orm实现数据表的6种约束

## Django csrf的实现机制

## 基于django使用ajax发送post请求是，有几种方式实现

## django的runserver与uwsgi的区别

## django如何实现websocket

https://github.com/django/channels

## django的常用第三方库

django_allauth

django_filter

ckeditor

django_debug_toolbar

django restful framework

## django中如何使用redis做缓存

django_redis

## django数据迁移

## django F & Q 方法

## nginx与uwsgi如何配合工作

首先浏览器发起 http 请求到 nginx 服务器，Nginx 根据接收到请求包，进行 url 分析,

判断访问的资源类型。如果是静态资源，直接读取静态资源返回给浏览器。

如果请求的是动态资源就转交给 uwsgi服务器。

uwsgi 服务器根据自身的uwsgi 和 WSGI 协议，找到对应的 Django 框架。

Django 框架下的应用进行逻辑处理后，将返回值发送到 uwsgi 服务器。

uwsgi 服务器再返回给 nginx，最后 nginx将返回值返回给浏览器进行渲染显示给用户。
