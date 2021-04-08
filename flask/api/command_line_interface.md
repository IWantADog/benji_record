# Command line interface

## FLASK_APP

1. flask通过`FLASK_APP`找到`application`的位置。

### how to set FLASK_APP

- (nothing): `wsgi.py`会被导入，并自动寻找一个`app`。
- FLASK_APP=hello: 指定名字的文件被导入，并自动寻找`app`或是工厂函数`create_app`

### FLASK_APP的构成

- FLASK_APP=src/hello
    
    Sets the current working directory to src then imports hello.

- FLASK_APP=hello.web

    Imports the path hello.web

- FLASK_APP=hello:app2

    Uses the app2 Flask instance in hello.

- FLASK_APP="hello:create_app('dev')"

    The create_app factory in hello is called with the string 'dev' as the argument.

### flask如何根据传入的参数寻找application

1. 通过传入的数据寻找`app`、`application`或是任何`application`对象。
2. 如果`app`对象未找到，则会寻找`create_app`或`make_app`，并返回一个应用对象。

## FLASK_ENV

1. 如果不设置，默认值为`production`
2. `development`

## 通过`reloader`监视额外的文件

1. 使用`--extra-files`或`FLASK_RUN_EXTRA_FILES`
2. 多个文件使用`:`分割

## FLASK_DEBUG

1. 开发模式下，debug模式默认开启
2. `FLASK_DEBUG=1`代表开启，`=0`代表关闭

## python-dotenv

## flask register command

可以在`app`或者`blueprint object`上注册`commands`

```py
from flask import Blueprint

bp = Blueprint('students', __name__)

@bp.cli.command('create')
@click.argument('name')
def create(name):
    ...

app.register_blueprint(bp)
```

声明`blueprint`时可以携带`cli_group`参数，用于指明该命令的所属层级。

```py
bp = Blueprint('students', __name__, cli_group='other')
# or
app.register_blueprint(bp, cli_group='other')
```

### command命令获取应用上下文

如果直接使用`click`，无法获取到应用的上下文。

```py
@app.cli.command('create')
def create():
    pass

# 等价与

@click.command('create')
@with_appcontext
def create():
    pass
```


