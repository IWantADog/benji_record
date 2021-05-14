# Using session

## What does the session do

The Session begins in a mostly stateless form. __Once queries are issued or other objects are persisted with it, it requests a connection resource from an Engine that is associated with the Session, and then establishes a transaction on that connection.__ This transaction remains in effect until the Session is instructed to commit or roll back the transaction.

## Basic using of sesison

### opening and closing session

```py
from sqlalchemy import create_engine
from sqlalchemy.orm import Session

# an Engine, which the Session will use for connection
# resources
engine = create_engine('postgresql://scott:tiger@localhost/')

# create session and add objects
with Session(engine) as session:
    session.add(some_object)
    session.add(some_other_object)
    session.commit()
```

### Expiring / Refreshing

When an ORM mapped object is loaded into memory, there are three general ways to refresh its contents with new data from the current transaction:

- `expire()`

    ```py
    session.expire(u1)
    u1.some_attribute  # <-- lazy loads from the transaction
    ```

- `refresh()`

    ```py
    session.refresh(u1)  # <-- emits a SQL query
    u1.some_attribute  # <-- is refreshed from the transaction
    ```

- `populate_existing()`

    ```py
    u2 = session.query(User).populate_existing().filter(id=5).first()
    ```

### UPDATE and DELETE with arbitrary WHERE clause

#### update

- 1.x style

    ```py
    session.query(User).filter(User.name == "squidward").update({"name": "spongebob"}, synchronize_session="fetch")
    ```

- 2.x style

    ```py
    from sqlalchemy import update

    stmt = update(User).where(User.name == "squidward").values(name="spongebob").execution_options(synchronize_session="fetch")

    result = session.execute(stmt)
    ```

#### delete

- 1.x style

    ```py
    session.query(User).filter(User.name == "squidward").delete(synchronize_session="fetch")
    ```

- 2.x style

    ```py
    from sqlalchemy import delete

    stmt = delete(User).where(User.name == "squidward").execution_options(synchronize_session="fetch")

    session.execute(stmt)
    ```

> The `Query.update.synchronize_session` parameter referring to `“fetch”` indicates the list of affected primary keys should be fetched either via a separate SELECT statement or via RETURNING if the backend database supports it; objects locally present in memory will be updated in memory based on these primary key identities.


> 执行 `update or  delete` 时通过 `Query.update.synchronize_session` 更新 `session` 中的数据。

#### Selecting a Synchronization Strategy

- `synchronize_session`
    - `False`
    - `fetch`
    - `evalute`

### good principles

