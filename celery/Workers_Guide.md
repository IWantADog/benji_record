# Workers Guide

## Starting the worker

[daemonizing](https://docs.celeryproject.org/en/master/userguide/daemonizing.html#daemonizing)

### Example

```sh
celery -A proj worker -l INFO
```

```sh
celery worker --help
```

You can start __multiple workers__ on the same machine, but be sure to name each individual worker by specifying a node name with the `--hostname` argument:

```sh
celery -A proj worker --loglevel=INFO --concurrency=10 -n worker1@%h

celery -A proj worker --loglevel=INFO --concurrency=10 -n worker2@%h

celery -A proj worker --loglevel=INFO --concurrency=10 -n worker3@%h
```

Variable |Template    | Result
---------|------------|--------------------------|
%h       | worker1@%h |worker1@george.example.com|
%n       | worker1@%n | worker1@george           |
%d       |worker1@%d  | worker1@example.com      |

## Stopping the worker

__When shutdown is initiated the worker will finish all currently executing tasks before it actually terminates.__ If these tasks are important, you should wait for it to finish before doing anything drastic, like sending the KILL signal.

__If the worker won’t shutdown after considerate time, for being stuck in an infinite-loop or similar, you can use the KILL signal to force terminate the worker: but be aware that currently executing tasks will be lost (i.e., unless the tasks have the acks_late option set).__

Also as processes can’t override the KILL signal, the worker will not be able to reap its children; make sure to do so manually. This command usually does the trick:

`$ pkill -9 -f 'celery worker'`

If you don’t have the pkill command on your system, you can use the slightly longer version:

`$ ps auxww | awk '/celery worker/ {print $2}' | xargs kill -9`

## Restarting the worker

To restart the worker you should send the TERM signal and start a new instance. The easiest way to manage workers for development is by using celery multi:

```sh
celery multi start 1 -A proj -l INFO -c4 --pidfile=/var/run/celery/%n.pid

celery multi restart 1 --pidfile=/var/run/celery/%n.pid
```

__For production deployments you should be using init-scripts or a process supervision system (see Daemonization).__

Other than stopping, then starting the worker to restart, you can also restart the worker using the `HUP` signal. Note that the worker will be responsible for restarting itself so this is prone to problems and isn’t recommended in production:

`$ kill -HUP $pid`

> Restarting by `HUP` only works if the worker is running in the background as a daemon (it doesn’t have a controlling terminal).

## Process Signals

## Variables in file paths

### Node name replacements

- %p: Full node name.

- %h: Hostname, including domain name.

- %n: Hostname only.

- %d: Domain name only.

- %i: Prefork pool process index or 0 if MainProcess.

- %I: Prefork pool process index with separator.

### Prefork pool process index

This can be used to specify one log file per child process.

## Concurrency

`By default multiprocessing is used to perform concurrent execution of tasks`, but you can also use Eventlet. The number of worker processes/threads can be changed using the --concurrency argument and __defaults to the number of CPUs available on the machine.__

### Concurrency with Eventlet

[origin link](https://docs.celeryproject.org/en/master/userguide/concurrency/eventlet.html#concurrency-eventlet)

### Remote Control

Workers have the ability to be remote controlled using a high-priority broadcast message queue. The commands can be directed to all, or a specific list of workers.

### The broadcast function

This is the client function used to send commands to the workers. Some remote control commands also have higher-level interfaces using `broadcast()` in the background, like `rate_limit()`, and `ping()`.

```py
>>> app.control.broadcast('rate_limit',
...  arguments={'task_name': 'myapp.mytask','rate_limit': '200/m'})
```

## Commands

### revoke: Revoking tasks

All worker nodes keeps a memory of revoked task ids, either in-memory or persistent on disk (see [Persistent revokes](https://docs.celeryproject.org/en/master/userguide/workers.html#worker-persistent-revokes)).

__When a worker receives a revoke request it will skip executing the task, but it won’t terminate an already executing task unless the terminate option is set.__

> The _terminate_ option is a last resort for administrators when a task is stuck. __It’s not for terminating the task, it’s for terminating the process that’s executing the task, and that process may have already started processing another task at the point when the signal is sent, so for this reason you must never call this programmatically.__

### Revoking multiple tasks

The revoke method also accepts a list argument, where it will revoke several tasks at once.

```py
>>> app.control.revoke([
...    '7993b0aa-1f0b-4780-9af0-c47c0858b3f2',
...    'f565793e-b041-4b2b-9ca4-dca22762a55d',
...    'd9d35e03-2997-42d0-a13e-64a66b88a618',
])
```

### Persistent revokes

__Revoking tasks works by sending a broadcast message to all the workers, the workers then keep a list of revoked tasks in memory. When a worker starts up it will synchronize revoked tasks with other workers in the cluster.__

__The list of revoked tasks is in-memory so if all workers restart the list of revoked ids will also vanish__. If you want to preserve this list between restarts you need to specify a file for these to be stored in by using the _–statedb_ argument to celery worker:

`$ celery -A proj worker -l INFO --statedb=/var/run/celery/worker.state`

or if you use celery multi you want to create one file per worker instance so use the %n format to expand the current node name:

`celery multi start 2 -l INFO --statedb=/var/run/celery/%n.state`

## Time Limits

>pool support: prefork/gevent

A single task can potentially run forever, if you have lots of tasks waiting for some event that’ll never happen you’ll block the worker from processing new tasks indefinitely. __The best way to defend against this scenario happening is enabling time limits.__

The time limit `(–time-limit)` is the maximum number of seconds a task may run before the process executing it is terminated and replaced by a new process. __You can also enable a soft time limit `(–soft-time-limit)`, this raises an exception the task can catch to clean up before the hard time limit kills it.__

### Soft, or hard

The time limit is set in two values, soft and hard. The soft time limit allows the task to catch an exception to clean up before it is killed: the hard timeout isn’t catch-able and force terminates the task.

### Changing time limits at run-time

> broker support: amqp, redis

There’s a remote control command that enables you to change both soft and hard time limits for a task — named time_limit.

__Only tasks that starts executing after the time limit change will be affected.__

```py
>>> app.control.time_limit('tasks.crawl_the_web',
                           soft=60, hard=120, reply=True)
[{'worker1.example.com': {'ok': 'time limits set successfully'}}]
```

## Rate Limits

```py
>>> app.control.rate_limit('myapp.mytask', '200/m',
...            destination=['celery@worker1.example.com'])
```

## Max tasks per child setting

> pool support: prefork

With this option you can configure the maximum number of tasks a worker can execute before it’s replaced by a new process.

## Max memory per child setting

> pool support: prefork

With this option you can configure the maximum amount of resident memory a worker can execute before it’s replaced by a new process.

## Autoscaling

> pool support: prefork, gevent

The autoscaler component is used to _dynamically_ resize the pool based on load:

- The autoscaler adds more pool processes when there is work to do,
- and starts removing processes when the workload is low.

It’s enabled by the `--autoscale` option, which needs two numbers: _the maximum and minimum number of pool processes_

## Queues

__A worker instance can consume from any number of queues.__ By default it will consume from all queues defined in the task_queues setting (that if not specified falls back to the default queue named _celery_).

You can specify what queues to consume from at start-up, by giving a comma separated list of queues to the -Q option:

`$ celery -A proj worker -l INFO -Q foo,bar,baz`

### configration

- task_queues: define task queues
- task_create_missing_queues: Celery use it create new queue when a queue name not defined in task_queueus
- add_consumer & cancel_consumer: start/stop worker consuming  from a queueu in run-time

### Queues: Adding consumers

`$ celery -A proj control add_consumer foo`

`$ celery -A proj control add_consumer foo -d celery@worker1.local`

`>>> app.control.add_consumer('foo', reply=True)`

`>>> app.control.add_consumer('foo', reply=True,destination=['worker1@example.com'])`

### Queues: Canceling consumers

`$ celery -A proj control cancel_consumer foo`

`$ celery -A proj control cancel_consumer foo -d celery@worker1.local`

`>>> app.control.cancel_consumer('foo', reply=True)`

### Queues: List of active queues

`$ celery -A proj inspect active_queues`

`$ celery -A proj inspect active_queues -d celery@worker1.local`

`>>> app.control.inspect().active_queues()`

`>>> app.control.inspect(['worker1.local']).active_queues()`

## Inspecting workers

`app.control.inspect` lets you inspect running workers.

```py
>>> # Inspect all nodes.
>>> i = app.control.inspect()

>>> # Specify multiple nodes to inspect.
>>> i = app.control.inspect(['worker1.example.com',
                            'worker2.example.com'])

>>> # Specify a single node to inspect.
>>> i = app.control.inspect('worker1.example.com')
```

Dump of registered tasks: `i.registered()`

Dump of currently executing tasks: `i.active()`

Dump of scheduled (ETA) tasks: `i.scheduled()`

Dump of reserved tasks: `i.reserved()`

### Statistics

The remote control command inspect stats (or stats()) will give you a long list of useful (or not so useful) statistics about the worker:

`$ celery -A proj inspect stats`

## Additional Commands

https://docs.celeryproject.org/en/master/userguide/workers.html#additional-commands

## Writing your own remote control commands

https://docs.celeryproject.org/en/master/userguide/workers.html#writing-your-own-remote-control-commands
