# how to aggregate in django

## Generating aggregates over a QuerySet

how to use aggregate.

```py
from django.db.models import Avg, Max, Min

Book.objects.aggregate(Avg('price'))

# specify the key
Book.objects.aggregate(avg=Avg('price'))

# generate more than one aggregate
Book.objects.aggregate(Avg('price'), Max('price'), Min('price'))
```

## Generating aggregates for each item in a QuerySet

```py
Book.objects.annotate(Count('authors'))

# specify the key
Book.objects.annotate(count=Count('authors'))
```

Unlike `aggregate()`, `annotate()` is not a __terminal clause__. The output of the `annotate()`clause is a `QuerySet`; this `QuerySet` can be modified using any other `QuerySet` operation, including `filter()`, `order_by()`, or even additional calls to `annotate()`.

### Combining multiple aggregations

Combining multiple aggregations with `annotate()` will yield the wrong results __because joins are used instead of subqueries__.

For most aggregates, there is no way to avoid this problem, however, __the Count aggregate has a distinct parameter that may help__:

```sh
>>> q = Book.objects.annotate(Count('authors', distinct=True), Count('store', distinct=True))
```

## Joins and aggregates

[dobule underscore notation](https://docs.djangoproject.com/en/3.1/topics/db/queries/#field-lookups-intro)

When specifying the field to be aggregated in an aggregate function, Django will allow you to use the same double underscore notation that is used when referring to related fields in filters. __Django will then handle any table joins that are required to retrieve and aggregate the related value__.

__Join chains can be as deep as you require__. For example, to extract the age of the youngest author of any book available for sale, you could issue the query:

## Aggregations and other QuerySet clauses

### Filtering on annotations

__Annotated values can also be filtered__. The alias for the annotation can be used in `filter()` and `exclude()` clauses in the same way as any other model field.

__If you need two annotations with two separate filters you can use the filter argument with any aggregate__. For example, to generate a list of authors with a count of highly rated books:

```sh
>>> highly_rated = Count('book', filter=Q(book__rating__gte=7))
>>> Author.objects.annotate(num_books=Count('book'), highly_rated_books=highly_rated)
```

#### Choosing between filter and QuerySet.filter()

> Avoid using the filter argument with a single annotation or aggregation. It’s more efficient to use QuerySet.filter() to exclude rows. __The aggregation filter argument is only useful when using two or more aggregations over the same relations with different conditionals__.

### Order of annotate() and filter() clauses

__When an `annotate()` clause is applied to a query, the annotation is computed over the state of the query up to the point where the annotation is requested. The practical implication of this is that `filter()` and `annotate()` are not commutative operations__.

__Inspect the SQL with `str(queryset.query)` and write plenty of tests.__

### values()

Ordinarily, annotations are generated on a per-object basis - an annotated QuerySet will return one result for each object in the original QuerySet. However, when a values() clause is used to constrain the columns that are returned in the result set, the method for evaluating annotations is slightly different. __Instead of returning an annotated result for each result in the original QuerySet, the original results `are grouped` according to the unique combinations of the fields specified in the `values()` clause__. __An annotation is then provided for each unique group; the annotation is computed over all members of the group__.

#### Order of annotate() and values() clauses

If the `values()` clause precedes the `annotate()` clause, any annotations will be automatically added to the result set. However, if the `values()` clause is applied after the `annotate()` clause, you need to explicitly include the aggregate column.

#### Interaction with default ordering or order_by()

[example](https://docs.djangoproject.com/en/3.1/topics/db/aggregation/#interaction-with-default-ordering-or-order-by)

notice the default order and can remove order constrain by `order_by()`

## Aggregating annotations

__You can also generate an aggregate on the result of an annotation__. When you define an `aggregate() clause`, the aggregates you provide can reference any alias defined as part of an `annotate() clause` in the query.
