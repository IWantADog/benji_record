# Quick Start

## 常用方法

### routing

variable rules

- string  : 默认，任何文本除了斜杠
- int     : 数字
- float   : 浮点型
- path    : 和`string`一样，不过也接受斜杠
- uuid    : UUID字符串

很怪的一点:

对于结尾含有`/`的路由，当访问时如果url结尾不带`/`，`flask`会自动给路由增加。

对于结尾不含`/`路由，当访问是如果url结尾带有`/`，flask报404。

对于开发的过程中，所有的路由都要增加`/`。

### url_for(): 

1. 通过方法名获取对应的url，接受多种参数。
2. 接受`static`，获取静态文件路径

### app.test_request_context()

伪造`request`对象，进行单元测试

```py
from flask import request

with app.test_request_context('/hello', method='POST'):
    # now you can do something with the request until the
    # end of the with block, such as basic assertions:
    assert request.path == '/hello'
    assert request.method == 'POST'
```

## Flask.route() 支持多少种http方法？

// todo

## render template

render_template():

- 输入：模版名和对应参数

Inside templates you also have access to the `request`, `session` and `g` objects as well as the `get_flashed_messages()` function.

## what is g object

// todo

## Access request data

Imagine the context being the handling thread. A request comes in and the web server decides to spawn a new thread (or something else, the underlying object is capable of dealing with concurrency systems other than threads). When Flask starts its internal request handling it figures out that the current thread is the active context and binds the current application and the WSGI environments to that context (thread). It does that in an intelligent way so that one application can invoke another application without breaking.

## request object

1. `request`是一个全局对象。调用方式`from flask import request`
2. request.method: 获取http方法的类型
3. request.form: 通过键值对的方式获取`post` & `puth`上传的数据
4. request.args: 获取查询参数

### File Uploads

1. `enctype="multipart/form-data"` attribute on your HTML form, 
2. `request.files`: 获取用户上传的文件，通过键值对方式获取文件。获取的对象类似于`python file object`。同时支持`save`方法将文件存储到文件系统。
3. 获取文件上传时的文件名，`f.filename`。不过保持警惕，用户给的文件名不可相信，可以使用`werkzeug.utils.secure_filename`对文件名进行修改。

## cookies

1. 获取cookies: `request.cookies.get('username')`
2. set cookies:
    __设置`cookies`需要在`response`上设置。__
    
    ```py
    from flask import make_response

    @app.route('/')
    def index():
        resp = make_response(render_template(...))
        resp.set_cookie('username', 'the username')
        return resp
    ```

## redirects and errors

`from flask import redirect, abort`

`redirect`: 重定向

`abort`: 提早拒绝一个请求，并返回一个响应码。通过`abort`返回的响应，会将错误的信息通过html展示出来。

如果需要自定义错误页面，可以使用`Flask.errorhandler()`

```py
from flask import render_template

@app.errorhandler(404)
def page_not_found(error):
    return render_template('page_not_found.html'), 404
```

## responses

1. If a response object of the correct type is returned it’s directly returned from the view.
2. If it’s a `string`, a response object is created with that data and the default parameters.
3. If it’s a `dict`, a response object is created using `jsonify`.
4. If a `tuple` is returned the items in the tuple can provide extra information. Such tuples have to be in the form `(response, status)`, `(response, headers)`, or `(response, status, headers)`. The status value will override the status code and headers can be a list or dictionary of additional header values.
5. `If none of that works, Flask will assume the return value is a valid WSGI application and convert that into a response object.`

## API with JSON

如果`view`返回的是个字典，flask会自动将起转换为`json`响应对象。

通过`make_response`获取`response object`，之后修改并返回。

对于较复杂的json接口，可以使用`jsonify`或者第三方的包。

## sessions

- `session`也是一个全局变量。
- 为了使用`session`，必须首先设置`secret key`
- 像使用字典一样使用session
- `session`的实现是基于`cookies`。

A note on cookie-based sessions: Flask will take the values you put into the session object and serialize them into a cookie. __If you are finding some values do not persist across requests, cookies are indeed enabled, and you are not getting a clear error message, check the size of the cookie in your page responses compared to the size supported by web browsers.__

Besides the default client-side based sessions, if you want to handle sessions on the server-side instead, there are several Flask extensions that support this.

### how to generate a good secret key

```sh
$ python -c 'import os; print(os.urandom(16))'
b'_5#y2L"F4Q8z\n\xec]/'
```

### flask的session如何存储

// todo

### 如何理解`cookies base session`

https://stackoverflow.com/questions/32563236/relation-between-sessions-and-cookies

https://www.hackingarticles.in/beginner-guide-understand-cookies-session-management/

https://stackoverflow.com/questions/6339783/what-is-the-difference-between-sessions-and-cookies-in-php

https://devcentral.f5.com/s/articles/sessions-and-cookies-and-persistence-oh-my#.UdPNRGfYhOY

### flask server-side session extension

// todo

## Message Flash

flush(): push a message
get_flashed_messages(): 获取所有的message

## logging

__The attached logger is a standard logging Logger.__

```py
app.logger.debug('A value for debugging')
app.logger.warning('A warning occurred (%d apples)', 42)
app.logger.error('An error occurred')
```

## hooking in WSGI middleware

__To add WSGI middleware to your Flask application, wrap the application’s `wsgi_app` attribute.__ For example, to apply Werkzeug’s ProxyFix middleware for running behind Nginx:

```py
from werkzeug.middleware.proxy_fix import ProxyFix
app.wsgi_app = ProxyFix(app.wsgi_app)
```

Wrapping `app.wsgi_app` instead of app means that app still points at your Flask application, not at the middleware, so you can continue to use and configure app directly.

### how to use flask middleware


## flask extentions

https://flask.palletsprojects.com/en/1.1.x/extensions/#extensions

## cookies & sessions

cookies

1. 存储在客户端，大小不超过4K。
2. 可以设置过期时间，当浏览器关闭时cookies失效。
3. http是无状态的，使用cookies可以用来跟踪用户的状态。

session cookies: cookies存储在浏览器的内存中，当浏览器关闭，cookies消失。

persistent cookies: cookies存放在客户端的电脑上。当浏览器关闭，cookies依然可用。

session

1. session-id一般通过`cookies`存储。一般通过在cookies中存储的`session-id`找到服务器上对应的`session`。

### cookies的获取

1. 客户端通过`get or post`发送请求。
2. session—ID在客户端被创建，并存储在服务端。服务器在响应头中添加`set-cookies`，并返回给客户端。
3. 之后客户端每次与服务端的请求都要在请求头中添加`cookies`
