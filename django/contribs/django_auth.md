# auth

## User authentication in Django

### Using the Django authentication system

Only one class of user exists in Django’s authentication framework, i.e., _'superusers'_ or admin _'staff'_ users are just user objects with special attributes set, not different classes of user objects.

#### User objects

##### Creating users

```py
>>> from django.contrib.auth.models import User
>>> user = User.objects.create_user('john', 'lennon@thebeatles.com', 'johnpassword')

# At this point, user is a User object that has already been saved
# to the database. You can continue to change its attributes
# if you want to change other fields.
>>> user.last_name = 'Lennon'
>>> user.save()
```

##### Creating superusers

`$ python manage.py createsuperuser --username=joe --email=joe@example.com`

##### Changing passwords

Django does not store raw (clear text) passwords on the user model, but _only a hash_.

```py
>>> from django.contrib.auth.models import User
>>> u = User.objects.get(username='john')
>>> u.set_password('new password')
>>> u.save()
```

##### Authenticating users

Use `authenticate()` to verify a set of credentials. It takes credentials as keyword arguments, _username_ and _password_ for the default case, checks them against each authentication backend, and returns a _User object_ if the credentials are valid for a backend. If the credentials aren’t valid for any backend or if a backend raises `PermissionDenied`, it returns `None`.

#### Permissions and Authorization

The Django admin site uses permissions as follows:

- Access to view objects is limited to users with the `“view”` or `“change”` permission for that type of object.
- Access to view the `“add”` form and add an object is limited to users with the `“add”` permission for that type of object.
- Access to view the change list, view the `“change”` form and change an object is limited to users with the `“change”` permission for that type of object.
- Access to delete an object is limited to users with the `“delete”` permission for that type of object.

__Permissions can be set not only per type of object, but also per specific object instance.__ By using the `has_view_permission()`, `has_add_permission()`, `has_change_permission()` and `has_delete_permission()` methods provided by the _ModelAdmin_ class, it is possible to customize permissions for different object instances of the same type.

User objects have two `many-to-many` fields: __groups__ and __user_permissions__. User objects can access their related objects in the same way as any other Django model.

##### Default permissions

When _django.contrib.auth_ is listed in your _INSTALLED_APPS_ setting, it will ensure that four default permissions – _add_, _change_, _delete_, and _view_ – are created for each Django model defined in one of your installed applications.

These permissions will be created when you run `manage.py migrate`; the first time you run migrate after adding _django.contrib.auth_ to _INSTALLED_APPS_, the default permissions will be created for all previously-installed models, as well as for any new models being installed at that time. Afterward, it will create default permissions for new models each time you run `manage.py migrate` (the function that creates permissions is connected to the post_migrate signal).

Assuming you have an application with an app_label `foo` and a model named `Bar`, to test for basic permissions you should use:

```py
add: user.has_perm('foo.add_bar')
change: user.has_perm('foo.change_bar')
delete: user.has_perm('foo.delete_bar')
view: user.has_perm('foo.view_bar')
```

##### Groups

A user can belong to any number of groups.

##### Programmatically creating permissions

```py
from myapp.models import BlogPost
from django.contrib.auth.models import Permission
from django.contrib.contenttypes.models import ContentType

content_type = ContentType.objects.get_for_model(BlogPost)
permission = Permission.objects.create(
    codename='can_publish',
    name='Can Publish Posts',
    content_type=content_type,
)
```

##### Permission caching

If you are adding permissions and checking them immediately afterward, in a test or view for example, __the easiest solution is to re-fetch the user from the database__.

##### Proxy models

If you want to create permissions for a `proxy model`, pass `for_concrete_model=False` to `ContentTypeManager.get_for_model()` to get the appropriate `ContentType`.

Proxy models work exactly the same way as concrete models. Permissions are created using the own content type of the proxy model. __Proxy models don’t inherit the permissions of the concrete model they subclass.__

#### Authentication in Web requests

Django uses `sessions` and `middleware` to hook the authentication system into request objects.

These provide a `request.user` attribute on every request which represents the current user. If the current user has not logged in, this attribute will be set to an instance of `AnonymousUser`, otherwise it will be an instance of User.

You can tell them apart with `is_authenticated`, like so:

```py
if request.user.is_authenticated:
    # Do something for authenticated users.
    ...
else:
    # Do something for anonymous users.
    ...
```

##### How to log a user in

`login(request, user, backend=None)`

