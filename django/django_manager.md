# django manager

## customer manager

You can use a custom Manager in a particular model by extending the base Manager class and instantiating your custom Manager in your model.

There are two reasons you might want to customize a Manager:

1. add extra Manager methods
2. modify the initial QuerySet the Manager returns.

### Adding extra manager methods

Adding extra Manager methods is the preferred way to add “table-level” functionality to your models. (For “row-level” functionality – i.e., functions that act on a single instance of a model object – use Model methods, not custom Manager methods.)

__A custom Manager method can return anything you want. It doesn’t have to return a QuerySet.__

> Another thing to note about this example is that Manager methods can access `self.model` to get the model class to which they’re attached.

### Modifying a manager’s initial QuerySet

You can override a Manager’s base QuerySet by overriding the Manager.get_queryset() method. get_queryset() should return a QuerySet with the properties you require.

__One model cant have multiples managers.__

#### Default manager

> If you use custom Manager objects, take note that the first Manager Django encounters __(in the order in which they’re defined in the model)__ has a special status. Django interprets the first Manager defined in a class as the “default” Manager, and several parts of Django (including dumpdata) will use that Manager exclusively for that model. As a result, it’s a good idea to be careful in your choice of default manager in order to avoid a situation where overriding get_queryset() results in an inability to retrieve objects you’d like to work with.

You can specify a custom default manager using `Meta.default_manager_name`.

#### Base manager

By default, Django uses an instance of the `Model._base_manager` manager class when accessing related objects (i.e. choice.question), not the `_default_manager` on the related object. This is because Django needs to be able to retrieve the related object, even if it would otherwise be filtered out (and hence be inaccessible) by the default manager.

If the normal base manager class (django.db.models.Manager) isn’t appropriate for your circumstances, you can tell Django which class to use by setting `Meta.base_manager_name`.

__Don’t filter away any results in this type of manager subclass__

This manager is used to access objects that are related to from some other model. In those situations, Django has to be able to see all the objects for the model it is fetching, so that anything which is referred to can be retrieved.

Therefore, you should not override get_queryset() to filter out any rows. If you do so, Django will return incomplete results.

#### Creating a manager with QuerySet methods

`QuerySet.as_manager()` can be used to create an instance of Manager with a copy of a custom QuerySet’s methods.

Methods are copied according to the following rules:

- Public methods are copied by default.
- Private methods (starting with an underscore) are not copied by default.
- Methods with a queryset_only attribute set to False are always copied.
- Methods with a queryset_only attribute set to True are never copied.

#### classmethod from_queryset(queryset_class)

For advanced usage you might want both a `custom Manager` and a `custom QuerySet`. You can do that by calling `Manager.from_queryset()` which returns a subclass of your `base Manager` with a copy of the `custom QuerySet` methods:

```py
class CustomManager(models.Manager):
    def manager_only_method(self):
        return

class CustomQuerySet(models.QuerySet):
    def manager_and_queryset_method(self):
        return

class MyModel(models.Model):
    objects = CustomManager.from_queryset(CustomQuerySet)()
```

### Custom managers and model inheritance

1. Managers from base classes are always inherited by the child class, using Python’s normal name resolution order (names on the child class override all others; then come names on the first parent class, and so on).

2. If no managers are declared on a model and/or its parents, Django automatically creates the objects manager.

3. The default manager on a class is either the one chosen with `Meta.default_manager_name`, or the first manager declared on the model, or the default manager of the first parent model.

### [Implementation concerns](https://docs.djangoproject.com/en/3.1/topics/db/managers/#implementation-concerns)