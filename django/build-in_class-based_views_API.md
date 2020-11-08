# build-in class-based views API

__A view is a callable which takes a request and returns a response.__ This can be more than just a function, and Django provides an example of some classes which can be used as views. These allow you to structure your views and reuse code by harnessing inheritance and mixins.

- [class base view](https://docs.djangoproject.com/en/3.1/topics/class-based-views/)
- [Introduction to class-based views](https://docs.djangoproject.com/en/3.1/topics/class-based-views/intro/)
- [Built-in class-based generic views](https://docs.djangoproject.com/en/3.1/topics/class-based-views/generic-display/)
- [Form handling with class-based views](https://docs.djangoproject.com/en/3.1/topics/class-based-views/generic-editing/)
- [Using mixins with class-based views](https://docs.djangoproject.com/en/3.1/topics/class-based-views/mixins/)

## class base view

__Note also that you can only inherit from one generic view - that is, only one parent class may inherit from View and the rest (if any) should be mixins.__ Trying to inherit from more than one class that inherits from View - for example, trying to use a form at the top of a list and combining ProcessFormView and ListView - won’t work as expected.

### Decorating class-based views

Decorating in URLconf

```py
urlpatterns = [
    path('about/', login_required(TemplateView.as_view(template_name="secret.html"))),
    path('vote/', permission_required('polls.can_vote')(VoteView.as_view())),
]
```

Decorating the class

```py
from django.utils.decorators import method_decorator

class ProtectedView(TemplateView):
    template_name = 'secret.html'

    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        return super().dispatch(*args, **kwargs)


# decorate repeatedly
decorators = [never_cache, login_required]

@method_decorator(decorators, name='dispatch')
class ProtectedView(TemplateView):
    template_name = 'secret.html'

@method_decorator(never_cache, name='dispatch')
@method_decorator(login_required, name='dispatch')
class ProtectedView(TemplateView):
    template_name = 'secret.html'
```

### expands

`from django.shortcuts import render`

## Built-in class-based generic views

Specifying model = Publisher is shorthand for saying queryset = Publisher.objects.all().

## Using mixins with class-based views

合理地使用已有的`Mixin`，有选择性的继承和覆盖已有的方法。

### 具有启发性的例子

```py
from django.views import View

class AuthorDetail(View):

    def get(self, request, *args, **kwargs):
        view = AuthorDisplay.as_view()
        return view(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        view = AuthorInterest.as_view()
        return view(request, *args, **kwargs)

```
