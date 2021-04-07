# Application and Request context

## 如何理解application & request context

todo

## context如何工作

1. `request context`和`application context`的工作模式类似 __栈__ 。他们分别存储在自己的栈中。
2. 实际使用的`request context`和`application context`都是实际对象的代理对象。
3. 当一个请求开始时，首先向压入一个`application context`，在压入一个`request context`。当`r_context`被压入后，就可以访问`current_app`、`g`、`request`、`session`对象了。
4. 当一个请求被解析并且产生了一个响应后，先将`r_context`弹出，再将`a_context`弹出。但当他们弹出后，`teardown_request()`和`teardown_appcontext()`被调用，即使请求报错。


## callback and error

1. 在所有请求被处理之前，`before_request`被调用，如果某个函数有返回值，其余的函数则被跳过，并将返回值作为响应返回给客户端。如果所有函数都没有返回值，这正确调用视图函数。
2. 响应正常产生后，`response`被传递给`after_request`方法，每个方法修改响应对象或者返回一个新的响应对象。
3. 请求返回后，`r_context`和`a_context`被弹出，分别调用`teardown_request`和`teardown_appcontext`。

## Note on Proxies

flask中很多的对象都是实际对象的代理对象。

如果想要通过被代理对象获取实际对象，可以通过`_get_current_object()`


## reference

https://flask.palletsprojects.com/en/1.1.x/appcontext/

https://flask.palletsprojects.com/en/1.1.x/reqcontext/