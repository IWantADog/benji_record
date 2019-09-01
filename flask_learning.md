# Flask

## 2019.02.25

1. 客户端-WSGI-FLask的关系

   - 客户端发送请求给web服务器，web服务器再把请求发送给Flask实例，Flaks再根据路由调用不同的函数。

2. Flask基础
   1. Flaks上下文全局变量
      - current_app

      - g

        >**To share data that is valid for one request only from one function to another**, a global variable is not good enough because it would break in threaded environments. Flask provides you with a special object that ensures it is only valid for the active request and that will return different values for each request. In a nutshell: it does the right thing, like it does for [`request`](http://flask.pocoo.org/docs/1.0/api/#flask.request) and [`session`](http://flask.pocoo.org/docs/1.0/api/#flask.session).

        

      - request

        > To access incoming request data, you can use the global request object. Flask parses incoming request data for you and gives you access to it through that global object. **Internally Flask makes sure that you always get the correct data for the active thread if you are in a multithreaded environment.**

      - session

        > If you have set [`Flask.secret_key`](http://flask.pocoo.org/docs/1.0/api/#flask.Flask.secret_key) (or configured it from [`SECRET_KEY`](http://flask.pocoo.org/docs/1.0/config/#SECRET_KEY)) you can use sessions in Flask applications. **A session makes it possible to remember information from one request to another.** The way Flask does this is by using a signed cookie. The user can look at the session contents, but can’t modify it unless they know the secret key, so make sure to set that to something complex and unguessable.
   2. 请求钩子
      - before_first_request
      - Before_request
      - after_request
      - teardown_request
   3. 请求调度
   4. 响应
   5. Flaks扩展
3. 