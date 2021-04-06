# Quick Start

## 常用方法

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

## render template

render_template():

- 输入：模版名和对应参数

Inside templates you also have access to the `request`, `session` and `g` objects as well as the `get_flashed_messages()` function.

## what is g object

## Access request data

Imagine the context being the handling thread. A request comes in and the web server decides to spawn a new thread (or something else, the underlying object is capable of dealing with concurrency systems other than threads). When Flask starts its internal request handling it figures out that the current thread is the active context and binds the current application and the WSGI environments to that context (thread). It does that in an intelligent way so that one application can invoke another application without breaking.

## request object

1. `request`是一个全局对象。调用方式`from flask import request`
2. request.method: 获取http方法的类型
3. request.form: 
    - 通过键值对的方式获取`post` & `puth`上传的数据
    - 获取查询参数`request.args`

## Fiel Uploads

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

如果需要自定义错误页面，可以使用`errorhandler()`

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

### 多用户的情况下，session的工作如何理解？

### 如何理解`cookies base session`

### flask server-side session extension

## Message Flash





















