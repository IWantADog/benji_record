# python datemodel

[offical document](https://docs.python.org/3/reference/datamodel.html)

> `__new__()` to create it, and `__init__()` to customize it.

> So in our example, `x.f` is a valid method reference, since `MyClass.f` is a function, but `x.i` is not, since `MyClass.i` is not. But `x.f` is not the same thing as `MyClass.f` — it is a `method object`, not a `function object`.

> the special thing about methods is that the instance object is passed as the first argument of the function. In our example, the call `x.f()` is exactly equivalent to `MyClass.f(x)`. In general, calling a method with a list of n arguments is equivalent to calling the corresponding function with an argument list that is created by inserting the method’s instance object before the first argument.

[进度](https://docs.python.org/3/reference/datamodel.html#customizing-attribute-access)
