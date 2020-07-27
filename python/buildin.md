# Python Buildin

## functools

partial

[what is metaclass](https://stackoverflow.com/questions/100003/what-are-metaclasses-in-python)

## collections

nametuple:

- 只读
- 可以通过filed和index同时获取数据

deque:

- 支持两端append和pop，且时间复杂度接近O(1)
- 线程安全
- 可设置最大长度。如果设置最大长度，当增加数据时，数据以达到最大长度，会将数据从压入数据的另一方挤出。

ChainMap:

- https://docs.python.org/3.3/library/collections.html#chainmap-objects

Counter:

- 统计次数
- 接受iterable初始化时，自动统计item的次数，以item为key，以次数为values
- 接受Mapping，以key为key，以value为value

OrderDict:

- 迭代时按照item的添加顺序迭代
- 新增的元素排在最后

defaultdict:

- 向defaultdict中插入元素时，如果key不存在则调用default_factory。

UserDict & UserList & UserString:

- dict & list & string的包装类，便于定制开发功能
