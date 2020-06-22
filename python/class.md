# python class 摘录

参考来源[python class](https://docs.python.org/3/tutorial/classes.html)

## function object and method object

```py
class MyClass:
    def f(self):
        pass

x = MyClass()
```

`MyClass.f`是一个`function object`，而`x.f`是一个`method object`。

`x.f`等价于`MyClass.f(x)`

## instance variable and class variable

如果相同的属性出现在实例和类中，调用时python优先寻找实例中的属性。

>If the same attribute name occurs in both an instance and in a class, then attribute lookup prioritizes the instance:

```py
>>> class Warehouse:
        purpose = 'storage'
        region = 'west'

>>> w1 = Warehouse()
>>> print(w1.purpose, w1.region)
storage west
>>> w2 = Warehouse()
>>> w2.region = 'east'
>>> print(w2.purpose, w2.region)
storage easts
```

当派生类覆盖了父类的方法，但又想要调用父类的该方法时，可以使用`BaseClassName.methodname(self, arguments)`

## private variables

在class中定义这样的变量（至少两个前下划线，至多一个后下划线）例如`__spam`，python会自动将其转换为`_className__spam`。这样做的唯一目的是避免派生类与父类变量名冲突。
