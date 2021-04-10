# section 14

## 异常链

捕获一个异常后继续抛出另一个异常。

```py
try:
    int('a')
except ValueError as e:
    raise RuntimeError('this is runtime error') from e
```

当捕获一个异常处理时如果再抛出一个异常，两个异常的信息都会保留。

```py
try:
    int('a')
except ValueError as e:
    print('in exception', err)
```

忽略异常链

`raise Exception('this is a exception') from None`

## 重新抛出捕获的异常

```py
try:
    int('a')
except ValueError as e:
    raise
```
