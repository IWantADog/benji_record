# Working with the shell

## 创建一个`Request Context`

```py
ctx = app.test_request_context()
ctx.push()

do_something()

# 触发`before_request`和`after_request`等方法

app.preprocess_request()

ctx.pop()
```
