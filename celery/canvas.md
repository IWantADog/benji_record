# Canvans: Designing Work-flows

## Signatures

```py
# how to use

>>> from celery import signature
>>> signature('tasks.add', args=(2, 2), countdown=10)
tasks.add(2, 2)

>>> add.signature((2, 2), countdown=10)
tasks.add(2, 2)

>>> add.s(2, 2)
tasks.add(2, 2)
```

It supports the “Calling API” of delay, apply_async, etc., including being called directly (__call__).

You can’t define options with s(), but a chaining set call takes care of that:

```py
>>> add.s(2, 2).set(countdown=1)
proj.tasks.add(2, 2)
```

### Immutability

Partials are meant to be used with callbacks, any tasks linked, or chord callbacks will be applied with the result of the parent task. Sometimes you want to specify a callback that doesn’t take additional arguments, and in that case you can set the signature to be immutable:

```py
>>> add.apply_async((2, 2), link=reset_buffers.signature(immutable=True))
The .si() shortcut can also be used to create immutable signatures:

>>> add.apply_async((2, 2), link=reset_buffers.si())
```

### Callbacks

Callbacks can be added to any task using the `link` argument to `apply_async`:

`add.apply_async((2, 2), link=other_task.s())`

## The Primitives

- group

  The group primitive is a signature that takes a list of tasks that should be applied __in parallel__.

- chain

  The chain primitive lets us link together signatures so that __one is called after the other__, essentially forming a chain of callbacks.

- chord

  A chord is just like a group but with a callback. __A chord consists of a header group and a body, where the body is a task that should execute after all of the tasks in the header are complete.__

- map

  __The map primitive works like the built-in map function, but creates a temporary task where a list of arguments is applied to the task__. For example, `task.map([1, 2])` – results in a single task being called, applying the arguments in order to the task function so that the result is: `res = [task(1), task(2)]`

- starmap

  __Works exactly like map except the arguments are applied as *args.__ For example add.starmap([(2, 2), (4, 4)]) results in a single task calling:

  `res = [add(2, 2), add(4, 4)]`

- chunks

  Chunking splits a long list of arguments into parts, for example the operation:
  
  ```py
  >>> items = zip(range(1000), range(1000))  # 1000 items
  >>> add.chunks(items, 10)
  ```

  will split the list of items into chunks of 10, resulting in 100 tasks (each processing 10 items in sequence).

### Examples

```py
>>> (add.s(2, 2) | add.s(4) | add.s(8))().get()
```

[some useful examples](https://docs.celeryproject.org/en/master/userguide/canvas.html#the-primitives)

### Chains

Tasks can be linked together: __the linked task is called when the task returns successfully__.

The linked task will be applied with the result of its parent task as the __first argument__.

`chirden` & `parent` & `collect`

### Groups

A group can be used to execute several tasks in parallel.

The group function takes a list of signatures.

If you __call__ the group, the tasks will be applied __one after another in the current process__, and a `GroupResult` instance is returned that can be used to keep track of the results, or tell how many tasks are ready and so on.

#### Group Results

The GroupResult takes a list of AsyncResult instances and operates on them as if it was a single task.

- successful()

  Return True if all of the subtasks finished successfully (e.g., didn’t raise an exception).

- failed()

  Return True if any of the subtasks failed.

- waiting()

  Return True if any of the subtasks isn’t ready yet.

- ready()

  Return True if all of the subtasks are ready.

- completed_count()

  Return the number of completed subtasks.

- revoke()

  Revoke all of the subtasks.

- join()

  Gather the results of all subtasks and return them in the same order as they were called (as a list).

### Chrods

A chord is a task that only executes after all of the tasks in a group have finished executing.

the callback can only be executed after all of the tasks in the header have returned. Each step in the header is executed as a task, in parallel, possibly on different nodes. The callback is then applied with the return value of each task in the header. The task id returned by chord() is the id of the callback, so you can wait for it to complete and get the final return value (but remember to never have a task wait for other tasks)

#### Error handling

The chord callback result will transition to the failure state, and the error is set to the ChordError exception.

__Note that the rest of the tasks will still execute,__ so the third task `(add.s(8, 8))` is still executed even though the middle task failed. Also the ChordError only shows the task that failed first (in time): it doesn’t respect the ordering of the header group.

To perform an action when a chord fails you can therefore attach an errback to the chord callback:

```py
@app.task
def on_chord_error(request, exc, traceback):
    print('Task {0!r} raised error: {1!r}'.format(request.id, exc))
>>> c = (group(add.s(i, i) for i in range(10)) |
...      xsum.s().on_error(on_chord_error.s())).delay()
```

### Important Notes

__Tasks used within a chord must not ignore their results. In practice this means that you must enable a result_backend in order to use chords.__ Additionally, if `task_ignore_result` is set to `True` in your configuration, be sure that the individual tasks to be used within the chord are defined with `ignore_result=False`. __This applies to both Task subclasses and decorated tasks.__

## Map & Starmap

map and starmap are built-in tasks that call the provided calling task for every element in a sequence.

They differ from group in that:

- only one task message is sent.
- the operation is sequential.






