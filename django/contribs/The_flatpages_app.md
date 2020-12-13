# The flatpages app

A flatpage is a object with a _URL_, _title_ and _content_. Use it for one-off, special-case pages, such as “About” or “Privacy Policy” pages, that you want to store in a database but for which you don’t want to develop a custom Django application.

## Installation

1. Install the sites framework by adding `'django.contrib.sites'` to your `INSTALLED_APPS` setting, if it’s not already in there.

   > Also make sure you’ve correctly set SITE_ID to the ID of the site the settings file represents. This will usually be 1 (i.e. SITE_ID = 1, but if you’re using the sites framework to manage multiple sites, it could be the ID of a different site.

2. Add `'django.contrib.flatpages'` to your `INSTALLED_APPS` setting.

Then either:

3.Add an entry in your URLconf. For example:

urlpatterns = [
    path('pages/', include('django.contrib.flatpages.urls')),
]

or:

3.Add 'django.contrib.flatpages.middleware.FlatpageFallbackMiddleware' to your MIDDLEWARE setting.

4.Run the command manage.py migrate.

[Using the URLconf](https://docs.djangoproject.com/en/3.1/ref/contrib/flatpages/#using-the-urlconf)

[Using the middleware](https://docs.djangoproject.com/en/3.1/ref/contrib/flatpages/#using-the-middleware)

## How to add, change and delete flatpages

[link](https://docs.djangoproject.com/en/3.1/ref/contrib/flatpages/#how-to-add-change-and-delete-flatpages)

## Flatpage templates

By default, flatpages are rendered via the template _flatpages/default.html_, but you can override that for a particular flatpage: in the admin, a collapsed fieldset titled “Advanced options” (clicking will expand it) contains a field for specifying a template name. If you’re creating a flat page via the Python API you can set the template name as the field template_name on the FlatPage object.

Creating the _flatpages/default.html_ template is your responsibility; in your template directory, create a flatpages directory containing a file _default.html_.

Flatpage templates are passed a single context variable, `flatpage`, which is the flatpage object.

Here’s a sample flatpages/default.html template:

```html
<!DOCTYPE html>
<html>
<head>
<title>{{ flatpage.title }}</title>
</head>
<body>
{{ flatpage.content }}
</body>
</html>
```
