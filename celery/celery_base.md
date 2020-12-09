# celery base

## project

```
proj/__init__.py
    /celery.py
    /tasks.py
```

```py
# proj/celery.py
from celery import Celery

app = Celery('proj',
             broker='amqp://',
             backend='rpc://',
             include=['proj.tasks'])

# Optional configuration, see the application user guide.
app.conf.update(
    result_expires=3600,
)

if __name__ == '__main__':
    app.start()
```

```py
# proj/task.py
from .celery import app

@app.task
def add(x, y):
    return x + y


@app.task
def mul(x, y):
    return x * y


@app.task
def xsum(numbers):
    return sum(numbers)
```

## start work

`$ celery -A proj worker -l INFO`

## calling tasks

These three methods - `delay()`, `apply_async()`, and applying `(__call__)`, make up the Celery calling API, which is also used for signatures.

If you have a result backend configured you can retrieve the return value of a task:

```py
>>> res = add.delay(2, 2)
>>> res.get(timeout=1)
4
>>> res.id
>>> res.failed()
True

>>> res.successful()
False
```

```py
# So how does it know if the task has failed or not? It can find out by looking at the tasks state:
>>> res.state
'FAILURE'
```

A task can only be in a single state, but it can progress through several states. The stages of a typical task can be:

`PENDING -> STARTED -> SUCCESS`

The pending state is actually not a recorded state, but rather the default state for any task id that’s unknown: this you can see from this example:

```py
>>> from proj.celery import app

>>> res = app.AsyncResult('this-id-does-not-exist')
>>> res.state
'PENDING'
```

## Canvas: Designing Work-flows

`signature`

Signature instances also support the calling API, meaning they have delay and apply_async methods.

But there’s a difference in that the signature may already have an argument signature specified. `

### The Primitives

`Groups`: A group calls a list of tasks in parallel, and it returns a special result instance that lets you inspect the results as a group, and retrieve the return values in order.

`Chains`: Tasks can be linked together so that after one task returns the other is called:

## Remote Control

[Monitoring and Management guide](https://docs.celeryproject.org/en/master/userguide/monitoring.html#guide-monitoring)
s
## refrences

[Monitoring and Management guide](https://docs.celeryproject.org/en/master/userguide/monitoring.html#guide-monitoring)

[Routing Tasks](https://docs.celeryproject.org/en/master/userguide/routing.html#guide-routing)

[Workers Guide](https://docs.celeryproject.org/en/master/userguide/workers.html#guide-workers)

[daemonization tutorial](https://docs.celeryproject.org/en/master/userguide/daemonizing.html#daemonizings)

[Calling Tasks](https://docs.celeryproject.org/en/master/userguide/calling.html#guide-calling)

[canavs](https://docs.celeryproject.org/en/master/userguide/canvas.html#guide-canvas)

[optimizing](https://docs.celeryproject.org/en/master/userguide/optimizing.html#guide-optimizing)