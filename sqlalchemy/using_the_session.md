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