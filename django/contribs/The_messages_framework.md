# The messages framework

## Enabling messages

The default `settings.py` created by `django-admin startproject` already contains all the settings required to enable message functionality:

1. `'django.contrib.messages'` is in `INSTALLED_APPS`.

2. `MIDDLEWARE` contains `'django.contrib.sessions.middleware.SessionMiddleware'` and `'django.contrib.messages.middleware.MessageMiddleware'`.

   > The default storage backend relies on sessions. That’s why `SessionMiddleware` must be enabled and appear before `MessageMiddleware` in `MIDDLEWARE`.

3. The `'context_processors'` option of the DjangoTemplates backend defined in your `TEMPLATES` setting contains `'django.contrib.messages.context_processors.messages'`.

If you don’t want to use messages, you can remove 'django.contrib.messages' from your INSTALLED_APPS, the MessageMiddleware line from MIDDLEWARE, and the messages context processor from TEMPLATES.

## Configuring the message engine

### Storage backends

`class storage.session.SessionStorage`

>This class stores all messages inside of the request’s session. Therefore it requires Django’s contrib.sessions application.

`class storage.cookie.CookieStorage`

>This class stores the message data in a cookie (signed with a secret hash to prevent manipulation) to persist notifications across requests. Old messages are dropped if the cookie data size would exceed 2048 bytes.

`class storage.fallback.FallbackStorage`

> This class first uses CookieStorage, and falls back to using SessionStorage for the messages that could not fit in a single cookie. It also requires Django’s contrib.sessions application.

> This behavior avoids writing to the session whenever possible. It should provide the best performance in the general case.

__FallbackStorage is the default storage class.__ If it isn’t suitable to your needs, you can select another storage class by setting `MESSAGE_STORAGE` to its full import path, for example:

```py
MESSAGE_STORAGE = 'django.contrib.messages.storage.cookie.CookieStorage'
```

### Message levels

DEBUG、INFO、SUCCESS、WARNING、ERROR

### Message tags

__Tags are stored in a string and are separated by spaces.__ Typically, message tags are used as CSS classes to customize message style based on message type. By default, each level has a single tag that’s a lowercase version of its own constant:

Level Constant   | Tag
-----------------|-----
DEBUG            | debug
INFO             | info
SUCCESS          | success
WARNING          | warning
ERROR            | error

## Using messages in views and templates

`add_message(request, level, message, extra_tags='', fail_silently=False)`

### Adding a message

```py
from django.contrib import messages
messages.add_message(request, messages.INFO, 'Hello world.')
```

Some shortcut methods provide a standard way to add messages with commonly used tags (which are usually represented as HTML classes for the message):

```py
messages.debug(request, '%s SQL statements were executed.' % count)
messages.info(request, 'Three credits remain in your account.')
messages.success(request, 'Profile details updated.')
messages.warning(request, 'Your account expires in three days.')
messages.error(request, 'Document deleted.')
```

### Displaying messages

`get_messages(request)`

```py
{% if messages %}
<ul class="messages">
    {% for message in messages %}
    <li{% if message.tags %} class="{{ message.tags }}"{% endif %}>{{ message }}</li>
    {% endfor %}
</ul>
{% endif %}
```

### Creating custom message levels

Messages levels are nothing more than integers, so you can define your own level constants and use them to create more customized user feedback.

### Changing the minimum recorded level per-request

```py
messages.set_level(request, messages.DEBUG)

current_level = messages.get_level(request)
```

### Adding extra message tags

`messages.add_message(request, messages.INFO, 'Over 9000!', extra_tags='dragonball')`

### Failing silently when the message framework is disabled

```py
messages.add_message(
    request, messages.SUCCESS, 'Profile details updated.',
    fail_silently=True,
)
```

> Setting `fail_silently=True` only hides the `MessageFailure` that would otherwise occur when the messages framework disabled and one attempts to use one of the add_message family of methods. It does not hide failures that may occur for other reasons.

### Adding messages in class-based views

[link](https://docs.djangoproject.com/en/3.1/ref/contrib/messages/#adding-messages-in-class-based-views)

### Expiration of messages

The messages are marked to be cleared when the storage instance is iterated (and cleared when the response is processed).

```py
storage = messages.get_messages(request)
for message in storage:
    do_something_with(message)
storage.used = False
```

### Behavior of parallel requests

[link](https://docs.djangoproject.com/en/3.1/ref/contrib/messages/#behavior-of-parallel-requests)
