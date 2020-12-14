# django conrtib packages

## The Django admin site

### ModelAdmin objects

```py
from django.contrib import admin
from myproject.myapp.models import Author

class AuthorAdmin(admin.ModelAdmin):
    pass
admin.site.register(Author, AuthorAdmin)
```

simplified to

```py
from django.contrib import admin
from myproject.myapp.models import Author

admin.site.register(Author)
```

### The register decorator

```py
from django.contrib import admin
from .models import Author

@admin.register(Author)
class AuthorAdmin(admin.ModelAdmin):
    pass
```

## admin action

### Writing action functions

- The current ModelAdmin
- An HttpRequest representing the current request,
- A QuerySet containing the set of objects selected by the user.
Our publish-these-articles function won’t need the ModelAdmin or the request object, but we will use the queryset:

```py
from django.contrib import admin
from myapp.models import Article

def make_published(modeladmin, request, queryset):
    queryset.update(status='p')
make_published.short_description = "Mark selected stories as published"

class ArticleAdmin(admin.ModelAdmin):
    list_display = ['title', 'status']
    ordering = ['title']
    actions = [make_published]

admin.site.register(Article, ArticleAdmin)
```

### Advanced action techniques

#### Actions as ModelAdmin methods

```py
class ArticleAdmin(admin.ModelAdmin):
    ...

    actions = ['make_published']

    def make_published(self, request, queryset):
        queryset.update(status='p')
    make_published.short_description = "Mark selected stories as published"
```

#### Actions that provide intermediate pages

[Actions that provide intermediate pages](https://docs.djangoproject.com/en/3.1/ref/contrib/admin/actions/#actions-that-provide-intermediate-pages)

#### Making actions available site-wide

```py
from django.contrib import admin

admin.site.add_action(export_selected_objects)
#admin.site.add_action(export_selected_objects, 'export_selected')
```

#### Disabling actions

```py
admin.site.disable_action('delete_selected')
```

delete all actions

```py
class MyModelAdmin(admin.ModelAdmin):
    actions = None
```

#### Setting permissions for actions

```py
def make_published(modeladmin, request, queryset):
    queryset.update(status='p')
make_published.allowed_permissions = ('change',)
```

### some useful propeties

formfield_overrides

[list_display](https://docs.djangoproject.com/en/3.1/ref/contrib/admin/#django.contrib.admin.ModelAdmin.list_display)

[list_editable](https://docs.djangoproject.com/en/3.1/ref/contrib/admin/#django.contrib.admin.ModelAdmin.list_editable)

[list_filter](https://docs.djangoproject.com/en/3.1/ref/contrib/admin/#django.contrib.admin.ModelAdmin.list_filter)

### custom template options

https://docs.djangoproject.com/en/3.1/ref/contrib/admin/#custom-template-options

### ModelAdmin Method

https://docs.djangoproject.com/en/3.1/ref/contrib/admin/#modeladmin-methods

### ModelAdmin asset definitions

https://docs.djangoproject.com/en/3.1/ref/contrib/admin/#modeladmin-asset-definitions

### InlineModelAdmin objects

The difference between these two is merely the template used to render them.

- TabularInline
- StackedInline

### Working with a model with two or more foreign keys to the same parent model

https://docs.djangoproject.com/en/3.1/ref/contrib/admin/#working-with-a-model-with-two-or-more-foreign-keys-to-the-same-parent-model

### Working with many-to-many models

https://docs.djangoproject.com/en/3.1/ref/contrib/admin/#working-with-many-to-many-models

### Working with many-to-many intermediary models

https://docs.djangoproject.com/en/3.1/ref/contrib/admin/#working-with-many-to-many-intermediary-models

### Using generic relations as an inline

https://docs.djangoproject.com/en/3.1/ref/contrib/admin/#using-generic-relations-as-an-inline

## ** Overriding admin templates

[origin link](https://docs.djangoproject.com/en/3.1/ref/contrib/admin/#overriding-admin-templates)

### Set up your projects admin template directories

The admin template files are located in the `contrib/admin/templates/admin` directory.

In order to override one or more of them, first create an admin directory in your project’s templates directory. This can be any of the directories you specified in the DIRS option of the DjangoTemplates backend in the TEMPLATES setting. If you have customized the 'loaders' option, be sure 'django.template.loaders.filesystem.Loader' appears before 'django.template.loaders.app_directories.Loader' so that your custom templates will be found by the template loading system before those that are included with django.contrib.admin.

Within this admin directory, create sub-directories named after your app. Within these app subdirectories create sub-directories named after your models. Note, that the admin app will lowercase the model name when looking for the directory, so make sure you name the directory in all lowercase if you are going to run your app on a case-sensitive filesystem.

To override an admin template for a specific app, copy and edit the template from the `django/contrib/admin/templates/admin` directory, and save it to one of the directories you just created.

For example, if we wanted to add a tool to the change list view for all the models in an app named my_app, we would copy `contrib/admin/templates/admin/change_list.html` to the `templates/admin/my_app/` directory of our project, and make any necessary changes.

If we wanted to add a tool to the change list view for only a specific model named ‘Page’, we would copy that same file to the `templates/admin/my_app/page` directory of our project.

### AdminSite objects

> A Django administrative site is represented by an instance of django.contrib.admin.sites.AdminSite; by default, an instance of this class is created as django.contrib.admin.site and you can register your models and ModelAdmin instances with it.

[orignal reference](https://docs.djangoproject.com/en/3.1/ref/contrib/admin/#adminsite-objects
)

### Customizing the AdminSite class

First subclass AdminSite and override or add anything you like. Create an instance of your AdminSite subclass (the same way you’d instantiate any other Python class) and register your models and ModelAdmin subclasses with it instead of with the default site. Finally, update `myproject/urls.py` to reference your AdminSite subclass.

### Overriding the default admin site

[link](https://docs.djangoproject.com/en/3.1/ref/contrib/admin/#overriding-the-default-admin-site)

### Multiple admin sites in the same URLconf

> AdminSite instances take a single argument to their constructor, their name, which can be anything you like. This argument becomes the prefix to the URL names for the purposes of reversing them. `This is only necessary if you are using more than one AdminSite`.

## LogEntry objectss

The LogEntry class tracks additions, changes, and deletions of objects done through the admin interface.
