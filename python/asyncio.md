# python asyncio

## Awaitable

We say that an object is an awaitable object if it can be used in an await expression. Many asyncio APIs are designed to accept awaitables.

There are three main types of awaitable objects: coroutines, Tasks, and Futures.

### Coroutines

- a coroutine function: an async def function;
- a coroutine object: an object returned by calling a coroutine function.

### Task

Tasks are used to schedule coroutines concurrently.

When a coroutine is wrapped into a Task with functions like asyncio.create_task() the coroutine is automatically scheduled to run soon.

### Futures

A Future is a special low-level awaitable object that represents an eventual result of an asynchronous operation.

When a Future object is awaited it means that the coroutine will wait until the Future is resolved in some other place.

Future objects in asyncio are needed to allow callback-based code to be used with async/await.

Normally there is no need to create Future objects at the application level code.

## Running a asyncio program

https://docs.python.org/3/library/asyncio.html

## How asyncio work

https://stackoverflow.com/questions/49005651/how-does-asyncio-actually-work
