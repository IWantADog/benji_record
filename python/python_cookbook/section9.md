# section 9 about python cookbook

## 创建装饰器时保留函数元信息

`@warps(func)`

通过`__wrapped__`访问被包装函数。

## 带参数的装饰器

```py
@decorator(x, y, z)
def func(a, b):
    pass

# 等效于

def func(a, b):
    pass
func = decorator(x, y, z)(func)
```

## 运行时可修改属性的装饰器

```py
from functools import wraps, partial
import logging
# Utility decorator to attach a function as an attribute of obj
def attach_wrapper(obj, func=None):
    if func is None:
        return partial(attach_wrapper, obj)
    setattr(obj, func.__name__, func)
    return func

def logged(level, name=None, message=None):
    '''
    Add logging to a function. level is the logging
    level, name is the logger name, and message is the
    log message. If name and message aren't specified,
    they default to the function's module and name.
    '''
    def decorate(func):
        logname = name if name else func.__module__
        log = logging.getLogger(logname)
        logmsg = message if message else func.__name__

        @wraps(func)
        def wrapper(*args, **kwargs):
            log.log(level, logmsg)
            return func(*args, **kwargs)

        # Attach setter functions
        @attach_wrapper(wrapper)
        def set_level(newlevel):
            nonlocal level
            level = newlevel

        @attach_wrapper(wrapper)
        def set_message(newmsg):
            nonlocal logmsg
            logmsg = newmsg

        return wrapper

    return decorate

# Example use
@logged(logging.DEBUG)
def add(x, y):
    return x + y
```

## 带可选参数的装饰器

即可以传递参数，也可以选择不传递参数。

```py
from functools import wraps, partial
import logging

def logged(func=None, *, level=logging.DEBUG, name=None, message=None):
    if func is None:
        return partial(logged, level=level, name=name, message=message)

    logname = name if name else func.__module__
    log = logging.getLogger(logname)
    logmsg = message if message else func.__name__

    @wraps(func)
    def wrapper(*args, **kwargs):
        log.log(level, logmsg)
        return func(*args, **kwargs)

    return wrappe
```

## 函数签名检查

`inspect`中`Signature`和`Parameter`

## 将装饰器定义为类

描述器协议
[Advantages of Using MethodType in Python](https://stackoverflow.com/questions/37455426/advantages-of-using-methodtype-in-python)
[Understanding __get__ and __set__ and Python descriptors](https://stackoverflow.com/questions/3798835/understanding-get-and-set-and-python-descriptors)
[how to descriptor](https://docs.python.org/3/howto/descriptor.html)

## 为类和静态方法添加装饰器

给类或静态方法提供装饰器要确保装饰器在`@classmethod`或`@staticmethod`之前。

问题在于`@classmethod`和`@staticmethod`实际上并不会创建可直接调用的对象，而是创建特殊的描述器对象。

[Descriptor HowTo Guide](https://docs.python.org/3/howto/descriptor.html?highlight=descriptors)

## 使用类装饰器扩展类的功能

```py
def log_getattribute(cls):
    # Get the original implementation
    orig_getattribute = cls.__getattribute__

    # Make a new definition
    def new_getattribute(self, name):
        print('getting:', name)
        return orig_getattribute(self, name)

    # Attach to the class and return
    cls.__getattribute__ = new_getattribute
    return cls

# Example use
@log_getattribute
class A:
    def __init__(self,x):
        self.x = x
    def spam(self):
        pass
```

## 元类

[metaclasses](https://docs.python.org/3/reference/datamodel.html#metaclasses)

[PEP 3115](https://www.python.org/dev/peps/pep-3115/)

[PEP 3135 - New super](https://www.python.org/dev/peps/pep-3135/)

[what are metaclasses in python](https://stackoverflow.com/questions/100003/what-are-metaclasses-in-python)

[type](https://docs.python.org/3/library/functions.html#type)

[9.19-在定义的时候初始化类的成员](https://python3-cookbook.readthedocs.io/zh_CN/latest/c09/p19_initializing_class_members_at_definition_time.html)

## super

[consider python super](https://rhettinger.wordpress.com/2011/05/26/super-considered-super/amp/)

## 了解

[以编程方式定义类](https://python3-cookbook.readthedocs.io/zh_CN/latest/c09/p18_define_classes_programmatically.html)