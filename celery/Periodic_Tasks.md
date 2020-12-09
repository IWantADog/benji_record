# Periodic Tasks

## Time Zones

`timezone = 'Europe/London'`

The default scheduler (storing the schedule in the `celerybeat-schedule` file) will automatically detect that the time zone has changed, and so will reset the schedule itself, but other schedulers may not be so smart (e.g., the Django database scheduler, see below) and in that case you’ll have to reset the schedule manually.

## Entries

` on_after_configure` & `on_after_finalize` & `add_periodic_task()`

> Like with cron, the tasks may overlap if the first task doesn’t complete before the next. If that’s a concern you should use a locking strategy to ensure only one instance can run at a time (see for example [Ensuring a task is only executed one at a time](https://docs.celeryproject.org/en/master/tutorials/task-cookbook.html#cookbook-task-serials)).

## Crontab schedules

If you want more control over when the task is executed, for example, a particular time of day or day of the week, you can use the `crontab` schedule type:

```py
from celery.schedules import crontab

app.conf.beat_schedule = {
    # Executes every Monday morning at 7:30 a.m.
    'add-every-monday-morning': {
        'task': 'tasks.add',
        'schedule': crontab(hour=7, minute=30, day_of_week=1),
        'args': (16, 16),
    },
}
```

## Solar schedules

If you have a task that should be executed according to sunrise, sunset, dawn or dusk, you can use the solar schedule type:

```py
from celery.schedules import solar

app.conf.beat_schedule = {
    # Executes at sunset in Melbourne
    'add-at-melbourne-sunset': {
        'task': 'tasks.add',
        'schedule': solar('sunset', -37.81753, 144.96715),
        'args': (16, 16),
    },
}
```

## Starting the Scheduler

`$ celery -A proj beat`

You can also embed beat inside the worker by enabling the workers `-B` option, this is convenient if you’ll never run more than one worker node, __but it’s not commonly used and for that reason isn’t recommended for production use__:

`$ celery -A proj worker -B`

Beat needs to store the last run times of the tasks in a local database file (named `celerybeat-schedule` by default), so it needs access to write in the current directory, or alternatively you can specify a custom location for this file:

`$ celery -A proj beat -s /home/celery/var/run/celerybeat-schedule`

### Using custom scheduler classes

[origin link](https://docs.celeryproject.org/en/master/userguide/periodic-tasks.html#using-custom-scheduler-classes)
