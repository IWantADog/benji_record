# django-admin and manage.py

## Usage

```py
$ django-admin <command> [options]
$ manage.py <command> [options]
$ python -m django <command> [options]
```

## Available commands

- check
- compilemessages
- createcachetable
- dbshell
- diffsettings
- dumpdata

   > Outputs to standard output all data in the database associated with the named application(s).

- flush

    >Removes all data from the database and re-executes any post-synchronization handlers. The table of which migrations have been applied is not cleared.

- inspectdb
- loaddata
- makemigrations
- migrate
- runserver
- sendtestemail
- shell
- showmigrations
- sqlflush
- sqlmigrate
- startapp
- startproject
- test
- testserver
- changepassword
- createsuperuser
- clearsessions
- collectstatic
- findstatic
