# jinja2

## Bytecode Cachea

## jinja2 template syntax

### Filters

build in filter

https://jinja.palletsprojects.com/en/2.11.x/templates/#builtin-filters

### tests

is

### Whitespace Control

trim_blocks & lstrip_blocks: 全局清除模版渲染是的空白行

手动清除空白行

`{%+ if something %}yay{% endif %}`

```
{% for item in seq -%}
    {{ item }}
{%- endfor %}
```

You must not add whitespace between the tag and the minus sign.

```
valid:

{%- if foo -%}...{% endif %}
invalid:

{% - if foo - %}...{% endif %}
```

### Escaping

{% raw %} {% endraw %}

### Template Inheritance

If you want to print a block multiple times, you can, however, use the special self variable and call the block with that name:

```html
<title>{% block title %}{% endblock %}</title>
<h1>{{ self.title() }}</h1>
{% block body %}{% endblock %}
```

{{ super() }}

#### Nesting extends

```py
# parent.tmpl
body: {% block body %}Hi from parent.{% endblock %}

# child.tmpl
{% extends "parent.tmpl" %}
{% block body %}Hi from child. {{ super() }}{% endblock %}

# grandchild1.tmpl
{% extends "child.tmpl" %}
{% block body %}Hi from grandchild1.{% endblock %}

# grandchild2.tmpl
{% extends "child.tmpl" %}
{% block body %}Hi from grandchild2. {{ super.super() }} {% endblock %}
```

### HTML Escaping

#### Working with Manual Escaping

`{{ user.username|e }}`

#### Working with Automatic Escaping

When automatic escaping is enabled, everything is escaped by default except for values explicitly marked as safe. Variables and expressions can be marked as safe either in:

1. The context dictionary by the application with markupsafe.Markup

2. The template, with the |safe filter.

### loop

#### recursive

It is also possible to use loops recursively. This is useful if you are dealing with recursive data such as sitemaps or RDFa. To use loops recursively, you basically have to add the recursive modifier to the loop definition and call the loop variable with the new iterable where you want to recurse.

The following example implements a sitemap with recursive loops:

```py
<ul class="sitemap">
{%- for item in sitemap recursive %}
    <li><a href="{{ item.href|e }}">{{ item.title }}</a>
    {%- if item.children -%}
        <ul class="submenu">{{ loop(item.children) }}</ul>
    {%- endif %}</li>
{%- endfor %}
</ul>
```

#### loop.previtem & loop.nextitem && loop.changed

### Macros

Macros are comparable with functions in regular programming languages. They are useful to put often used idioms into reusable functions to not repeat yourself (“DRY”).

https://jinja.palletsprojects.com/en/2.11.x/templates/#macros

### call

In some cases it can be useful to pass a macro to another macro.

https://jinja.palletsprojects.com/en/2.11.x/templates/#call

### Filters && Assignments

### Block Assignments

it’s possible to also use block assignments to capture the contents of a block into a variable name.

```
{% set navigation %}
    <li><a href="/">Index</a>
    <li><a href="/downloads">Downloads</a>
{% endset %}
```

### Import

This works similarly to the import statements in Python.

```
{% macro input(name, value='', type='text') -%}
    <input type="{{ type }}" value="{{ value|e }}" name="{{ name }}">
{%- endmacro %}

{% import 'forms.html' as forms %}

{% from 'forms.html' import input as input_field, textarea %}
```

### Import Context Behavior

By default, included templates are passed the current context and imported templates are not. The reason for this is that imports, unlike includes, are cached; as imports are often used just as a module that holds macros.

### {% debug %}

### With Statement

The with statement makes it possible to create a new inner scope. Variables set within this scope are not visible outside of the scope.