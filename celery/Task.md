# Task

A task is a class that can be created out of any callable. It performs dual roles in that it defines both what happens when a task is called (sends a message), and what happens when a worker receives that message.

The default prefork pool scheduler is not friendly to long-running tasks, so if you have tasks that run for minutes/hours make sure you enable the -Ofair command-line argument to the celery worker. See Prefetch Limits for more information, and for the best performance route long-running and short-running tasks to dedicated workers (Automatic routing).

## Basics

### Bound tasks

```py
logger = get_task_logger(__name__)
# bind
@task(bind=True)
def add(self, x, y):
    logger.info(self.request.id)
```

Multiple decorators

When using multiple decorators in combination with the task decorator you must make sure that the task decorator is applied last (oddly, in Python this means it must be first in the list):

```py
@app.task
@decorator2
@decorator1
def add(x, y):
    return x + y
```

### Task inheritance

```py
import celery

class MyTask(celery.Task):

    def on_failure(self, exc, task_id, args, kwargs, einfo):
        print('{0!r} failed: {1!r}'.format(task_id, exc))

@task(base=MyTask)
def add(x, y):
    raise KeyError()
```

## Names

Every task must have a unique name.

If no explicit name is provided the task decorator will generate one for you, and this name will be based on `1) the module the task is defined in,` and `2) the name of the task function`.

> A best practice is to use the module name as a name-space, this way names won’t collide if there’s already a task with that name defined in another module.

### Automatic naming and relative imports

Relative imports and automatic name generation don’t go well together, so if you’re using relative imports you should set the name explicitly.

### Changing the automatic naming behavior

you can change the automatic naming behavior by overriding `app.gen_task_name()`.

```py
from celery import Celery

class MyCelery(Celery):

    def gen_task_name(self, name, module):
        if module.endswith('.tasks'):
            module = module[:-6]
        return super(MyCelery, self).gen_task_name(name, module)

app = MyCelery('main')
```

## Task Request

The `bind` argument means that the function will be a “bound method” so that you can access attributes and methods on the task type instance.

## Logging

The best practice is to create a common logger for all of your tasks at the top of your module.

## Retrying

`app.Task.retry()` can be used to re-execute the task, for example in the event of recoverable errors.

When you call retry it’ll send a new message, using the same task-id, and it’ll take care to make sure the message is delivered to the same queue as the originating task.

### Using a custom retry delay

When a task is to be retried, it can wait for a given amount of time before doing so, and the default delay is defined by the `default_retry_delay` attribute. `By default this is set to 3 minutes.` Note that the unit for setting the delay is in seconds (int or float).

### Automatic retry for known exceptions

#### Task.autoretry_for

`A list/tuple of exception classes.` If any of these exceptions are raised during the execution of the task, the task will automatically be retried. By default, no exceptions will be autoretried.

```py
from twitter.exceptions import FailWhaleError

@app.task(autoretry_for=(FailWhaleError,))
def refresh_timeline(user):
    return twitter.refresh_timeline(user)
```

#### Task.retry_kwargs

`A dictionary.` Use this to customize how autoretries are executed. Note that if you use the exponential backoff options below, the countdown task option will be determined by Celery’s autoretry system, and any countdown included in this dictionary will be ignored.

If you want to specify custom arguments for an internal retry() call, pass `retry_kwargs` argument to task() decorator:

```py
@app.task(autoretry_for=(FailWhaleError,),
          retry_kwargs={'max_retries': 5})
def refresh_timeline(user):
    return twitter.refresh_timeline(user)
```

#### Task.retry_backoff

`A boolean, or a number.` If this option is set to True, autoretries will be delayed following the rules of exponential backoff. The first retry will have a delay of 1 second, the second retry will have a delay of 2 seconds, the third will delay 4 seconds, the fourth will delay 8 seconds, and so on. (However, this delay value is modified by retry_jitter, if it is enabled.) If this option is set to a number, it is used as a delay factor. For example, if this option is set to 3, the first retry will delay 3 seconds, the second will delay 6 seconds, the third will delay 12 seconds, the fourth will delay 24 seconds, and so on. `By default, this option is set to False, and autoretries will not be delayed.`s

