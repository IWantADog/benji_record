# loggin and config

## how to logging in blueprint

todo

## configuring from files

```py
app = Flask(__name__)
app.config.from_object('/path/to/config.conf')

app.config.from_envvar('APPLICATION_SETTINGS')

app.config.from_object()
```

### configuration best practices

1. Create your application in a function and register blueprints on it. That way you can create multiple instances of your application with different configurations attached which makes unit testing a lot easier. You can use this to pass in configuration as needed.

2. Do not write code that needs the configuration at import time. If you limit yourself to request-only accesses to the configuration you can reconfigure the object later on as needed.

### how to manage configuration file

1. 维护一个默认配置文件。
2. 通过一个环境变量切换配置文件。
3. 使用第三方工具，如`fabric`

### Instance Folders

`instance_path`和`instance_relative_config`的作用是什么？

```py

app = Flask(__name__, instance_path='/path/to/instance/folder')

app = Flask(__name__, instance_relative_config=True)
app.config.from_object('yourapplication.default_settings')
app.config.from_pyfile('application.cfg', silent=True)
```