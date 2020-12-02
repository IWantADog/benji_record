# Application

The application is thread-safe so that multiple Celery applications with different configurations, components, and tasks can co-exist in the same process space.

## Main Name

### Configuration

`config_from_object`

## Laziness

The `app.task()` decorators don’t create the tasks at the point when the task is defined, instead it’ll defer the creation of the task to happen either when the task is used, or after the application has been finalized,
