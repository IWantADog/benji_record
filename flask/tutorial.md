# flask tutorial

## flaks environment variable

FLASK_APP

FLASK_ENV

## about g object

1. 每个请求都有一个不同`g object`。
2. `g`主要用来存储在一个请求过程中，可能被函数多次请求的资源。
3. 当有资源在`g`中被分配，相应的需要将资源的释放函数通过`teardown_appcontext`注册到app。

## about blueprint

create a blueprint

```py
bp = flaks.Blueprint('auth', __name__, url_prefix='/auth')
```

register a blueprint to a app

```py
app.register_blueprint(auth.bp)
```

### before_app_request

`before_app_request`注册一个函数在`view function`，不论请求的url。

## write correct setup.py and MANIFEST.in

```py
# setup.py
from setuptools import find_packages, setup

setup(
    name='flaskr',
    version='1.0.0',
    packages=find_packages(),
    include_package_data=True,
    zip_safe=False,
    install_requires=[
        'flask',
    ],
)
```

```
<!--MANIFEST.in -->
include flaskr/schema.sql
graft flaskr/static
graft flaskr/templates
global-exclude *.pyc
```

## Test coverage

`pip install pytest coverage`

`tempfile` ??

`app.test_client()`

`app.test_cli_runner()`

`pytest`

### pytest.fixture

`Pytest` uses `fixtures` by matching their function names with the names of arguments in the test functions. For example, the `test_hello` function you’ll write next takes a client argument. __Pytest matches that with the client fixture function, calls it, and passes the returned value to the test function.__

## what need register to app instance?

app.cli.command(function)

app.teardown_appcontext(function)




