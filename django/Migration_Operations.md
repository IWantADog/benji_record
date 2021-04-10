# Migration Operations

## Adding migrations to apps

`python manage.py migrate --fake-initial`

## Reversing migrations

__Migrations can be reversed with migrate by passing the number of the previous migration.__

`$ python manage.py migrate books 0002`

If you want to reverse all migrations applied for an app, use the name `zero`:

`$ python manage.py migrate books zero`

## TODO

[Migrations](https://docs.djangoproject.com/en/3.1/topics/migrations/)