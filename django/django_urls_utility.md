# django.urls utility

## django.urls utility functions

### `reverse()`

If you need to use something similar to the url template tag in your code, Django provides the following function:

```py
from news import views

path('archive/', views.archive, name='news-archive')

# 1
reverse('news-archive')

# 2
from news import views
reverse(views.archive)

# 3
reverse('arch-summary', args=[1945])

# 4
reverse('admin:app_list', kwargs={'app_label': 'auth'})
```

### `reverse_lazy()`

It is useful for when you need to use a URL reversal before your project’s URLConf is loaded. Some common cases where this function is necessary are:

- providing a reversed URL as the url attribute of a generic class-based view.
- providing a reversed URL to a decorator (such as the login_url argument for the django.contrib.auth.decorators.permission_required() decorator).
- providing a reversed URL as a default value for a parameter in a function’s signature.

### `resolve()`

The resolve() function can be used for resolving URL paths to the corresponding view functions.

## django.urls functions for use in URLconfs
