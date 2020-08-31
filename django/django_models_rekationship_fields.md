# django models

## Relationship fields

### ForeignKey

A `many-to-one` relationship. Requires two positional arguments: the class to which the `model` is related and the `on_delete` option.

To create a `recursive relationship` – an object that has a many-to-one relationship with itself – use `models.ForeignKey('self', on_delete=models.CASCADE)`.

If you need to create a relationship on a `model that has not yet been defined`, you can use the `name of the model`, rather than the model object itself.

To refer to `models defined in another application`, you can explicitly specify a `model with the full application label`.

__A database index is automatically created on the `ForeignKey`__. You can disable this by setting `db_index` to `False`. You may want to avoid the overhead of an index if you are creating a foreign key for consistency rather than joins, or if you will be creating an alternative index like a partial or multiple column index.

`ForeignKey.limit_choices_to`:

__Sets a limit to the available choices for this field when this field is rendered using a ModelForm or the admin (by default, all objects in the queryset are available to choose)__. Either a dictionary, a Q object, or a callable returning a dictionary or Q object can be used.

`ForeignKey.related_name`:

__The name to use for the relation from the related object back to this one__. It’s also the default value for related_query_name (the name to use for the reverse filter name from the target model).

`ForeignKey.related_query_name`:

__The name to use for the reverse filter name from the target model__. It defaults to the value of related_name or default_related_name if set, otherwise it __defaults to the name of the model__.

`ForeignKey.to_field`
__The field on the related object that the relation is to__. __By default, Django uses the `primary key` of the related object.__ If you reference a different field, that field must have unique=True.

`ForeignKey.db_constraint`

can't understand

`ForeignKey.swappable`

can't understand

### ManyToManyField

`ForeignKey.limit_choices_to` & `ForeignKey.related_name` & `ForeignKey.related_query_name`

same as `ForeignKey`

`ManyToManyField.symmetrical`

```py
from django.db import models

class Person(models.Model):
    friends = models.ManyToManyField("self")
```

When Django processes this model, it identifies that it has a `ManyToManyField` on itself, and as a result, it doesn’t add a `person_set` attribute to the Person class. Instead, the `ManyToManyField` is assumed to be symmetrical – that is, if I am your friend, then you are my friend.

`ManyToManyField.through`

Django will automatically generate a table to manage many-to-many relationships. __However, if you want to manually specify the intermediary table, you can use the through option to specify the Django model that represents the intermediate table that you want to use__.

The most common use for this option is when you want to [associate extra data with a many-to-many relationship](https://docs.djangoproject.com/en/3.1/topics/db/models/#intermediary-manytomany).

If you don’t specify an explicit through model, there is still an implicit through model class you can use to directly access the table created to hold the association. It has three fields to link the models.

If the source and target models differ, the following fields are generated:

- `id`: the primary key of the relation.
- `<containing_model>_id`: the id of the model that declares the ManyToManyField.
- `<other_model>_id`: the id of the model that the ManyToManyField points to.

If the ManyToManyField points from and to the same model, the following fields are generated:

- `id`: the primary key of the relation.
- `from_<model>_id`: the id of the instance which points at the model (i.e. the source instance).
- `to_<model>_id`: the id of the instance to which the relationship points (i.e. the target model instance).

This class can be used to query associated records for a given model instance like a normal model:

>`Model.m2mfield.through.objects.all()`

`ManyToManyField.through_fields`

Only used when a custom intermediary model is specified.

Membership has two foreign keys to Person (person and inviter), which makes the relationship ambiguous and Django can’t know which one to use. In this case, you must explicitly specify which foreign keys Django should use using through_fields, as in the example above.

```py
from django.db import models

class Person(models.Model):
    name = models.CharField(max_length=50)

class Group(models.Model):
    name = models.CharField(max_length=128)
    members = models.ManyToManyField(
        Person,
        through='Membership',
        through_fields=('group', 'person'),
    )

class Membership(models.Model):
    group = models.ForeignKey(Group, on_delete=models.CASCADE)
    person = models.ForeignKey(Person, on_delete=models.CASCADE)
    inviter = models.ForeignKey(
        Person,
        on_delete=models.CASCADE,
        related_name="membership_invites",
    )
    invite_reason = models.CharField(max_length=64)
```

through_fields accepts a 2-tuple `('field1', 'field2')`, where `field1` is the name of the foreign key to the model the `ManyToManyField` is defined on (group in this case), and `field2` the name of the foreign key to the target model (person in this case).

__When you have more than one foreign key on an intermediary model to any (or even both) of the models participating in a many-to-many relationship, you must specify through_fields__. This also applies to recursive relationships when an intermediary model is used and there are more than two foreign keys to the model, or you want to explicitly specify which two Django should use.

`ManyToManyField.db_table`

The name of the table to create for storing the many-to-many data. If this is not provided, Django will assume a default name based upon the names of: the table for the model defining the relationship and the name of the field itself.

### OneToOneField

A `one-to-one` relationship. __Conceptually, this is similar to a `ForeignKey` with `unique=True`, but the “reverse” side of the relation will directly return a single object__.

__This works exactly the same as it does for ForeignKey__, including all the options regarding recursive and lazy relationships.

__If you do not specify the related_name argument for the `OneToOneField`, Django will use the lowercase name of the current model as default value__.
