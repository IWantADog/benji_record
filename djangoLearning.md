# Django Learning

## start 
django-admin startproject projectName

python manager.py startapp appName

python manager.py runserver

[setting.py](https://docs.djangoproject.com/en/1.10/topics/settings/)

[url.py](https://docs.djangoproject.com/en/1.10/topics/http/urls/)

[wsgi](https://docs.djangoproject.com/en/1.10/topics/http/urls/)

[runserver](https://docs.djangoproject.com/en/1.10/ref/django-admin/#django-admin-runserver)

[databases](https://docs.djangoproject.com/en/1.10/ref/settings/#std:setting-DATABASES)

[template](https://docs.djangoproject.com/en/1.10/topics/templates/)

[generate view document](https://docs.djangoproject.com/en/1.10/topics/class-based-views/)

[test is django](https://docs.djangoproject.com/en/1.10/topics/testing/)

[list display](https://docs.djangoproject.com/en/1.10/ref/contrib/admin/#django.contrib.admin.ModelAdmin.list_display)

[Change list pagination](https://docs.djangoproject.com/en/1.10/ref/contrib/admin/#django.contrib.admin.ModelAdmin.list_per_page)

[search boxes](https://docs.djangoproject.com/en/1.10/ref/contrib/admin/#django.contrib.admin.ModelAdmin.search_fields)

[filters](https://docs.djangoproject.com/en/1.10/ref/contrib/admin/#django.contrib.admin.ModelAdmin.list_filter)

[date-hierarchies](https://docs.djangoproject.com/en/1.10/ref/contrib/admin/#django.contrib.admin.ModelAdmin.date_hierarchy)

[column-header-ordering](https://docs.djangoproject.com/en/1.10/ref/contrib/admin/#django.contrib.admin.ModelAdmin.list_display)

[Advanced tutorial: How to write reusable apps](https://docs.djangoproject.com/en/1.10/intro/reusable-apps/)

[work with form](https://docs.djangoproject.com/en/1.10/topics/forms/)

[form api](https://docs.djangoproject.com/en/1.10/ref/forms/)

[custorm template tags](https://docs.djangoproject.com/en/1.10/howto/custom-template-tags/)

[See the template loading documentation for more information about how Django finds its templates.](https://docs.djangoproject.com/en/1.10/topics/templates/#template-loading)

For more information on model relations, [see Accessing related objects](https://docs.djangoproject.com/en/1.10/ref/models/relations/). For more on how to use double underscores to perform field lookups via the API, see [Field lookups](https://docs.djangoproject.com/en/1.10/topics/db/queries/#field-lookups-intro). For full details on the database API, see [our Database API reference](https://docs.djangoproject.com/en/1.10/topics/db/queries/).

python manage.py runserver 8080 修改启动的端口号

`question = models.ForeignKey(Question, on_delete=models.CASCADE)` models.CASCADE ????

 python manage.py check
 > this checks for any problems in your project without making migrations or touching the database.

### remember the three-step guide to making model changes

- Change your models (in models.py).
- Run python manage.py makemigrations to create migrations for those changes
- Run python manage.py migrate to apply those changes to the database.


### python manage.py shell

### python manage.py createsuperuser


### Make the poll app modifiable in the admin
polls/admin.py
```python

from django.contrib import admin

from .models import Question

admin.site.register(Question)

```

## 2020.02.12

setting.py ROOT_URLCONF 参数的作用

### Template namespacing

Within the templates directory you have just created, create another directory called polls, and within that create a file called index.html. In other words, your template should be at polls/templates/polls/index.html. Because of how the app_directories template __loader__ works as described above, you can refer to this template within Django simply as polls/index.html.

> Now we might be able to get away with putting our templates directly in polls/templates (rather than creating another polls subdirectory), but it would actually be a bad idea. Django will choose the first template it finds whose name matches, and if you had a template with the same name in a different application, Django would be unable to distinguish between them. We need to be able to point Django at the right one, and the easiest way to ensure this is by namespacing them. That is, by putting those templates inside another directory named for the application itself.

### render 

`from django.shortcut import render`

The render() function takes the request object as its first argument, a template name as its second argument and a dictionary as its optional third argument. It returns an HttpResponse object of the given template rendered with the given context.

### from django.http import Http404

`raise Http404("Question does not exist")`

### get_object_or_404()

The get_object_or_404() function takes a Django model as its first argument and an arbitrary number of keyword arguments, which it passes to the get() function of the model’s manager. It raises Http404 if the object doesn’t exist.


### Removing hardcoded URLs in templates

`<li><a href="{% url 'detail' question.id %}">{{ question.question_text }}</a></li>`

The problem with this hardcoded, tightly-coupled approach is that it becomes challenging to change URLs on projects with a lot of templates. However, since you defined the name argument in the url() functions in the polls.urls module, you can remove a reliance on specific URL paths defined in your url configurations by using the {% url %} template tag:


### Namespacing URL names
The tutorial project has just one app, polls. In real Django projects, there might be five, ten, twenty apps or more. How does Django differentiate the URL names between them? For example, the polls app has a detail view, and so might an app on the same project that is for a blog. How does one make it so that Django knows which app view to create for a url when using the {% url %} template tag?

The answer is to add namespaces to your URLconf. In the polls/urls.py file, go ahead and add an app_name to set the application namespace:


### question.choice_set.all()? 从哪里来的方法。

### reverse方法


### [race condation](https://docs.djangoproject.com/en/1.10/ref/models/expressions/#avoiding-race-conditions-using-f)


[ListView](https://docs.djangoproject.com/en/1.10/ref/class-based-views/generic-display/#django.views.generic.list.ListView)

[DetailView](https://docs.djangoproject.com/en/1.10/ref/class-based-views/generic-display/#django.views.generic.detail.DetailView)


## 2020.02.13

### django test 

python manage.py test polls

`from django.test import TestCase`


from django.test.utils import setup_test_environment

[assertContains()](https://docs.djangoproject.com/en/1.10/topics/testing/tools/#django.test.SimpleTestCase.assertContains)

[assertQuerysetEqual()](https://docs.djangoproject.com/en/1.10/topics/testing/tools/#django.test.TestCase)

### style

First, create a directory called static in your polls directory. Django will look for static files there, similarly to how Django finds templates inside polls/templates/.

Django’s STATICFILES_FINDERS setting contains a list of finders that know how to discover static files from various sources. One of the defaults is AppDirectoriesFinder which looks for a “static” subdirectory in each of the INSTALLED_APPS, like the one in polls we just created. The admin site uses the same directory structure for its static files.

Within the static directory you have just created, create another directory called polls and within that create a file called style.css. In other words, your stylesheet should be at polls/static/polls/style.css. Because of how the AppDirectoriesFinder staticfile finder works, you can refer to this static file in Django simply as polls/style.css, similar to how you reference the path for templates.

```html
{% load static %}

<link rel="stylesheet" type="text/css" href="{% static 'polls/style.css' %}" />
```

#### static namespace

Just like templates, we might be able to get away with putting our static files directly in polls/static (rather than creating another polls subdirectory), but it would actually be a bad idea. Django will choose the first static file it finds whose name matches, and if you had a static file with the same name in a different application, Django would be unable to distinguish between them. We need to be able to point Django at the right one, and the easiest way to ensure this is by namespacing them. That is, by putting those static files inside another directory named for the application itself.

### Customize the admin form
By registering the Question model with admin.site.register(Question), Django was able to construct a default form representation. Often, you’ll want to customize how the admin form looks and works. You’ll do this by telling Django the options you want when you register the object.

Let’s see how this works by reordering the fields on the edit form. Replace the admin.site.register(Question) line with:


```python
polls/admin.py
from django.contrib import admin

from .models import Question


class QuestionAdmin(admin.ModelAdmin):
    fields = ['pub_date', 'question_text']

admin.site.register(Question, QuestionAdmin)
```

## 2020.02.14

### form

```python
class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['name', 'email', 'url', 'text']
```

### 模版的继承

### app.py 的作用 && from django.apps import AppConfig的作用 [link](https://docs.djangoproject.com/en/1.10/ref/applications/)

## 2020.02.15

#### from django.contrib.syndication.views import Feed

Django comes with a high-level syndication-feed-generating framework that makes creating RSS and Atom feeds easy.

[The syndication feed framework](https://docs.djangoproject.com/en/1.10/ref/contrib/syndication/)


### from django.db.models import Q


## 2020.02.21

### django URLconfig

```python
urlpatterns = [
    path('admin/', admin.site.urls),
    path('book/', include('book.urls')),
]
```

## 2020.02.23

### 用户认证 [link](https://docs.djangoproject.com/en/3.0/topics/auth/default/)

### generic.ListView && generic.DetailView && LoginView 的调用方式？

## 2020.02.25

python3 setattr()

## 2020.03.01

### django file upload

1. setting file: 设置图片的存放路径 [参考](https://docs.djangoproject.com/en/3.0/topics/files/)
    `MEDIA_ROOT = os.path.join(BASE_DIR, 'images')`

2. model && form [model参考](https://docs.djangoproject.com/en/3.0/ref/models/fields/#filefield)

    ```python

    # model
    class AClass:
        img = models.ImageField(upload_to=user_directory_path)

    def user_directory_path(instance, filename):
        return 'user_img/{}/{}'.format(instance.user.id, filename)

    # form
    class MyForm():
            img = forms.ImageField(label='images')
    ```

3. html:[产考](https://docs.djangoproject.com/en/3.0/topics/http/file-uploads/)
    - __{% csrg_token %}__
    - form add attribute __enctype="multipart/form-data"__

    ```html
    <form action="{% url 'user_detail_edit' user.id %}" method="post" enctype="multipart/form-data">
        {% csrf_token %}
        ....
    </form>
    ```

4. view:[产考](https://docs.djangoproject.com/en/3.0/topics/http/file-uploads/)
    - 将 __request.FILES__ 计入FORM初始化中

    ```python
    form = UploadFileForm(request.POST, request.FILES)
    ```

5. serve local image:

    setting.py中MEDIA_URL和MEDIA_ROOT的关系
    例子：
    MEDIA_URL="/meida/"
    MEDIA_ROOT="/path/to/images"

    __http://1270.0.0.1/modeia/a.jpg__ 访问的是 __/path/to/images/a.jpg__

    ```python
    # must add in module urls. add in app url don't work
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

    ```

6. static file serve [link](https://docs.djangoproject.com/en/1.11/howto/static-files/)

7. http://www.threemeal.com/blog/29/
