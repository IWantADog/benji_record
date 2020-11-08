# django applications

## Configuring applications

### For application authors

If you’re creating a pluggable app called “Rock ’n’ roll”, here’s how you would provide a proper name for the admin:

> The recommended convention is to put the configuration class in a submodule of the application called `apps`

```py
# rock_n_roll/apps.py

from django.apps import AppConfig

class RockNRollConfig(AppConfig):
    name = 'rock_n_roll'
    verbose_name = "Rock ’n’ roll"
```

You can also tell your users to put `'rock_n_roll.apps.RockNRollConfig'` in their `INSTALLED_APPS` setting. __You can even provide several different AppConfig subclasses with different behaviors and allow your users to choose one via their `INSTALLED_APPS` setting__.

INSTALLED_APPS:
> A list of strings designating all applications that are enabled in this Django installation. Each string should be a dotted Python path to: `an application configuration class (preferred)` or `a package containing an application`.
> Your code should never access `INSTALLED_APPS` directly. Use `django.apps.apps` instead.

### For application users

If you’re using “Rock ’n’ roll” in a project called anthology, but you want it to show up as “Jazz Manouche” instead, you can provide your own configuration:

```py
# anthology/apps.py

from rock_n_roll.apps import RockNRollConfig

class JazzManoucheConfig(RockNRollConfig):
    verbose_name = "Jazz Manouche"

# anthology/settings.py

INSTALLED_APPS = [
    'anthology.apps.JazzManoucheConfig',
    # ...
]
```

## Application configuration

[Application Class](https://docs.djangoproject.com/en/3.1/ref/applications/#application-configuration)

## reference

[How applications are loaded](https://docs.djangoproject.com/en/3.1/ref/applications/#how-applications-are-loaded)
