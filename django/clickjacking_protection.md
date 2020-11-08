# django clickjacking protection

## An example of clickjacking

https://docs.djangoproject.com/en/3.1/ref/clickjacking/#an-example-of-clickjacking

## Preventing clickjacking

[X-Frame-Options](https://developer.mozilla.org/en-US/docs/Web/HTTP/Headers/X-Frame-Options)

> If you specify `DENY`, not only will attempts to load the page in a frame fail when loaded from other sites, attempts to do so will fail when loaded from the same site. On the other hand, if you specify `SAMEORIGIN`, you can still use the page in a frame as long as the site including it in a frame is the same as the one serving the page.

## how to use it

### Setting X-Frame-Options for all responses

```py
MIDDLEWARE = [
    ...
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    ...
]
```

By default, the middleware will set the `X-Frame-Options` header to `DENY` for every outgoing `HttpResponse`. If you want any other value for this header instead, set the `X_FRAME_OPTIONS`setting:

`X_FRAME_OPTIONS = 'SAMEORIGIN'`

`@xframe_options_exempt`

### Setting X-Frame-Options per view

```py
from django.http import HttpResponse
from django.views.decorators.clickjacking import xframe_options_deny
from django.views.decorators.clickjacking import xframe_options_sameorigin

@xframe_options_deny
def view_one(request):
    return HttpResponse("I won't display in any frame!")

@xframe_options_sameorigin
def view_two(request):
    return HttpResponse("Display in a frame if it's from the same origin as me.")
```
