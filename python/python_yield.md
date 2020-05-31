# python yield

[官方文档](https://docs.python.org/3/reference/expressions.html?highlight=yield#generator-iterator-methods)

官方文档的解释十分详细，应优先阅读。

需要牢记的几点

1. 含有yield的函数，被称为生成器函数。调用生成器函数时函数不会立即执行，而是返回一个生成器对象，之后等待外部的触发。

2. `yield` 操作会使一个生成器函数返回一个并暂停。 接下来调用生成器的 `__next__()` 或 `send()` 方法又会让它从暂停处继续执行。

代码示例，便于理解

## 示例一

```py
def apply_async(func, args, *, callback):
    # Compute the result
    result = func(*args)

    # Invoke the callback with the result
    callback(result)
```

```py
from queue import Queue
from functools import wraps

class Async:
    def __init__(self, func, args):
        self.func = func
        self.args = args

def inlined_async(func):
    @wraps(func)
    def wrapper(*args):
        f = func(*args)
        result_queue = Queue()
        result_queue.put(None)
        while True:
            result = result_queue.get()
            try:
                a = f.send(result)
                apply_async(a.func, a.args, callback=result_queue.put)
            except StopIteration:
                break
    return wrapper
```

```py
def add(x, y):
    return x + y

@inlined_async
def test():
    r = yield Async(add, (2, 3))
    print(r)
    r = yield Async(add, ('hello', 'world'))
    print(r)
    for n in range(10):
        r = yield Async(add, (n, n))
        print(r)
    print('Goodbye')
```

运行`test()`运行结果

```sh
5
helloworld
0
2
4
6
8
10
12
14
16
18
Goodbye
```


## 示例二

```py
def func():
    x = 1
    while True:
        y = (yield x)
        x += y

generator = func()

next(generator) # 1
generator(4) # 5
generator(5) # 10
```