[reference](https://docs.sqlalchemy.org/en/14/orm/session_basics.html#session-frequently-asked-questions)

1. `sessionmaker` 放在 `module level`。调用时仅使用 `Session()` 。

2. As a general rule, keep the lifecycle of the session `separate` and `external` from functions and objects that access and/or manipulate database data. This will greatly help with achieving a predictable and consistent transactional scope.
    > 方法和对象不应该保存 `session`，避免使用混乱。

3. Make sure you have a clear notion of where transactions `begin` and `end`, and `keep transactions short`, meaning, they end at the series of a sequence of operations, instead of being held open indefinitely.
    > 事务的使用应该清晰、简短。

4. Web applications. In this case, it’s best to make use of the SQLAlchemy integrations provided by the web framework in use. __Or otherwise, the basic pattern is create a Session at the start of a web request, call the Session.commit() method at the end of web requests that do POST, PUT, or DELETE, and then close the session at the end of web request.__ It’s also usually a good idea to set `Session.expire_on_commit` to `False` so that subsequent access to objects that came from a Session within the view layer do not need to emit new SQL queries to refresh the objects, if the transaction has been committed already.
    > 对于`web application`，好的原则是在请求开始时创建 `session`，在请求结束时`commit`。

5. A background daemon which spawns off child forks would want to create a Session local to each child process, work with that `Session` through the life of the `“job”` that the fork is handling, then tear it down when the job is completed.

6. For a command-line script, the application would create a single, `global` `Session` that is established when the program begins to do its work, and commits it right as the program is completing its task.

7. __For a GUI interface-driven application, the scope of the Session may best be within the scope of a user-generated event__, such as a button push. Or, the scope may correspond to explicit user interaction, such as the user “opening” a series of records, then “saving” them.

8. It’s somewhat used as a cache, in that it implements the `identity map pattern`, and stores objects keyed to their primary key.
    > 对于通过主键获取单行，sqlalchemy有 `cache`。对于所有的 `query`，没有 `cache`。

9. Additionally, the Session stores object instances using a weak reference by default. This also defeats the purpose of using the Session as a cache.
    > `session` 内部默认通过 `weak reference` 存储数据。`Session` 不可作为缓存。

10. The Session is very much intended to be used in a `non-concurrent` fashion, __which usually means in only one thread at a time__.
    > `Session` 使用时不推荐在 `thread` 间共享。

11. A more common approach to this situation is to maintain a single Session per concurrent thread, but to instead copy objects from one Session to another, often using the `Session.merge()` method to copy the state of an object into a new object local to a different Session.
    > 对于多线程处理相同的任务，官方推荐为每个线程分配一个 `session`。通过 `Session.merge()` 复制不同线程之间的数据。

## State Management

- `Transient` - an instance that’s not in a session, and is not saved to the database; i.e. it has no database identity. The only relationship such an object has to the ORM is that its class has a Mapper associated with it.

- `Pending` - when you `Session.add()` a transient instance, it becomes pending. It still wasn’t actually flushed to the database yet, but it will be when the next flush occurs.

- `Persistent` - An instance which is present in the session and has a record in the database. You get persistent instances by either flushing so that the pending instances become persistent, or by querying the database for existing instances (or moving persistent instances from other sessions into your local session).

- `Deleted` - An instance which has been deleted within a `flush`, but the transaction has not yet completed. Objects in this state are essentially in the opposite of “pending” state; when the session’s transaction is committed, the object will move to the detached state. Alternatively, when the session’s transaction is rolled back, a deleted object moves back to the persistent state.

- `Detached` - an instance which corresponds, or previously corresponded, to a record in the database, but is not currently in any session. The detached object will contain a database identity marker, however because it is not associated with a session, it is unknown whether or not this database identity actually exists in a target database. Detached objects are safe to use normally, except that they have no ability to load unloaded attributes or attributes that were previously marked as “expired”.

### Getting the Current State of an Object

The actual state of any mapped object can be viewed at any time using the `inspect()` system:

```py
>>> from sqlalchemy import inspect
>>> insp = inspect(my_object)
>>> insp.persistent
True
```

### Session Attributes

1. `session` 类似一个 `set-like` 容器，可以迭代。
2. 可以对 `session` 使用 `in`， 检查对象是否在 `session` 中。
3. `session.new` & `session.dirty` & `session.deleted` & `session.identity_map`

### Session Referencing Behavior

__Objects within the session are weakly referenced. This means that when they are dereferenced in the outside application, they fall out of scope from within the Session as well and are subject to garbage collection by the Python interpreter.__ The exceptions to this include objects which are pending, objects which are marked as deleted, or persistent objects which have pending changes on them. After a full flush, these collections are all empty, and all objects are again weakly referenced.

> `session` 中的所有对象都是 `weakly referenced`。

### Merging * 

[detail](https://docs.sqlalchemy.org/en/14/orm/session_state_management.html#merging)

> 将 `session` 外部的对象与 `session`中的对象合并，并更新状态。


### Expunging

__Expunge removes an object from the Session, sending persistent instances to the detached state, and pending instances to the transient state:__

```py
session.expunge(obj1)
```

> 待测试

### Refreshing / Expiring

`Expiring` means that the database-persisted data held inside a series of object attributes is erased, __in such a way that when those attributes are next accessed, a SQL query is emitted which will refresh that data from the database.__

`session.expire(user)` & `session.expire_all()` & `session.refresh(obj1)`


### What Actually Loads

[detail](https://docs.sqlalchemy.org/en/14/orm/session_state_management.html#what-actually-loads)

### When to Expire or Refresh

[detail](https://docs.sqlalchemy.org/en/14/orm/session_state_management.html#when-to-expire-or-refresh)

### reference

https://docs.sqlalchemy.org/en/14/orm/session_state_management.html#expunging