#### Task.retry_backoff_max

`A number.` If retry_backoff is enabled, this option will set a maximum delay in seconds between task autoretries. `By default, this option is set to 600, which is 10 minutes`s.

#### Task.retry_jitter

`A boolean.` Jitter is used to introduce randomness into exponential backoff delays, to prevent all tasks in the queue from being executed simultaneously. If this option is set to True, the delay value calculated by retry_backoff is treated as a maximum, and the actual delay value will be a random number between zero and that maximum. `By default, this option is set to True`.

## List of Options

### General

[origin link](https://docs.celeryproject.org/en/master/userguide/tasks.html#general)

## States

Celery can keep track of the tasks current state. The state also contains the result of a successful task, or the exception and traceback information of a failed task.

### Result Backends

`Backends use resources to store and transmit results. To ensure that resources are released, you must eventually call get() or forget() on EVERY AsyncResult instance returned after calling a task.`

### RPC Result Backend (RabbitMQ/QPid)

The RPC result backend (rpc://) is special as it doesn’t actually store the states, but rather sends them as messages. `This is an important difference as it means that a result can only be retrieved once, and only by the client that initiated the task. Two different processes can’t wait for the same result.`

`Even with that limitation, it is an excellent choice if you need to receive state changes in real-time. Using messaging means the client doesn’t have to poll for new states.`

The messages are transient (non-persistent) by default, so the results will disappear if the broker restarts. You can configure the result backend to send persistent messages using the `result_persistent` setting.

### Database Result Backend

Keeping state in the database can be convenient for many, especially for web applications with a database already in place, but it also comes with limitations.

- Polling the database for new states is expensive, and so you should increase the polling intervals of operations, such as result.get().

- Some databases use a default transaction isolation level that isn’t suitable for polling tables for changes.

  >In MySQL the default transaction isolation level is REPEATABLE-READ: meaning the transaction won’t see changes made by other transactions until the current transaction is committed.
  Changing that to the READ-COMMITTED isolation level is recommended.

### Built-in States

- PENDING
- STARTED
- SUCCESS
- FAILURE
- RETRY
- REVOKED

### Custom states

You can easily define your own states, all you need is a `unique` name. The name of the state is usually an `uppercase string`. As an example you could have a look at the abortable tasks which defines a custom ABORTED state.

### Creating pickleable exceptions

A rarely known Python fact is that exceptions must conform to some simple rules to support being serialized by the pickle module.

To make sure that your exceptions are pickleable the exception MUST provide the original arguments it was instantiated with in its .args attribute. `The simplest way to ensure this is to have the exception call Exception.__init__.`

> So the rule is: For any exception that supports custom arguments `*args`, `Exception.__init__(self, *args)` must be used.

## Semipredicates

The worker wraps the task in a tracing function that records the final state of the task. There are a number of exceptions that can be used to signal this function to change how it treats the return of the task.

### Ignore

The task may raise Ignore to force the worker to ignore the task. `This means that no state will be recorded for the task, but the message is still acknowledged (removed from queue).`

This can be used if you want to implement custom revoke-like functionality, or manually store the result of a task.

### Reject

The task may raise Reject to reject the task message using AMQP `basic_reject` method. This won’t have any effect unless Task.acks_late is enabled.

### Retry

The `Retry` exception is raised by the `Task.retry` method to tell the worker that the task is being retried.

## Custom task classes

### instantiation

`A task is not instantiated for every request, but is registered in the task registry as a global instance.`

This means that the __init__ constructor will only be called once per process, and that the task class is semantically closer to an Actor.

### Per task usage

```py
@app.task(base=DatabaseTask)
def process_rows():
    for row in process_rows.db.table.all():
        process_row(row)
```

The db attribute of the process_rows task will then always stay the same in each process

### App-wide usage

```py
from celery import Celery

app = Celery('tasks', task_cls='your.module.path:DatabaseTask')
```

This will make all your tasks declared using the decorator syntax within your app to use your `DatabaseTask` class and will all have a db attribute.

`The default value is the class provided by Celery: 'celery.app.task:Task'.`

### Handlers

`after_return`: Handler called after the task returns.

`on_failure`: This is run by the worker when the task fails.

`on_retry`: This is run by the worker when the task is to be retried.

`on_success`: Run by the worker if the task executes successfully.

### Requests and custom requests

`Upon receiving a message to run a task, the worker creates a request to represent such demand.`

Custom task classes may override which request class to use by changing the attribute celery.app.task.Task.Request. You may either assign the custom request class itself, or its fully qualified name.

The request has several responsibilities. Custom request classes should cover them all – they are responsible to actually run and trace the task. `We strongly recommend to inherit from celery.worker.request.Request.`

## ** How it works

All defined tasks are listed in a registry. The registry contains a list of task names and their task classes. You can investigate this registry yourself:

```py
>>> from proj.celery import app
>>> app.tasks
{'celery.chord_unlock':
    <@task: celery.chord_unlock>,
 'celery.backend_cleanup':
    <@task: celery.backend_cleanup>,
 'celery.chord':
    <@task: celery.chord>}
```

This is the list of tasks built into Celery. Note that tasks will only be registered when the module they’re defined in is imported.

__The app.task() decorator is responsible for registering your task in the applications task registry.__

__When tasks are sent, no actual function code is sent with it, just the name of the task to execute. When the worker then receives the message it can look up the name in its task registry to find the execution code.__

This means that your workers should always be updated with the same software as the client. This is a drawback, but the alternative is a technical challenge that’s yet to be solved.

## Tips and Best Practices

If you don’t care about the results of a task, be sure to set the `ignore_result` option, as storing results wastes time and resources.

```py
@app.task(ignore_result=True)
def mytask():
    something()
```

Results can even be disabled globally using the `task_ignore_result` setting.

Results can be enabled/disabled on a per-execution basis, by passing the `ignore_result` boolean parameter, when calling `apply_async` or `delay`.

__By default tasks will not ignore results (ignore_result=False) when a result backend is configured.__

The option precedence order is the following:

1. Global `task_ignore_result`

2. `ignore_result` option

3. Task execution option `ignore_result`

### More optimization tips

[document link](https://docs.celeryproject.org/en/master/userguide/optimizing.html#guide-optimizing)

### Avoid launching synchronous subtasks

```py
def update_page_info(url):
    # fetch_page -> parse_page -> store_page
    chain = fetch_page.s(url) | parse_page.s() | store_page_info.s(url)
    chain()

@app.task()
def fetch_page(url):
    return myhttplib.get(url)

@app.task()
def parse_page(page):
    return myparser.parse_document(page)

@app.task(ignore_result=True)
def store_page_info(info, url):
    PageInfo.objects.create(url=url, info=info)
```

## Performance and Strategies

### Granularity

The task granularity is the amount of computation needed by each subtask. In general it is better to split the problem up into many small tasks rather than have a few long running tasks.

With smaller tasks you can process more tasks in parallel and the tasks won’t run long enough to block the worker from processing other waiting tasks.

However, executing a task does have overhead. A message needs to be sent, data may not be local, etc. __So if the tasks are too fine-grained the overhead added probably removes any benefit.__

### Data locality

The worker processing the task should be as close to the data as possible. The best would be to have a copy in memory, the worst would be a full transfer from another continent.

If the data is far away, you could try to run another worker at location, or if that’s not possible - cache often used data, or preload data you know is going to be used.

The easiest way to share data between workers is to use a distributed cache system, like [memcached](http://memcached.org/).

### State

Another gotcha is Django model objects. They shouldn’t be passed on as arguments to tasks. It’s almost always better to re-fetch the object from the database when the task is running instead, as using old data may lead to race conditions.

## Database transactions

...

## Example

[origin link](https://docs.celeryproject.org/en/master/userguide/tasks.html#task-example)
