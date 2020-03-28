# django 数据的基本、常用操作

## 增加修改数据

save():创建、更新数据
> Django doesn’t hit the database until you explicitly call save()

create():
> To create and save an object in a single step, use the create() method.

### Saving ForeignKey and ManyToManyField fields

save ForeignKey

```shell
>>>from blog.models import Blog, Entry
>>> entry = Entry.objects.get(pk=1)
>>> cheese_blog = Blog.objects.get(name="Cheddar Talk")
>>> entry.blog = cheese_blog
>>> entry.save()
```

save ManyToManyField use __add()__
> add支持同时保存多个对象

```shell
>>> from blog.models import Author
>>> joe = Author.objects.create(name="Joe")
>>> entry.authors.add(joe)
```

## 查找数据

查找数据的关键是 QuerySet && Manager

> a QuerySet equates to a __SELECT__ statement, and a __filter__ is a limiting clause such as __WHERE__ or __LIMIT__.

> You get a QuerySet by using your model’s Manager. Each model has at least one Manager, and it’s called __objects by default.__


### all(): 返回一张表所有的数据
>The all() method returns a QuerySet of all the objects in the database.


### 在QuerySet上检索数据

#### filter(**kwargs):

Returns a new QuerySet containing objects that match the given lookup parameters.

#### exclude(**kwargs):

Returns a new QuerySet containing objects that do not match the given lookup parameters.

filter&&exclude返回的是QuerySet对象，这意味着可以进行连续查询。

#### QuerySets are lazy

> in general, the results of a QuerySet aren’t fetched from the database until you “ask” for them. When you do, the QuerySet is evaluated by accessing the database

#### QuerySet支持切片

```shell
>>> Entry.objects.all()[:5]
```

### get(): 返回单一对象

如果搜索的数据不存在，get返回DoesNotExist异常

如果搜索的数据存在多条，get返回MultipleObjectsReturned异常

### field lookups(属性查询)

Basic lookups keyword arguments take the form __field__lookuptype=value__. (That’s a double-underscore). For example:

```shell
>>> Entry.objects.filter(pub_date__lte='2006-01-01')
```

translates (roughly) into the following SQL:

```sql
SELECT * FROM blog_entry WHERE pub_date <= '2006-01-01';
```

#### ForeignKey（外键上的查询有些不同）

需要在field后面添加'_id'，查询的值为模型的外键

#### 常用的属性查询条件

exact（精准查询）、iexact（不区分大小写查询）、contains（模糊查询）、startswith、endswith

#### 属性上的关联查询（类似与joins）

>To span a relationship, use the field name of related fields across models, separated by double underscores, until you get to the field you wantTo span a relationship, use the field name of related fields across models, separated by double underscores, until you get to the field you want。

关联查询的属性通过双下划线连接，直到找到想要的属性。

关联查询上filter的使用有些特别，exclued在关联查询上的使用方式与filter不同。详细解释见官方文档。[link](https://docs.djangoproject.com/en/3.0/topics/db/queries/#spanning-multi-valued-relationships)

#### F object: 同一模型上的字段比较查询 [link](https://docs.djangoproject.com/en/3.0/topics/db/queries/#filters-can-reference-fields-on-the-model)

#### pk的使用

pk在查询是等价与使用id、id__exact查询

pk还额外支持‘__in’和‘__gt’等方式查询

### Caching and QuerySets

使用QuerySets时，尽量多次重用。对于相同查询的不同属性获取，要将QuerySets保存在内存中，多次使用。如果重新查询可能会由于其他用户对数据的增删导致查询结果的不一致。

### 复杂查询使用Q对象

get、filter、exclude都支持Q对象查询

Q object支持与或查询

### QuerySet.delete():删除对象

delete()有返回值，返回一个元组包含删除对象的数量和种类

delete方法作用于QuerySet对象，不作用与Manager对象

### 复制对象

django不提供copy方法

简单的复制方法:将实例的主键设置为None再保存。

```python
blog = Blog(name='My blog', tagline='Blogging is easy')
blog.save() # blog.pk == 1

blog.pk = None
blog.save() # blog.pk == 2
```

对于继承的对象需要将实例的pk和id都置为None

对于oneToOneField需要将关联字段的pk也设置为None，赋值后再保存

这样的方法不会复制实例的关联字段，关联字段需要手动赋值

### QuerySet.update():一次更新多个对象

update可以接受普通字段和外键字段

update不会调用save()方法，需要手动调用

update支持使用有限的F object TODO:

### One-to-Many relationship

#### select_related ==> QuerySet

递归的缓存所有的所有的onetomany关系，之后的所有查询都会使用缓存。

[官方文档链接](https://docs.djangoproject.com/en/3.0/ref/models/querysets/#django.db.models.query.QuerySet.select_related)

#### oneToMany字段反向查询

oneToMany关系中，"1"的那一方存在一个Foo_set（其中Foo是"many"方类名的小写）字段。该字段是一个Manager，可以查询到所有关联到"1"的“many”对象。

默认的字段为Foo_set，不过可以通过ForeignKey声明时 __related_name__ 修改。

#### ForeignKey Manager上额外的方法

直接作用与Manager。add、create、remove、clear、set

### Many-to-Many relationship

多对多关系与一对多关系的使用方法一致

### One-to-One relationship

一对一关系中的反向查询的变量名为类名的小写形式，返回的是一个Manager，不过只存在一个对象。

### Queries over related objects

对于查询的方式，可以使用对象事例也可使用对象的id

```python
Entry.objects.filter(blog=b) # Query using object instance
Entry.objects.filter(blog=b.id) # Query using id from instance
Entry.objects.filter(blog=5) # Query using id directly
```






































