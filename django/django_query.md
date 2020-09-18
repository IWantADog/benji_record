# how to query in django

https://docs.djangoproject.com/en/3.1/topics/db/queries/#making-queries

https://docs.djangoproject.com/en/3.1/ref/models/conditional-expressions/

## F() expressions

An `F()` object represents the value of a model field or annotated column. It makes it possible to refer to model field values and perform database operations using them without actually having to pull them out of the database into Python memory.

F() can offer performance advantages by:

- getting the database, rather than Python, to do work
- reducing the number of queries some operations require

### * Avoiding race conditions using F()

Another useful benefit of `F()` is that having the database - rather than Python - __update a field’s value avoids a race condition__.

If two Python threads execute the code in the first example above, one thread could retrieve, increment, and save a field’s value after the other has retrieved it from the database. The value that the second thread saves will be based on the original value; the work of the first thread will be lost.

If the database is responsible for updating the field, the process is more robust: it will only ever update the field based on the value of the field in the database when the `save()` or `update()` is executed, rather than based on its value when the instance was retrieved.

### F() assignments persist after Model.save()

`F()` objects assigned to model fields persist after saving the model instance and will be applied on each `save()`. For example:

```py
reporter = Reporters.objects.get(name='Tintin')
reporter.stories_filed = F('stories_filed') + 1
reporter.save()

reporter.name = 'Tintin Jr.'
reporter.save()
```

`stories_filed` will be updated twice in this case. If it’s initially `1`, the final value will be `3`. This persistence can be avoided by reloading the model object after saving it, for example, by using `refresh_from_db()`.

### Using F() in filters

`F()` is also very useful in `QuerySet` filters, where they make it possible to filter a set of objects against criteria based on their field values, rather than on Python values.

### Using F() to sort null values

Use `F()` and the nulls_first or nulls_last keyword argument to `Expression.asc()` or `desc()` to control the ordering of a field’s null values. By default, the ordering depends on your database.

For example, to sort companies that haven’t been contacted (`last_contacted` is null) after companies that have been contacted:

```py
from django.db.models import F
Company.objects.order_by(F('last_contacted').desc(nulls_last=True))
```

### Using F() with annotations

__If the fields that you’re combining are of different types you’ll need to tell Django what kind of field will be returned__. Since `F()` does not directly support output_field you will need to wrap the expression with `ExpressionWrapper`:

```py
from django.db.models import DateTimeField, ExpressionWrapper, F

Ticket.objects.annotate(
    expires=ExpressionWrapper(
        F('active_at') + F('duration'), output_field=DateTimeField()))
```

## Func() expressions

__`Func()` expressions are the base type of all expressions that involve database functions like `COALESCE` and `LOWER`, or aggregates like `SUM`__.

```py
from django.db.models import F, Func

queryset.annotate(field_lower=Func(F('field'), function='LOWER'))

## or

queryset.annotate(field_lower=Lower('field'))
```

## Aggregate() expressions

An aggregate expression is a special case of a `Func() expression` that informs the query that a `GROUP BY` clause is required. All of the aggregate functions, like `Sum()` and `Count()`, `inherit from Aggregate()`.

## Conditional expressions

https://docs.djangoproject.com/en/3.1/ref/models/conditional-expressions/#conditional-aggregation

## Subquery

https://docs.djangoproject.com/en/3.1/ref/models/expressions/#subquery-expressions

较难理解。

### Referencing columns from the outer queryset

Use `OuterRef` when a queryset in a `Subquery` needs to refer to a field from the outer query. It acts like an F expression except that the check to see if it refers to a valid field isn’t made until the outer queryset is resolved.

## Raw SQL expressions

not recommend

## Window functions

[what is windosw farm](https://mjk.space/advances-sql-window-frames/)

intersting and powerful

https://docs.djangoproject.com/en/3.1/ref/models/expressions/#window-functions

## Complex lookups with Q objects

__Keyword argument queries – in filter(), etc. – are “AND”ed together__. If you need to execute more complex queries (for example, __queries with OR statements__), you can use `Q objects`.

`Q objects` can be negated using the `~` operator, allowing for combined lookups that combine both a normal query and a `negated (NOT) query`.

```py
Q(question__startswith='Who') | ~Q(pub_date__year=2005)
```

Each lookup function that takes keyword-arguments (e.g. filter(), exclude(), get()) can also be passed one or more Q objects as positional (not-named) arguments. __If you provide multiple Q object arguments to a lookup function, the arguments will be `“AND”`ed together__.

Lookup functions can mix the use of `Q objects` and `keyword arguments`. All arguments provided to a lookup function (be they keyword arguments or Q objects) are “AND”ed together. __However, if a Q object is provided, it must precede the definition of any keyword arguments__.
