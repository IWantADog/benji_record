# document reading reacord

## Serving WSGI Applications

如何创建一个简单的内置server。

```py
from werkzeug.serving import run_simple
from myproject import make_app

app = make_app(...)
run_simple('localhost', 8080, app, use_reloader=True)
```

### Reloader

`reloader`监控web application的相关文件，但文件被修改时重启整个服务。

`werkzeug`支持两种`reloader`:
- `stat`: 默认配置，固定间隔检查文件的`mtime`（修改时间）。
- `watchdag`: 使用`filesystem event`，比`stat`更快。但需要`watchdog`依赖，推荐的办法是在配置文件中增加`Werkzeug[watchdog]`。如果`watchdag`已被安装，会自动使用；如果没有被安装，则默认使用`stat`。


