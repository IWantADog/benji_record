# Routing Tasks

## Basics

The simplest way to do routing is to use the `task_create_missing_queues` setting (__on by default__).

With this setting on, a named queue that’s not already defined in task_queues will be created automatically.

### Automatic routing

`task_routes = {'feed.tasks.import_feed': {'queue': 'feeds'}}`

```py
# use glob pattern matching, or even regular expressions
app.conf.task_routes = {'feed.tasks.*': {'queue': 'feeds'}}
```

```py
# If the order of matching patterns is important you should specify the router in items format instead

task_routes = ([
    ('feed.tasks.*', {'queue': 'feeds'}),
    ('web.tasks.*', {'queue': 'web'}),
    (re.compile(r'(video|image)\.tasks\..*'), {'queue': 'media'}),
],)
```

start server to process the feeds queue: `user@z:/$ celery -A proj worker -Q feeds`

#### Changing the name of the default queue

`app.conf.task_default_queue = 'default'`

#### How the queues are defined

## Manual routing

don't understand

## Special Routing Options

### RabbitMQ Message Priorities

> supported: transports
RabbitM

```py
from kombu import Exchange, Queue

app.conf.task_queues = [
    Queue('tasks', Exchange('tasks'), routing_key='tasks',
          queue_arguments={'x-max-priority': 10}),
]
```

A default value for __all queues__ can be set using the `task_queue_max_priority` setting:

`app.conf.task_queue_max_priority = 10`

A default priority for __all tasks__ can also be specified using the `task_default_priority` setting:

`app.conf.task_default_priority = 5`

### Redis Message Priorities

__While the Celery Redis transport does honor the priority field, Redis itself has no notion of priorities.__

To start scheduling tasks based on priorities you need to configure queue_order_strategy transport option.

```py
app.conf.broker_transport_options = {
    'queue_order_strategy': 'priority',
}
```

The priority support is implemented by creating n lists for each queue. This means that even though there are 10 (0-9) priority levels, these are consolidated into 4 levels by default to save resources. This means that a queue named celery will really be split into 4 queues:

`['celery0', 'celery3', 'celery6', 'celery9']`

If you want more priority levels you can set the priority_steps transport option:

```py
app.conf.broker_transport_options = {
    'priority_steps': list(range(10)),
    'queue_order_strategy': 'priority',
}
```

## AMQP Primer

### Messages

__A message consists of headers and a body. Celery uses headers to store the content type of the message and its content encoding. The content type is usually the serialization format used to serialize the message.__ The body contains the name of the task to execute, the task id (UUID), the arguments to apply it with and some additional meta-data – like the number of retries or an ETA.

### Producers, consumers, and brokers

The client sending messages is typically called a _publisher_, or a _producer_, while the entity receiving messages is called a _consumer_.

The _broker_ is the message server, routing messages from producers to consumers.

### Exchanges, queues, and routing keys

1. Messages are sent to exchanges.

2. An exchange routes messages to one or more queues. Several exchange types exists, providing different ways to do routing, or implementing different messaging scenarios.

3. The message waits in the queue until someone consumes it.

4. sThe message is deleted from the queue when it has been acknowledged.

### Exchange types

__The exchange type defines how the messages are routed through the exchange.__ The exchange types defined in the standard are `direct`, `topic`, `fanout` and `headers`. Also non-standard exchange types are available as plug-ins to RabbitMQ, like the last-value-cache plug-in by Michael Bridgen.

#### Direct exchanges

Direct exchanges match by exact routing keys, so a queue bound by the routing key video only receives messages with that routing key.

#### Topic exchanges

Topic exchanges matches routing keys using dot-separated words, and the wild-card characters: `*` (__matches a single word__), and `#` (__matches zero or more words__).

### Related API commands

https://docs.celeryproject.org/en/master/userguide/routing.html#related-api-commands

### Hands-on with the API

https://docs.celeryproject.org/en/master/userguide/routing.html#hands-on-with-the-api

## Routing Tasks

### Defining queues

```py
default_exchange = Exchange('default', type='direct')
media_exchange = Exchange('media', type='direct')

app.conf.task_queues = (
    Queue('default', default_exchange, routing_key='default'),
    Queue('videos', media_exchange, routing_key='media.video'),
    Queue('images', media_exchange, routing_key='media.image')
)
app.conf.task_default_queue = 'default'
app.conf.task_default_exchange = 'default'
app.conf.task_default_routing_key = 'default'
```

```py
from kombu import Exchange, Queue, binding

media_exchange = Exchange('media', type='direct')

CELERY_QUEUES = (
    Queue('media', [
        binding(media_exchange, routing_key='media.video'),
        binding(media_exchange, routing_key='media.image'),
    ]),
)
```

### Specifying task destination

The destination for a task is decided by the following (in order):

1. The routing arguments to Task.apply_async().

2. Routing related attributes defined on the Task itself.

3. The Routers defined in [task_routes](https://docs.celeryproject.org/en/master/userguide/configuration.html#std-setting-task_routes).

### Router

A router is a function that decides the routing options for a task.

All you need to define a new router is to define `a function with the signature (name, args, kwargs, options, task=None, **kw):`

#### Priority Order and Cluster Responsiveness

It is important to note that, due to worker prefetching, if a bunch of tasks submitted at the same time they may be out of priority order at first. Disabling worker prefetching will prevent this issue, but may cause less than ideal performance for small, fast tasks. In most cases, simply reducing worker_prefetch_multiplier to 1 is an easier and cleaner way to increase the responsiveness of your system without the costs of disabling prefetching entirely.

Note that priorities values are sorted in reverse when using the redis broker: 0 being highest priority.

### Broadcast

Celery can also support broadcast routing. Here is an example exchange broadcast_tasks that delivers copies of tasks to all workers connected to it:

```py
from kombu.common import Broadcast

app.conf.task_queues = (Broadcast('broadcast_tasks'),)
app.conf.task_routes = {
    'tasks.reload_cache': {
        'queue': 'broadcast_tasks',
        'exchange': 'broadcast_tasks'
    }
}
```

Here is another example of broadcast routing, this time with a celery beat schedule:

```py
from kombu.common import Broadcast
from celery.schedules import crontab

app.conf.task_queues = (Broadcast('broadcast_tasks'),)

app.conf.beat_schedule = {
    'test-task': {
        'task': 'tasks.reload_cache',
        'schedule': crontab(minute=0, hour='*/3'),
        'options': {'exchange': 'broadcast_tasks'}
    },
}
```

## Don't understand

- Topic exchanges
