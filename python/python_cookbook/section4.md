# section4

## 带有外部状态的生成器函数

如果你想让你的生成器暴露外部状态给用户，你可以简单的将它实现为一个类，然后把生成器函数放到`__iter__()`方法中过去。比如：

```py
from collections import deque

class linehistory:
    def __init__(self, lines, histlen=3):
        self.lines = lines
        self.history = deque(maxlen=histlen)

    def __iter__(self):
        for lineno, line in enumerate(self.lines, 1):
            self.history.append((lineno, line))
            yield line

    def clear(self):
        self.history.clear()
```

## itertools

当我们碰到看上去有些复杂的迭代问题时，最好可以先去看看itertools模块

### 在迭代中跳过开头的部分数据

`itertools.dropwhile()`函数。使用时，你给它传递一个函数对象和一个可迭代对象。它会返回一个迭代器对象，丢弃原有序列中直到函数返回Flase之前的所有元素，然后返回后面所有元素。

### 迭代器切片

`itertools.islice()`

```py
def count(n):
    while True:
        yield n
        n += 1

import itertools
>>> for x in itertools.islice(c, 10, 20):
...     print(x)
```

### 对多个在不同容器中的对象进行迭代

`itertools.chain()`

## 同时遍历多个序列

`zip` and `zip_longest`

__`zip()`会创建一个迭代器来作为结果返回。如果你需要将结对的值存储在列表中，要使用`list()`函数__

## 顺序迭代合并后的排序迭代对象

`heapq.merge()`

## 迭代器代替while无限循环

`iter`函数一个鲜为人知的特性是它接受一个可选的`callable`对象和一个标记(结尾)值作为输入参数。当以这种方式使用的时候，它会创建一个迭代器，这个迭代器会不断调用`callable`对象直到返回值和标记值相等为止。
