# The staticfiles app

## Settings

- STATIC_ROOT
- STATIC_URL
- STATICFILES_DIRS
- STATICFILES_STORAGE
- STATICFILES_FINDERS

## Management Commands

[django-admin collectstatic](https://docs.djangoproject.com/en/3.1/ref/contrib/staticfiles/#django-admin-collectstatic)

[django-admin findstatic staticfile [staticfile ...]](https://docs.djangoproject.com/en/3.1/ref/contrib/staticfiles/#django-admin-findstatic)

[django-admin runserver [addrport]](https://docs.djangoproject.com/en/3.1/ref/contrib/staticfiles/#runserver)

## Managing static files (e.g. images, JavaScript, CSS)

### Configuring static files

1. Make sure that `django.contrib.staticfiles` is included in your `INSTALLED_APPS`.

2. In your settings file, define STATIC_URL, for example:`STATIC_URL = '/static/'`

3. In your templates, use the static template tag to build the URL for the given relative path using the configured STATICFILES_STORAGE.

    ```html
    {% load static %}
    <img src="{% static 'my_app/example.jpg' %}" alt="My image">
    ```

4. Store your static files in a folder called static in your app. For example `my_app/static/my_app/example.jpg`.

Your project will probably also have static assets that aren’t tied to a particular app. In addition to using a `static/` directory inside your apps, you can define a list of directories (`STATICFILES_DIRS`) in your settings file where Django will also look for static files. For example:

```py
STATICFILES_DIRS = [
    BASE_DIR / "static",
    '/var/www/static/',
]
```

## Deploying static files

https://docs.djangoproject.com/en/3.1/howto/static-files/deployment/