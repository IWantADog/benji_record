# Relationship Configuration

## Basic Relationship Patterns

### One To Many

```py
# using back_populated
class Parent(Base):
    __tablename__ = 'parent'
    id = Column(Integer, primary_key=True)
    children = relationship("Child", back_populates="parent")

class Child(Base):
    __tablename__ = 'child'
    id = Column(Integer, primary_key=True)
    parent_id = Column(Integer, ForeignKey('parent.id'))
    parent = relationship("Parent", back_populates="children")
```

```py
# using backref
class Parent(Base):
    __tablename__ = 'parent'
    id = Column(Integer, primary_key=True)
    children = relationship("Child", backref="parent")

class Child(Base):
    __tablename__ = 'child'
    id = Column(Integer, primary_key=True)
    parent_id = Column(Integer, ForeignKey('parent.id'))
```
 
### Many To One

same to `One TO Many`

### One To One

```py
class Parent(Base):
    __tablename__ = 'parent'
    id = Column(Integer, primary_key=True)
    child = relationship("Child", uselist=False, back_populates="parent")

class Child(Base):
    __tablename__ = 'child'
    id = Column(Integer, primary_key=True)
    parent_id = Column(Integer, ForeignKey('parent.id'))
    parent = relationship("Parent", back_populates="child")
```

or 

```py
from sqlalchemy.orm import backref

class Parent(Base):
    __tablename__ = 'parent'
    id = Column(Integer, primary_key=True)
    child_id = Column(Integer, ForeignKey('child.id'))
    child = relationship("Child", backref=backref("parent", uselist=False))

class Child(Base):
    __tablename__ = 'child'
    id = Column(Integer, primary_key=True)
    parent_id = Column(Integer, ForeignKey('parent.id'))
```

### Many To Many

```py
association_table = Table('association', Base.metadata,
    Column('left_id', Integer, ForeignKey('left.id')),
    Column('right_id', Integer, ForeignKey('right.id'))
)

class Parent(Base):
    __tablename__ = 'left'
    id = Column(Integer, primary_key=True)
    children = relationship("Child",
                    secondary=association_table,
                    backref="parents")

class Child(Base):
    __tablename__ = 'right'
    id = Column(Integer, primary_key=True)
```

#### Deleting Rows from the Many to Many Table

A question which often arises is how the row in the “secondary” table can be deleted when the child object is handed directly to `Session.delete()`:

There are several possibilities here:

- If there is a `relationship()` from `Parent` to `Child`, but there is not a reverse-relationship that links a particular `Child` to each `Parent`, SQLAlchemy will not have any awareness that when deleting this particular Child object, it needs to maintain the “secondary” table that links it to the Parent. No delete of the “secondary” table will occur.

- If there is a relationship that links a particular `Child` to each `Parent`, suppose it’s called `Child.parents`, SQLAlchemy by default will load in the `Child.parents` collection to locate all `Parent` objects, and remove each row from the “secondary” table which establishes this link. Note that this relationship does not need to be bidirectional; SQLAlchemy is strictly looking at every `relationship()` associated with the `Child` object being deleted.

- A higher performing option here is to use `ON DELETE CASCADE` directives with the foreign keys used by the database. Assuming the database supports this feature, the database itself can be made to automatically delete rows in the “secondary” table as referencing rows in `“child”` are deleted. `SQLAlchemy` can be instructed to forego actively loading in the `Child.parents` collection in this case using the relationship.passive_deletes directive on `relationship()`; see Using foreign key `ON DELETE` cascade with `ORM` relationships for more details on this.

> 对于`many to many`删除数据时，可能出现的逻辑。

### Association Object

The association object pattern is a variant on many-to-many: __it’s used when your association table contains additional columns beyond those which are foreign keys to the left and right tables.__ Instead of using the `relationship.secondary` argument, you map a new class directly to the association table. __The left side of the relationship references the association object via one-to-many, and the association class references the right side via many-to-one.__

```py
class Association(Base):
    __tablename__ = 'association'
    left_id = Column(Integer, ForeignKey('left.id'), primary_key=True)
    right_id = Column(Integer, ForeignKey('right.id'), primary_key=True)
    extra_data = Column(String(50))
    child = relationship("Child", back_populates="parents")
    parent = relationship("Parent", back_populates="children")

class Parent(Base):
    __tablename__ = 'left'
    id = Column(Integer, primary_key=True)
    children = relationship("Association", back_populates="parent")

class Child(Base):
    __tablename__ = 'right'
    id = Column(Integer, primary_key=True)
    parents = relationship("Association", back_populates="child")
```

## Late-Evaluation of Relationship Arguments

Many of the examples in the preceding sections illustrate mappings where the various `relationship()` constructs refer to __their target classes using a string name, rather than the class itself。__

__These string names are resolved into classes in the mapper resolution stage, which is an internal process that occurs typically after all mappings have been defined and is normally triggered by the first usage of the mappings themselves. The registry object is the container in which these names are stored and resolved to the mapped classes they refer towards.__

In addition to the main class argument for `relationship()`, other arguments which __depend upon the columns present on an as-yet undefined class may also be specified either as Python functions, or more commonly as strings.__ For most of these arguments except that of the main argument, string inputs are evaluated as Python expressions using Python’s built-in eval() function, as they are intended to recieve complete SQL expressions.

> `relationship()` 中的部分参数，可以设置为 `python function` or `string` or `sql语句`

## Late-Evaluation for a many-to-many relationship

`Many-to-many` relationships include a reference to an additional, typically non-mapped Table object that is typically present in the `MetaData` collection referred towards by the `registry`. __The late-evaluation system also includes support for having this attribute be specified as a string argument which will be resolved from this MetaData collection.__

> `many to many` 关系中，`Relationship.secondary` 可以定义为 `string`。
