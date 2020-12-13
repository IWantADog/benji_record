# The contenttypes framework

Instances of `ContentType` represent and store information about the models installed in your project, and new instances of `ContentType` are automatically created whenever new models are installed.

Instances of `ContentType` have methods for returning the model classes they represent and for querying objects from those models. `ContentType` also has a custom manager that adds methods for working with `ContentType` and for obtaining instances of `ContentType` for a particular model.

## Methods on ContentType instances

`ContentType.get_object_for_this_type(**kwargs)`
> Takes a set of valid lookup arguments for the model the `ContentType` represents, and does a `get()` lookup on that model, returning the corresponding object.

`ContentType.model_class()`
> Returns the model class represented by this `ContentType` instance.

```py
>>> from django.contrib.contenttypes.models import ContentType
>>> user_type = ContentType.objects.get(app_label='auth', model='user')
>>> user_type
<ContentType: user>
# And then use it to query for a particular User, or to get access to the User model class:

>>> user_type.model_class()
<class 'django.contrib.auth.models.User'>
>>> user_type.get_object_for_this_type(username='Guido')
<User: Guido>
```

Together, `get_object_for_this_type()` and `model_class()` enable two extremely important use cases:

1. Using these methods, you can write high-level generic code that performs queries on any installed model – instead of importing and using a single specific model class, you can pass an _app_label_ and model into a `ContentType` lookup at runtime, and then work with the model class or retrieve objects from it.

2. You can relate another model to `ContentType` as a way of tying instances of it to particular model classes, and use these methods to get access to those model classes.

__Latter technique is amazing.__

## Generic relations

__Adding a foreign key from one of your own models to ContentType allows your model to effectively tie itself to another model class,__ as in the example of the Permission model above.

But it’s possible to go one step further and use `ContentType` to enable truly generic (sometimes called “polymorphic”) relationships between models.

__The contenttypes application provides a special field type `(GenericForeignKey)` which works around this and allows the relationship to be with any model.__

### GenericForeignKey

There are three parts to setting up a `GenericForeignKey`:

1. Give your model a `ForeignKey` to `ContentType`. The usual name for this field is “content_type”.
2. Give your model a field that can store primary key values from the models you’ll be relating to. For most models, this means a `PositiveIntegerField`. The usual name for this field is “object_id”.
3. Give your model a `GenericForeignKey`, and pass it the names of the two fields described above. If these fields are named “content_type” and “object_id”, you can omit this – those are the default field names `GenericForeignKey` will look for.

```py
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from django.db import models

class TaggedItem(models.Model):
    tag = models.SlugField()
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    object_id = models.PositiveIntegerField()
    content_object = GenericForeignKey('content_type', 'object_id')

    def __str__(self):
        return self.tag
```

Due to the way `GenericForeignKey` is implemented, you cannot use such fields directly with filters (`filter()` and `exclude()`, for example) via the database API. Because a `GenericForeignKey` isn’t a normal field object, these examples will not work:

```py
# This will fail
>>> TaggedItem.objects.filter(content_object=guido)
# This will also fail
>>> TaggedItem.objects.get(content_object=guido)
```

## Reverse generic relations

If you know which models you’ll be using most often, you can also add a “reverse” generic relationship to enable an additional API. For example:

```py
from django.contrib.contenttypes.fields import GenericRelation
from django.db import models

class Bookmark(models.Model):
    url = models.URLField()
    tags = GenericRelation(TaggedItem)
    # Defining GenericRelation with related_query_name set allows querying from the related object:
    tags = GenericRelation(TaggedItem, related_query_name='bookmark')
```

Just as `GenericForeignKey` accepts the names of the content-type and object-ID fields as arguments, so too does `GenericRelation`; if the model which has the generic foreign key is using non-default names for those fields, you must pass the names of the fields when setting up a GenericRelation to it. For example, if the TaggedItem model referred to above used fields named `content_type_fk` and `object_primary_key` to create its generic foreign key, then a GenericRelation back to it would need to be defined like so:

```py
tags = GenericRelation(
    TaggedItem,
    content_type_field='content_type_fk',
    object_id_field='object_primary_key',
)
```
