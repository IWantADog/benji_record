# pytest

## * Fixtures as Function arguments

__Test functions can receive fixture objects by naming them as an input argument. For each argument name, a fixture function with that name provides the fixture object. Fixture functions are registered by marking them with `@pytest.fixture`.__

fixture can be use only in local module.

## * conftest.py: sharing fixture functions

If during implementing your tests you realize that you want to use a fixture function from multiple test files you can move it to a `conftest.py` file. __You don’t need to import the fixture you want to use in a test, it automatically gets discovered by pytest. The discovery of fixture functions starts at test classes, then test modules, then conftest.py files and finally builtin and third party plugins.__

## Sharing test data

__If you want to make test data from files available to your tests, a good way to do this is by loading these data in a fixture for use by your tests__. This makes use of the automatic caching mechanisms of pytest.

Another good approach is by adding the data files in the tests folder. There are also community plugins available to help managing this aspect of testing, e.g. [pytest-datadir](https://pypi.org/project/pytest-datadir/) and [pytest-datafiles](https://pypi.org/project/pytest-datafiles/).

## * Scope: sharing fixtures across classes, modules, packages or session

### Fixture scopes

Fixtures are created when first requested by a test, and are destroyed based on their scope:

- function: `the default scope`, the fixture is destroyed at the end of the test.

- class: the fixture is destroyed during teardown of the last test in the `class`.

- module: the fixture is destroyed during teardown of the last test in the `module`.

- package: the fixture is destroyed during teardown of the last test in the `package`.

- session: the fixture is destroyed at the end of the test `session`.

> Pytest only caches one instance of a fixture at a time, which means that when using a parametrized fixture, pytest may invoke a fixture more than once in the given scope.

### Dynamic scope

In some cases, you might want to change the scope of the fixture without changing the code. To do that, pass a callable to scope. The callable must return a string with a valid scope and will be executed only once - during the fixture definition. It will be called with two keyword arguments - `fixture_name` as a string and `config` with a configuration object

## Order: Higher-scoped fixtures are instantiated first

Within a function request for fixtures, those of higher-scopes (such as `session`) are instantiated before lower-scoped fixtures (such as `function` or `class`). The relative order of fixtures of same scope follows the declared order in the test function and honours dependencies between fixtures. `Autouse fixtures` will be instantiated before explicitly used fixtures.

## * Fixture finalization / executing teardown code

pytest supports execution of fixture specific finalization code when the fixture goes out of scope. By using a `yield` statement instead of return, __all the code after the yield statement serves as the teardown code__.

Note that if an exception happens during the setup code (before the yield keyword), the teardown code (after the yield) will not be called.

```py
import smtplib
import pytest

@pytest.fixture(scope="module")
def smtp_connection():
    smtp_connection = smtplib.SMTP("smtp.gmail.com", 587, timeout=5)
    yield smtp_connection  # provide the fixture value
    print("teardown smtp")
    smtp_connection.close()
```

## Fixtures can introspect the requesting test context

Fixture functions can accept the `request` object to introspect the “requesting” test function, class or module context.

## Using markers to pass data to fixtures

Using the `request` object, a fixture can also access markers which are applied to a test function. __This can be useful to pass data into a fixture from a test__.

## * Factories as fixtures

The `“factory as fixture”` pattern can help in situations where the result of a fixture is needed multiple times in a single test. __Instead of returning data directly, the fixture instead returns a function which generates the data.__ This function can then be called multiple times in the test.

```py
@pytest.fixture
def make_customer_record():
    def _make_customer_record(name):
        return {"name": name, "orders": []}

    return _make_customer_record


def test_customer_records(make_customer_record):
    customer_1 = make_customer_record("Lisa")
    customer_2 = make_customer_record("Mike")
    customer_3 = make_customer_record("Meredith")
```

## Parametrizing fixtures

```py
import pytest
import smtplib

@pytest.fixture(scope="module", params=["smtp.gmail.com", "mail.python.org"])
def smtp_connection(request):
    smtp_connection = smtplib.SMTP(request.param, 587, timeout=5)
    yield smtp_connection
    print("finalizing {}".format(smtp_connection))
    smtp_connection.close()
```

## Using marks with parametrized fixture

`pytest.param()` can be used to apply marks in values sets of parametrized fixtures in the same way that they can be used with `@pytest.mark.parametrize`.

## Modularity: using fixtures from a fixture function

In addition to using fixtures in test functions, __fixture functions can use other fixtures themselves__.

## Automatic grouping of tests by fixture instances

pytest minimizes the number of active fixtures during test runs. If you have a parametrized fixture, then all the tests using it will first execute with one instance and then finalizers are called before the next fixture instance is created. Among other things, this eases testing of applications which create and use global state.

## * Using fixtures from classes, modules or projects

`usefixtures`: using fixture for classes

```py
# content of conftest.py

import os
import shutil
import tempfile

import pytest

@pytest.fixture
def cleandir():
    old_cwd = os.getcwd()
    newpath = tempfile.mkdtemp()
    os.chdir(newpath)
    yield
    os.chdir(old_cwd)
    shutil.rmtree(newpath)
```

```py
import os
import pytest

@pytest.mark.usefixtures("cleandir")
class TestDirectoryInit:
    def test_cwd_starts_empty(self):
        assert os.listdir(os.getcwd()) == []
        with open("myfile", "w") as f:
            f.write("hello")

    def test_cwd_again_starts_empty(self):
        assert os.listdir(os.getcwd()) == []
```

Due to the `usefixtures` marker, __the cleandir fixture will be required for the execution of each test method, just as if you specified a `“cleandir”` function argument to each of them.__

Specify multiple fixtures like this:

```py
@pytest.mark.usefixtures("cleandir", "anotherfixture")
def test():
    ...
```

and you may specify fixture usage at the test module level using pytestmark:

```py
pytestmark = pytest.mark.usefixtures("cleandir")
```

It is also possible to put fixtures required by all tests in your project into an ini-file:

```conf
# content of pytest.ini
[pytest]
usefixtures = cleandir
```

## * Autouse fixtures (xUnit setup on steroids)

Occasionally, you may want to have fixtures get invoked automatically without declaring a function argument explicitly or a usefixtures decorator.

```py
import pytest

class DB:
    def __init__(self):
        self.intransaction = []

    def begin(self, name):
        self.intransaction.append(name)

    def rollback(self):
        self.intransaction.pop()

@pytest.fixture(scope="module")
def db():
    return DB()

class TestClass:
    @pytest.fixture(autouse=True)
    def transact(self, request, db):
        db.begin(request.function.__name__)
        yield
        db.rollback()

    def test_method1(self, db):
        assert db.intransaction == ["test_method1"]

    def test_method2(self, db):
        assert db.intransaction == ["test_method2"]
```
