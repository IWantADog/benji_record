# python import

## summary

It’s important to keep in mind that all packages are modules, but not all modules are packages. Or put another way, packages are just a special kind of module. Specifically, any module that contains a __path__ attribute is considered a package.

When a regular package is imported, this __init__.py file is implicitly executed, and the objects it defines are bound to names in the package’s namespace. The __init__.py file can contain the same Python code that any other module can contain, and Python will add some additional attributes to the module when it is imported.

## reference

[python import](https://docs.python.org/3.7/reference/import.htmls)

[PEP 302](https://www.python.org/dev/peps/pep-0302/)

[PEP 366](https://www.python.org/dev/peps/pep-0366/)s

[PEP 328](https://www.python.org/dev/peps/pep-0328/)

[PEP 420](https://www.python.org/dev/peps/pep-0420/)