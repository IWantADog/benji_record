# Calling Tasks

## Basics

The API defines a standard set of execution options, as well as three methods:

- apply_async(args[, kwargs[, …]])

  Sends a task message.

- delay(*args, **kwargs)

  Shortcut to send a task message, __but doesn’t support execution options.__

- calling (__call__)

  Applying an object supporting the calling API (e.g., add(2, 2)) means that the task will not be executed by a worker, but in the current process instead (a message won’t be sent).

### Example

```py
# how to use delay
task.delay(arg1, arg2, kwarg1='x', kwarg2='y')
```

```py
# how to use apply_async
task.apply_async(args=[arg1, arg2], kwargs={'kwarg1': 'x', 'kwarg2': 'y'})
```

## Linking (callbacks/errbacks)

`link` and `link_error` options.

## On message

Celery supports catching all states changes by setting `on_message` callback.

## ETA and Countdown

__The ETA (estimated time of arrival) lets you set a specific date and time that is the earliest time at which your task will be executed. countdown is a shortcut to set ETA by seconds into the future.__

 To make sure your tasks are executed in a timely manner you should monitor the queue for congestion. Use [Munin](https://docs.celeryproject.org/en/master/userguide/monitoring.html#monitoring-munin), or similar tools, to receive alerts, so appropriate action can be taken to ease the workload. See Munin.

## Expiration

The __expires__ argument defines an optional expiry time, either as __seconds__ after task publish, or a specific date and time using datetime:

## Message Sending Retry

### Retry Policy

- max_retries

  Maximum number of retries before giving up, in this case the exception that caused the retry to fail will be raised.

  __A value of None means it will retry forever.__

  __The default is to retry 3 times.__

- interval_start

  Defines the number of seconds (float or integer) to wait between retries. __Default is 0 (the first retry will be instantaneous).__

- interval_step

  On each consecutive retry this number will be added to the retry delay (float or integer). __Default is 0.2.__

- interval_max

  Maximum number of seconds (float or integer) to wait between retries. __Default is 0.2.__

```py
# example
add.apply_async((2, 2), retry=True, retry_policy={
    'max_retries': 3,
    'interval_start': 0,
    'interval_step': 0.2,
    'interval_max': 0.2,
})
```

## Connection Error Handling

If you have retries enabled this will only happen after retries are exhausted, or when disabled immediately.

## Compression

[origin link](https://docs.celeryproject.org/en/master/userguide/calling.html#compression)