###### Selecting the authentication backend

The authentication backend to save in the session is selected as follows:

1. Use the value of the optional backend argument, if provided.
2. Use the value of the `user.backend` attribute, if present. This allows pairing `authenticate()` and `login()`: `authenticate()` sets the `user.backend` attribute on the user object it returns.
3. Use the backend in `AUTHENTICATION_BACKENDS`, if there is only one.
4. Otherwise, raise an exception.

##### How to log a user out

`logout(request)`

##### Limiting access to logged-in users

###### The login_required decorator

`login_required(redirect_field_name='next', login_url=None)`

##### The LoginRequired mixin

When using `class-based views`, you can achieve the same behavior as with login_required by using the `LoginRequiredMixin`. __This mixin should be at the leftmost position in the inheritance list.__

```py
from django.contrib.auth.mixins import LoginRequiredMixin

class MyView(LoginRequiredMixin, View):
    login_url = '/login/'
    redirect_field_name = 'redirect_to'
```

##### Limiting access to logged-in users that pass a test

`user_passes_test(test_func, login_url=None, redirect_field_name='next')`

##### UserPassesTestMixin

When using `class-based` views, you can use the `UserPassesTestMixin` to do this.

You have to override the `test_func()` method of the class to provide the test that is performed.

You can also override the `get_test_func()` method to have the mixin use a differently named function for its checks (instead of test_func()).

##### The permission_required decorator

`permission_required(perm, login_url=None, raise_exception=False)`

```py
from django.contrib.auth.decorators import permission_required

@permission_required('polls.add_choice', login_url='/loginpage/')
def my_view(request):
    ...
```

##### The PermissionRequiredMixin mixin

```py
from django.contrib.auth.mixins import PermissionRequiredMixin

class MyView(PermissionRequiredMixin, View):
    permission_required = 'polls.add_choice'
    # Or multiple of permissions:
    permission_required = ('polls.view_choice', 'polls.change_choice')
```

You may also override these methods:

`get_permission_required()`

> Returns an iterable of permission names used by the mixin. Defaults to the permission_required attribute, converted to a tuple if necessary.

`has_permission()`

> Returns a boolean denoting whether the current user has permission to execute the decorated view. By default, this returns the result of calling has_perms() with the list of permissions returned by get_permission_required().

#### Redirecting unauthorized requests in class-based views

[class AccessMixin](https://docs.djangoproject.com/en/3.1/topics/auth/default/#django.contrib.auth.mixins.AccessMixin)

##### Session invalidation on password change

`update_session_auth_hash(request, user)`

> This function takes the current request and the updated user object from which the new session hash will be derived and updates the session hash appropriately. It also rotates the session key so that a stolen session cookie will be invalidated.

> Since `get_session_auth_hash()` is based on `SECRET_KEY`, updating your site to use a new secret will invalidate all existing sessions.

#### Authentication Views

##### Using the views

There are different methods to implement these views in your project. The easiest way is to include the provided URLconf in `django.contrib.auth.urls` in your own URLconf, for example:

```py
urlpatterns = [
    path('accounts/', include('django.contrib.auth.urls')),
]```
```

##### All authentication views

[detail](https://docs.djangoproject.com/en/3.1/topics/auth/default/#all-authentication-views)

#### Authentication data in templates

##### Users

When rendering a template `RequestContext`, the currently logged-in user, either a `User` instance or an `AnonymousUser` instance, is stored in the template variable `{{ user }}`:

```py
{% if user.is_authenticated %}
    <p>Welcome, {{ user.username }}. Thanks for logging in.</p>
{% else %}
    <p>Welcome, new user. Please log in.</p>
{% endif %}
```

##### Permissions

Evaluating a single-attribute lookup of `{{ perms }}` as a boolean is a proxy to `User`.`has_module_perms()`.

For example, to check if the logged-in user has any permissions in the foo app:

`{% if perms.foo %}`

Evaluating a two-level-attribute lookup as a boolean is a proxy to `User.has_perm()`. For example, to check if the logged-in user has the permission foo.add_vote:

`{% if perms.foo.add_vote %}`

It is possible to also look permissions up by `{% if in %}` statements. For example:

```py
{% if 'foo' in perms %}
    {% if 'foo.add_vote' in perms %}
        <p>In lookup works, too.</p>
    {% endif %}
{% endif %}
```

## Customizing authentication in Django

TODO

## Password management in Django

TODO
