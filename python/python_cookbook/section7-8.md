# section 7 and 8 about python cookbook

## 函数

### * 强制位置参数

`func(self, value, /)`

It signifies the end of the positional only parameters, parameters you cannot use as keyword parameters.

[stackoverflow anwser](https://stackoverflow.com/questions/24735311/what-does-the-slash-mean-in-help-output/24735582#24735582)

[PEP 570](https://www.python.org/dev/peps/pep-0570/)

[PEP 457](https://www.python.org/dev/peps/pep-0457/)

### * 强制关键字参数

将强制关键字参数放到某个`*`参数或者单个`*`后面就能达到这种效果。比如：

```py
def recv(maxsize, *, block):
    'Receives a message'
    pass

recv(1024, True) # TypeError
recv(1024, block=True) # Ok
```

### 默认值函数

__默认参数的值应该是不可变的对象，比如None、True、False、数字或字符串__。 不可为可变对象。

__检查`None`时应该使用`is`__。

检测用户是否传入了可选参数。可以将参数默认值设置为一个用户无法输入的实例，例如`object()`。

### 减少可调用对象的参数个数

`from functools import partial`

### * 闭包

一个闭包本质是一个函数，不过维持了一个额外的域，它会记住自己被定义时的环境。

### * 带额外状态信息的回调函数

[sourece](https://python3-cookbook.readthedocs.io/zh_CN/latest/c07/p10_carry_extra_state_with_callback_functions.html)

类实例、闭包、协程

### * 访问闭包中定义的变量

```py
def sample():
    n = 0
    # Closure function
    def func():
        print('n=', n)

    # Accessor methods for n
    def get_n():
        return n

    def set_n(value):
        nonlocal n
        n = value

    # Attach as function attributes
    func.get_n = get_n
    func.set_n = set_n
    return func
```

## 类和对象

### __slots__

当你定义`__slots__`后，Python就会为实例使用一种更加紧凑的内部表示。 实例通过一个很小的固定大小的数组来构建，而不是为每个实例定义一个字典，这跟元组或列表很类似。在`__slots__`中列出的属性名在内部被映射到这个数组的指定小标上。 使用slots一个不好的地方就是我们不能再给实例添加新的属性了，只能使用在`__slots__`中定义的那些属性名。

关于`__slots__`的一个常见误区是 __它可以作为一个封装工具来防止用户给实例增加新的属性__。尽管使用`slots`可以达到这样的目的，但是这个并不是它的初衷。`__slots__`更多的是用来作为一个内存优化工具。

### 让对象支持上下文管理协议

```py
class LazyConnection:
    def __init__(self, address, family=AF_INET, type=SOCK_STREAM):
        self.address = address
        self.family = family
        self.type = type
        self.sock = None

    def __enter__(self):
        if self.sock is not None:
            raise RuntimeError('Already connected')
        self.sock = socket(self.family, self.type)
        self.sock.connect(self.address)
        return self.sock

    def __exit__(self, exc_ty, exc_val, tb):
        self.sock.close()
        self.sock = None
```

这个类的关键特点在于它表示了一个网络连接，但是初始化的时候并不会做任何事情(比如它并没有建立一个连接)。 __连接的建立和关闭是使用 with 语句自动完成的。__

当出现 with 语句的时候，对象的 `__enter__()` 方法被触发， 它返回的值(如果有的话)会被赋值给 as 声明的变量。然后，with 语句块里面的代码开始执行。 最后，`__exit__()` 方法被触发进行清理工作。

__不管 with 代码块中发生什么，上面的控制流都会执行完，就算代码块中发生了异常也是一样的__。 事实上，`__exit__()` 方法的三个参数包含了异常类型、异常值和追溯信息(如果有的话)。` __exit__()` 方法能自己决定怎样利用这个异常信息，或者忽略它并返回一个`None`值。 如果 `__exit__()` 返回 `True` ，那么异常会被清空，就好像什么都没发生一样，`with`语句后面的程序继续在正常执行。

### 在类中封装属性名

__Python程序员不去依赖语言特性去封装数据，而是通过遵循一定的属性和方法命名规约来达到这个效果。__

```py
class B:
    def __init__(self):
        self.__private = 0

    def __private_method(self):
        pass

    def public_method(self):
        pass
        self.__private_method()
```

使用 __双下划线__ 开始会导致访问名称变成其他形式。 比如，在前面的类B中，私有属性会被分别重命名为`_B__private`和 `_B__private_method`。 这时候你可能会问这样重命名的目的是什么，__答案就是继承——这种属性通过继承是无法被覆盖的。__

### 可管理的属性（@property使用方法）

```py
class Person:
    def __init__(self, first_name):
        self._first_name = first_name

    # Getter function
    @property
    def first_name(self):
        return self._first_name

    # Setter function
    @first_name.setter
    def first_name(self, value):
        if not isinstance(value, str):
            raise TypeError('Expected a string')
        self._first_name = value

    # Deleter function (optional)
    @first_name.deleter
    def first_name(self):
        raise AttributeError("Can't delete attribute")
```

上述代码中有三个相关联的方法，__这三个方法的名字都必须一样__。 第一个方法是一个`getter`函数，它使得`first_name`成为一个属性。 其他两个方法给`first_name`属性添加了`setter`和`deleter`函数。需要强调的是只有在`first_name`属性被创建后，后面的两个装饰器`@first_name.setter` 和 `@first_name.deleter` 才能被定义。

`property`的一个关键特征是它看上去跟普通的`attribute`没什么两样， 但是访问它的时候会自动触发`getter`、`setter` 和 `deleter`方法。

### 调用父类方法

`super()`的原理

对于你定义的每一个类，Python会计算出一个所谓的`方法解析顺序(MRO)列表`。 这个`MRO列表`就是一个简单的所有基类的线性顺序表。

实际上就是合并所有父类的MRO列表并遵循如下三条准则:

- 子类会先于父类被检查
- 多个父类会根据它们在列表中的顺序被检查
- 如果对下一个类存在两个合法的选择，选择第一个父类

__当你使用`super()`函数时，Python会在MRO列表上继续搜索下一个类。只要每个重定义的方法统一使用`super()`并只调用它一次，那么控制流最终会遍历完整个`MRO`列表，每个方法也只会被调用一次。__

### 描述器（Descriptors）

描述器的并不存储实际数据，而是接受实例通过`self.__dict__['key']`对属性进行额外的操作（比如：类型检测）。

通过描述器可以捕获核心的实例操作（get、set、delete）,并且可以完全定义它们的行为。

描述器必须定义为类属性。

```py
# Descriptor attribute for an integer type-checked attribute
class Integer:
    def __init__(self, name):
        self.name = name

    def __get__(self, instance, cls):
        if instance is None:
            return self
        else:
            return instance.__dict__[self.name]

    def __set__(self, instance, value):
        if not isinstance(value, int):
            raise TypeError('Expected an int')
        instance.__dict__[self.name] = value

    def __delete__(self, instance):
        del instance.__dict__[self.name]
```

```py
class Point:
    x = Integer('x')
    y = Integer('y')

    def __init__(self, x, y):
        self.x = x
        self.y = y
```

```sh
>>> p = Point(2, 3)
>>> p.x # Calls Point.x.__get__(p,Point)
2
>>> p.y = 5 # Calls Point.y.__set__(p, 5)
>>> p.x = 2.3 # Calls Point.x.__set__(p, 2.3)
```

#### references

[Understanding __get__ and __set__ and Python descriptors](https://stackoverflow.com/questions/3798835/understanding-get-and-set-and-python-descriptors)

### 使用延迟计算属性

[example](https://python3-cookbook.readthedocs.io/zh_CN/latest/c08/p10_using_lazily_computed_properties.html#id1)

> 当一个描述器被放入一个类的定义时，每次访问属性时它的 `__get__()`、`__set__()` 和 `__delete__()` 方法就会被触发。不过，如果一个描述器仅仅只定义了一个`__get__()`方法的话，它比通常的具有更弱的绑定。特别地，只有当被访问属性不在实例底层的字典中时`__get__()`方法才会被触发。

### 实现数据模型的类型约束

[描述器、类装饰器、元类、混入类、使用装饰器代替混入类](https://python3-cookbook.readthedocs.io/zh_CN/latest/c08/p13_implementing_data_model_or_type_system.html#id1)

### 代理模式

`__getattr__`:

在访问attribute不存在的时候被调用。如果代理类实例本身有这个属性的话，那么不会触发这个方法的。另外，`__setattr__()`和`__delattr__()` 需要额外的魔法来区分代理实例和被代理实例`_obj`的属性。__一个通常的约定是只代理那些不以下划线`_`开头的属性(代理类只暴露被代理类的公共属性)__。

需要注意的是，`__getattr__()`对于大部分以`双下划线(__)开始和结尾的属性`并不适用。

实现代理模式

```py
# A proxy class that wraps around another object, but
# exposes its public attributes
class Proxy:
    def __init__(self, obj):
        self._obj = obj

    # Delegate attribute lookup to internal obj
    def __getattr__(self, name):
        print('getattr:', name)
        return getattr(self._obj, name)

    # Delegate attribute assignment
    def __setattr__(self, name, value):
        if name.startswith('_'):
            super().__setattr__(name, value)
        else:
            print('setattr:', name, value)
            setattr(self._obj, name, value)

    # Delegate attribute deletion
    def __delattr__(self, name):
        if name.startswith('_'):
            super().__delattr__(name)
        else:
            print('delattr:', name)
            delattr(self._obj, name)
```

### 定义多个构造器

__类方法的一个主要用途就是定义多个构造器。它接受一个`class`作为第一个参数(cls)。你应该注意到了这个类被用来创建并返回最终的实例。__

```py
import time

class Date:
    """方法一：使用类方法"""
    # Primary constructor
    def __init__(self, year, month, day):
        self.year = year
        self.month = month
        self.day = day

    # Alternate constructor
    @classmethod
    def today(cls):
        t = time.localtime()
        return cls(t.tm_year, t.tm_mon, t.tm_mday)
```

### 状态对象或状态机

[将每种状态转换为一个对象。(状态模式)](https://python3-cookbook.readthedocs.io/zh_CN/latest/c08/p19_implements_stateful_objects_or_state_machines.html)

### 通过字符串调用方法

- getattr
- operation.methodcaller

    创建一个可调用对象，并同时提供所有必要参数，然后调用的时候只需要将实例对象传递给它即可。

### 访问者模式

理解不深

### 不用递归实现访问者模式

[太吓人了](https://python3-cookbook.readthedocs.io/zh_CN/latest/c08/p22_implementing_visitor_pattern_without_recursion.html#id1)

### 循环引用数据结构的内存管理（如何使用弱引用）

python的垃圾回收机制基于简单的引用计数，当出现循环引用时，引用永远无法为0，导致实例无法被删除。

虽然python中有专门的垃圾回收机制处理循环引用问题，不过无法确定它何时执行。当然也可以通过

```py
import gc
gc.collect()
```

手动清除，不过这种方式并不推荐。

对于这个问题可以使用`弱引用（weakref）`。

本质上讲，弱引用就是一个对象指针，它不会增加引用计数。为了访问弱引用所引用的对象，你可以像函数一样去调用它即可。如果那个对象还存在就会返回它，否则就返回一个`None`。

### 让类支持比较操作

装饰器`functools.total_ordering`就是用来简化这个处理的。使用它来装饰一个类，你只需定义一个`__eq__()`方法， 外加其他方法(`__lt__`, `__le__`, `__gt__`, or `__ge__`)中的一个即可。然后装饰器会自动为你填充其它比较方法。