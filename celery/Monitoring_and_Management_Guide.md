# Monitoring and Management Guide

## Workers

### Management Command-line Utilities (inspect/control)¶

#### Commands

https://docs.celeryproject.org/en/master/userguide/monitoring.html#commands

#### Specifying destination nodes

By default the inspect and control commands operates on all workers. You can specify a single, or a list of workers by using the `--destination` argument:

```
$ celery -A proj inspect -d w1@e.com,w2@e.com reserved

$ celery -A proj control -d w1@e.com,w2@e.com enable_events
```

### Flower: Real-time Celery web-monitor

#### Usage

install: `$ pip install flower`

run: `$ celery -A proj flower`

The default port is `http://localhost:5555`, but you can change this using the `–port` argument:

`$ celery -A proj flower --port=5555`

Broker URL can also be passed through the --broker argument :

`$ celery flower --broker=amqp://guest:guest@localhost:5672//`

[flower official document](https://flower.readthedocs.io/en/latest/)

### celery events: Curses Monitor

[reference link](https://docs.celeryproject.org/en/master/userguide/monitoring.html#celery-events-curses-monitor)

## RabbitMQ

To manage a Celery cluster it is important to know how RabbitMQ can be monitored.

### Inspecting queues

[refer linking](https://docs.celeryproject.org/en/master/userguide/monitoring.html#inspecting-queues)

## Redis

> Queue keys only exists when there are tasks in them, so if a key doesn’t exist it simply means there are no messages in that queue. This is because in Redis a list with no elements in it is automatically removed, and hence it won’t show up in the keys command output, and llen for that list returns 0.

> Also, if you’re using Redis for other purposes, the output of the keys command will include unrelated values stored in the database. The recommended way around this is to use a dedicated DATABASE_NUMBER for Celery, you can also use database numbers to separate Celery applications from each other (virtual hosts), but this won’t affect the monitoring events used by for example Flower as Redis pub/sub commands are global rather than database based.

## Munin

...

## Events

The worker has the ability to send a message whenever some event happens. These events are then captured by tools like Flower, and celery events to monitor the cluster.

### Snapshots

A sequence of events describes the cluster state in that time period, by taking periodic snapshots of this state you can keep all history, but still only periodically write it to disk.

celery events is then used to take snapshots with the camera, for example if you want to capture state every 2 seconds using the camera `myapp.Camera` you run celery events with the following arguments:

`$ celery -A proj events -c myapp.Camera --frequency=2.0`

#### Custom Camera

Cameras can be useful if you need to capture events and do something with those events at an interval. For real-time event processing you should use app.events.Receiver directly, like in Real-time processing.

```py
from pprint import pformat

from celery.events.snapshot import Polaroid

class DumpCam(Polaroid):
    clear_after = True  # clear after flush (incl, state.event_count).

    def on_shutter(self, state):
        if not state.event_count:
            # No new events since last snapshot.
            return
        print('Workers: {0}'.format(pformat(state.workers, indent=4)))
        print('Tasks: {0}'.format(pformat(state.tasks, indent=4)))
        print('Total: {0.event_count} events, {0.task_count} tasks'.format(
            state))
```

`$ celery -A proj events -c myapp.DumpCam --frequency=2.0`

### Real-time processing
...

## Event Reference

[origin link](https://docs.celeryproject.org/en/master/userguide/monitoring.html#event-reference)

## don't understand

- event reference

