# sqlalchemy common use

## Establishing Connectivity - the Engine

### create engine

```sh
>>> from sqlalchemy import create_engine
>>> engine = create_engine("sqlite+pysqlite:///:memory:", echo=True, future=True)
```

> `in-memory-only`数据库

## Working with Transactions and the DBAPI

### Getting a Connection

```sh
>>> from sqlalchemy import text

>>> with engine.connect() as conn:
...     result = conn.execute(text("select 'hello world'"))
...     print(result.all())
```

__The default behavior of the Python DBAPI includes that a `transaction` is always in progress; when the scope of the connection is released, a `ROLLBACK` is emitted to end the transaction. The transaction is not committed automatically; when we want to commit data we normally need to call `Connection.commit()` as we’ll see in the next section.__

> 使用python DBAPI默认使用事务处理数据库请求。除非显示使用`commit`，否则事务接受后会`rollback`


`Engin.begin()`。和`Engin.connect()`类似，不过`begin`结束后会自动`commit`

### Basics of Statement Execution

`Result object` 

### how to use session

```sh
>>> with Session(engine) as session:
...     result = session.execute(
...         text("UPDATE some_table SET y=:y WHERE x=:x"),
...         [{"x": 9, "y":11}, {"x": 13, "y": 15}]
...     )
...     session.commit()
```

> The Session doesn’t actually hold onto the `Connection` object after it ends the transaction. It gets a new `Connection` from the `Engine` when executing SQL against the database is next needed.

## Working with Database Metadata

### Metadata object

Having a single `MetaData` object for an entire application is the most common case, represented as a module-level variable in a single place in an application, often in a “models” or “dbschema” type of package. There can be multiple `MetaData` collections as well, however it’s typically most helpful if a series of `Table` objects that are related to each other belong to a single `MetaData` collection.

> `Metadata`似乎用来存储所有的`table`

### Declaring Simple Constraints

```py
# 如何定义外键
Column('user_id', ForeignKey('user_account.id'), nullable=False),
```
> __When using the `ForeignKey` object within a Column definition, we can omit the datatype for that Column;__ it is automatically inferred from that of the related column, in the above example the Integer datatype of the user_account.id column.

### Emitting DDL to the Database

```sh
>>> metadata.create_all(engine)
```
> 通过`metadata`创建所有的表。

[Alembic: base sqlalchemy database migration tool](https://alembic.sqlalchemy.org/en/latest/)

### Defining Table Metadata with the ORM

#### setting up Registry

`registry` & `MetaData` & `ORM Mapped Table`

> 如何理解`registry`。


```sh
>>> from sqlalchemy.orm import registry
>>> mapper_registry = registry()
>>> Base = mapper_registry.generate_base()
```

> 通过`registry`，获取`ORM Mapped Table`基类


- tip

    The steps of creating the registry and “declarative base” classes can be combined into one step using the historically familiar `declarative_base()` function:

    ```py
    from sqlalchemy.orm import declarative_base
    Base = declarative_base()
    ```

### Table Reflection

[Reflecting DataBase Objects](https://docs.sqlalchemy.org/en/14/core/reflection.html)

> 通过数据库中已经存在的表，创建`ORM Mapped Table`。

## Working with Data

### Inserting Rows with Core

skip

### Selecting Rows with Core or ORM

`Connection.execute() in Core` and `Session.execute() in ORM`


https://docs.sqlalchemy.org/en/14/tutorial/data_select.html




























