# logging要点摘录

## Basic

对于简单的需求使用`basicConfig`，配置少，方便简洁。

`basicConfig`支持的功能可以通过初始化的参数来配置。支持的功能有日志写入文件、文件写入方式、日志格式、时间格式、日志报警最低级别、`handles`。具体如何使用参见[官方文档](https://docs.python.org/3.5/library/logging.html#logging.basicConfig)

```py
def main():
    logging.basicConfig(filename='myapp.log', level=logging.INFO)
    logging.info('Started')
    logging.info('Finished')

if __name__ == '__main__':
    main()
```

## Advanced

https://docs.python.org/3.5/howto/logging.html#advanced-logging-tutorial

### companent

- Loggers expose the interface that application code directly uses.
- Handlers send the log records (created by loggers) to the appropriate destination.
- Filters provide a finer grained facility for determining which log records to output.
- Formatters specify the layout of log records in the final output.

### namespace hierarchy

Logging is performed by calling methods on instances of the Logger class (hereafter called loggers). Each instance has a name, and they are conceptually arranged in a namespace hierarchy using dots (periods) as separators. For example, a logger named ‘scan’ is the parent of loggers ‘scan.text’, ‘scan.html’ and ‘scan.pdf’. Logger names can be anything you want, and indicate the area of an application in which a logged message originates.

### convention

`logger = logging.getLogger(__name__)`

### Loggers

Logger常用方法

- `Logger.setLevel()`
- `Logger.addHandle()` and `Logger.removeHandle()`
- `Logger.addFilter()` and `Logger.removeFilter()`

### Handlers

>It is, of course, possible to log messages to different destinations. Support is included in the package for writing log messages to files, HTTP GET/POST locations, email via SMTP, generic sockets, queues, or OS-specific logging mechanisms such as syslog or the Windows NT event log. Destinations are served by handler classes. You can create your own log destination class if you have special requirements not met by any of the built-in handler classes.

>As an example scenario, an application may want to send all log messages to a log file, all log messages of error or higher to stdout, and all messages of critical to an email address. This scenario requires three individual handlers where each handler is responsible for sending messages of a specific severity to a specific location.

`handlers`用于应对较复杂的情况。一个`logger`可以绑定多个`handler`。通过`handlers`可以将同一份日志输出按照不同的方式处理并发送到不同的地方。

logger中提供了一些内置的[useful handlers](https://docs.python.org/3.5/howto/logging.html#useful-handlers)

handle中常用的方法

- `setLevel()`
- `setFormatter()`
- `addFilter()` and `removeFilter()`

### Formatters

具体使用方法。传入参数初始化`Formatter`，之后通过`Handle.setFormatter()`将实例传入`handler`。

具体日志的格式参见[LogRecord attributes](https://docs.python.org/3.5/library/logging.html#logrecord-attributes)

### Filter

https://docs.python.org/3.5/library/logging.html#filter-objects

通过`Filter`可以实现比`levels`更加复杂的过滤。`Filter`可以实现对指定logger及其后代以外的日志进行过滤。

>Filters can be used by Handlers and Loggers for more sophisticated filtering than is provided by levels. The base filter class only allows events which are below a certain point in the logger hierarchy. For example, a filter initialized with ‘A.B’ will allow events logged by loggers ‘A.B’, ‘A.B.C’, ‘A.B.C.D’, ‘A.B.D’ etc. but not ‘A.BB’, ‘B.A.B’ etc. If initialized with the empty string, all events are passed.

## Configuring Logging

Programmers can configure logging in three ways:

1. Creating loggers, handlers, and formatters explicitly using Python code that calls the configuration methods listed above.
2. Creating a logging config file and reading it using the `fileConfig()` function.
3. Creating a dictionary of configuration information and passing it to the `dictConfig()` function.
