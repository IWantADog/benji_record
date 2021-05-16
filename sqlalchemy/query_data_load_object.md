# Query data, Loading object

## ORM Querying Guide

### select statements

```py
>>> from sqlalchemy import select
>>> stmt = select(User).where(User.name == 'spongebob')
```

#### Selecting ORM Entities and Attributes

The `select()` construct accepts `ORM` entities, including mapped classes as well as `class-level attributes` representing mapped columns, which are converted into ORM-annotated `FromClause` and `ColumnElement` elements at construction time.

When selecting from `ORM` entities, the entity itself is returned in the `result` as a `row` with a single element, as opposed to a series of individual columns; for example above, the `Result` returns `Row` objects that have just a single element per row, that element holding onto a User object。

> `select()` 通过传入 `Base.Column`, 指定模型属性的部分查找。 

__ORM Entities are named in the result row based on their class name__。

> `Result` & `Row` object。正确理解 `Resutl` 和 `Row`。

When selecting a list of single-element rows containing `ORM` entities, it is typical to skip the generation of Row objects and instead receive `ORM` entities directly, which is achieved using the `Result.scalars()` method:

> `Result.scalars()` 跳过将数据封装为 `ROW` ，直接返回 `ORM` 实例。

#### Grouping Selected Attributes with Bundles

```py
>>> from sqlalchemy.orm import Bundle
>>> stmt = select(
...     Bundle("user", User.name, User.fullname),
...     Bundle("email", Address.email_address)
... ).join_from(User, Address)
SQL>>> for row in session.execute(stmt):
...     print(f"{row.user.name} {row.email.email_address}")

# output
spongebob spongebob@sqlalchemy.org
sandy sandy@sqlalchemy.org
sandy squirrel@squirrelpower.org
patrick pat999@aol.com
squidward stentcl@sqlalchemy.org
```

#### Selecting ORM Aliases

```py
>>> from sqlalchemy.orm import aliased
>>> u1 = aliased(User)
>>> print(select(u1).order_by(u1.id))
```
> 模型设置别名

### Joins

`Select.join()` & `Select.join_from()`

#### Simple Relationship Joins

```py
>>> stmt = select(User).join(User.addresses)
```

#### Chaining Multiple Joins

> `join()` 支持传入的是 `ORM` 中定义的 `relationship`。

#### Joins to a Target Entity or Selectable

> `join()` 支持传入 `ORM`。这种情况下，`sqlalchemy` 自动使用外键连接两张表。

#### Joins to a Target with an ON Clause

> `join()` 支持显示设置 `on`。传入的参数可以显示设置表达式，或者传入 `relationship`。

```py
>>> stmt = select(User).join(Address, User.id==Address.user_id)
>>> print(stmt)

SELECT user_account.id, user_account.name, user_account.fullname
FROM user_account JOIN address ON user_account.id = address.user_id

# 等价
>>> stmt = select(User).join(Address, User.addresses)
```

#### Augmenting Built-in ON Clauses

The `Select.join_from()` method accepts `two` or `three` arguments, either in the form `<join from>, <onclause>,` or `<join from>, <join to>, [<onclause>]`。

> `join`：被 `select`的表作为 `from` 的主表，传入 `jion` 表，作为连接表

> `join_from`：被 `select` 的表仅作为查找的属性。`join_from` 中传入的第一参数作为主表，或许的其他参数作为连接表。

## Loading Columns

### Deferred Column Loading

Deferred column loading allows particular columns of a table be loaded only upon direct access, instead of when the entity is queried using `Query`. __This feature is useful when one wants to avoid loading a large text or binary field into memory when it’s not needed.__ Individual columns can be lazy loaded by themselves or placed into groups that lazy-load together, using the `deferred()` function to mark them as “deferred”.

> 延迟部分属性的加载。对于较大的文本或是二进制文件，为了避免每次查询时都将其加入内存，可以在定义模型时，将其设置为延迟加载。

```py
from sqlalchemy.orm import deferred
from sqlalchemy import Integer, String, Text, Binary, Column

class Book(Base):
    __tablename__ = 'book'

    book_id = Column(Integer, primary_key=True)
    title = Column(String(200), nullable=False)
    summary = Column(String(2000))
    excerpt = deferred(Column(Text))
    photo = deferred(Column(Binary))
```

`Deferred columns` can be associated with a `“group”` name, so that they load together when any of them are first accessed. 

### Deferred Column Loader Query Options

Columns can be marked as `“deferred”` or reset to `“undeferred”` at query time using options which are passed to the `Query.options()` method; the most basic query options are `defer()` and `undefer()`.

> 属性可在被查询的时候，设置是否延迟加载。

## Relationship Loading Techniques

This behavior can be configured at mapper construction time using the `relationship.lazy` parameter to the `relationship()` function, as well as by using `options` with the `Query object`.

> `Relationship` 的加载策略。可以通过 `Relationship.lazy` 显示地设置，也可在查询时通过 `Query.options` 设置。

The loading of relationships falls into three categories; `lazy loading`, `eager loading`, and `no loading`.

> `lazy loading`: 当对象首次被使用时，`select` 语句才执行。

> `eager loading`: 查询后直接返回所有数据。

> `no loading`: 相关的属性被设置为`empty`，并且从不被加载；或者当属性被访问时，直接返回异常。

The primary forms of relationship loading are:

- `lazy loading` - available via `lazy='select'` or the `lazyload()` option。
- `joined loading` - available via `lazy='joined'` or the `joinedload()` option。
- `subquery loading` - available via `lazy='subquery'` or the `subqueryload()` option。
- `select IN loading` - available via `lazy='selectin'` or the `selectinload()` option。
- `raise loading` - available via `lazy='raise'`, `lazy='raise_on_sql'`, or the `raiseload()` option。
- `no loading` - available via `lazy='noload'`, or the `noload()` option。

> The default value of the `relationship.lazy` argument is `"select"`, which indicates lazy loading。

### Relationship Loading with Loader Options

The other, and possibly more common way to configure loading strategies is to set them up on a per-query basis against specific attributes using the `Query.options()` method.

> 通过 `Query.options()` 设置加载策略。

```py
# set children to load lazily
session.query(Parent).options(lazyload(Parent.children)).all()

# set children to load eagerly with a join
session.query(Parent).options(joinedload(Parent.children)).all()
```

```py
session.query(Parent).options(
    joinedload(Parent.children).
    subqueryload(Child.subelements)).all()
```

#### Specifying Sub-Options with Load.options()

Using method chaining, the loader style of each link in the path is explicitly stated. To navigate along a path without changing the existing loader style of a particular attribute, the `defaultload()` method/function may be used.

> 设置链式加载策略。

### [Detail about all loading techniques](https://docs.sqlalchemy.org/en/14/orm/loading_relationships.html#lazy-loading)


### What Kind of Loading to Use ?

[detail](https://docs.sqlalchemy.org/en/14/orm/loading_relationships.html#what-kind-of-loading-to-use)

### Wildcard Loading Strategies

Each of `joinedload()`, `subqueryload()`, `lazyload()`, `selectinload()`, `noload()`, and `raiseload()` can be used to set the default style of `relationship()` loading for a particular query, affecting all `relationship()` -mapped attributes not otherwise specified in the `Query`. This feature is available by passing the string '*' as the argument to any of these options:

```py
session.query(MyClass).options(lazyload('*'))
```

> 对于查询的所有相关的加载，设置相同的加载策略。
