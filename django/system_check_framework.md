# django -- systtem check framework

[system check framework](https://docs.djangoproject.com/en/3.1/ref/checks/)
[system check framework how to guide](https://docs.djangoproject.com/en/3.1/topics/checks/)

The system check framework is a set of static checks for validating Django projects. It detects common problems and provides hints for how to fix them. The framework is extensible so you can easily add your own checks.

Checks can be triggered explicitly via the check command. Checks are triggered implicitly before most commands, including runserver and migrate. For performance reasons, checks are not run as part of the WSGI stack that is used in deployment. If you need to run system checks on your deployment server, trigger them explicitly using check.
