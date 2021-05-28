# Application and Request context

## 手动压入上下文

手动压入`current_app`

```py
with app.app_context():
    # can access current_app
    do_something_with_current_app()
```

手动压入`request`

```py
with app.test_request_context():
    do_something_with_request()
```

## Propose of the context

当flask应用处理一个请求时，它首先创建一个基于从`WSGI server`接受到的环境变量的`Request`。之后请求处理单元(可以是线程、进程或协程)会获取一个`Request`。由于每个处理单元一次只能处理一个`Request`，所以可以将每个请求视为全局请求。

## context如何工作

1. `request context`和`application context`的工作模式类似 __栈__ 。他们分别存储在自己的栈中分别为`_request_ctx_stack`和`_app_ctx_stack`。
2. 实际使用的`request context`和`application context`都是实际对象的代理对象。
3. 当一个请求开始时，首先向栈压入一个`application context`，再压入一个`request context`。当`r_context`被压入后，就可以访问`current_app`、`g`、`request`、`session`对象了。
4. 当一个请求被解析并且产生了一个响应后，先将`r_context`弹出，再将`a_context`弹出。当他们被弹出后，`teardown_request()`和`teardown_appcontext()`被调用，即使请求报错。

5. 参考文件

    - https://werkzeug.palletsprojects.com/en/1.0.x/local/


## callback and error

1. 在所有请求被处理之前，`before_request`被调用，如果某个函数有返回值，其余的函数则被跳过，并将返回值作为响应返回给客户端。如果所有函数都没有返回值，这正确调用视图函数。
2. 响应正常产生后，`response`被传递给`after_request`方法，每个方法修改响应对象或者返回一个新的响应对象。
3. 请求返回后，`r_context`和`a_context`被弹出，分别调用`teardown_request`和`teardown_appcontext`。

对于`before_request`、`after_request`、`teardown_request`和`teardown_appcontext`都可以使用装饰器。

### callback for app and blueprint

### app callback

- before_request: before all request
- after_request: after each request
- teardown_appcontext: call when application context end
- teardown_request: call at end of each request

### blueprint callback

- after_app_request: call after each request
- after_request: call after each only for that buleprint
- before_app_request: call before each request
- before_request: call before each request just for that blueprint
- teardown_app_request: call when request end
- teardown_request: call when request end just for that blueprint


## Note on Proxies

flask中很多的对象都是实际对象的代理对象。

如果想要通过被代理对象获取实际对象，可以通过`_get_current_object()`


## reference

https://flask.palletsprojects.com/en/1.1.x/appcontext/

https://flask.palletsprojects.com/en/1.1.x/reqcontext/