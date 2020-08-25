# django form

## bound and unbound form

A Form instance is either bound to a set of data, or unbound.

`Form.is_bound`

- If it’s bound to a set of data, it’s capable of validating that data and rendering the form as HTML with the data displayed in the HTML.
- If it’s unbound, it cannot do validation (because there’s no data to validate!), but it can still render the blank form as HTML.

To bind data to a form, pass the data as a dictionary as the first parameter to your Form class constructor:

```sh
>>> data = {'subject': 'hello',
...         'message': 'Hi there',
...         'sender': 'foo@example.com',
...         'cc_myself': True}
>>> f = ContactForm(data)
```

__If you have a bound Form instance and want to change the data somehow, or if you want to bind an unbound Form instance to some data, create another Form instance. There is no way to change data in a Form instance. Once a Form instance has been created, you should consider its data immutable, whether it has data or not.__

## Using forms to validate data

this article about how form and filed validate is very useful. __[form and filed validate](https://docs.djangoproject.com/en/3.1/ref/forms/validation/#validating-fields-with-clean)__

`Form.clean()`:

Implement a clean() method on your Form when you must add custom validation for fields that are interdependent.

`Form.is_valid()`:

The primary task of a Form object is to validate data.

Deal with Form Errors

`Form.errors`:

Access the errors attribute to get a dictionary of error messages. In this dictionary, the keys are the field names, and the values are lists of strings representing the error messages. The error messages are stored in lists because a field can have multiple error messages.

`Form.errors.as_data()`:

Returns a dict that maps fields to their original ValidationError instances. Use this method anytime you need to identify an error by its code.

`Form.errors.as_json()`:

Returns the errors serialized as JSON.

`Form.errors.get_json_data()`:

Returns the errors as a dictionary suitable for serializing to JSON. Form.errors.as_json() returns serialized JSON, while this returns the error data before it’s serialized.

`Form.add_error()`:

This method allows adding errors to specific fields from within the Form.clean() method, or from outside the form altogether; for instance from a view.

`Form.has_error()`:

This method returns a boolean designating whether a field has an error with a specific error code. If code is None, it will return True if the field contains any errors at all.

`Form.non_fields_errors()`:

This method returns the list of errors from Form.errors that aren’t associated with a particular field.

## Dynamic initial values

`Form.initial`:

Use initial to declare the initial value of form fields at runtime.

```sh
f = ContactForm(initial={'subject': 'Hi there!'})
```

If a `Field` defines initial and you include initial when instantiating the `Form`, then the latter initial will have precedence. In this example, initial is provided both at the field level and at the form instance level, and the latter gets precedence.

`Form.get_initial_for_field(field, field_name)`:

Use get_initial_for_field() to retrieve initial data for a form field. __It retrieves data from Form.initial and Field.initial, in that order, and evaluates any callable initial values.__

### Checking which form data has changed

`Form.has_changed()`:

Use the `has_changed()` method on your `Form` when you need to check if the form data has been changed from the initial data.

`Form.changed_data`:

The changed_data attribute returns a list of the names of the fields whose values in the form’s bound data (usually `request.POST`) differ from what was provided in `initial`. It returns an empty list if no data differs.

### Accessing the fields from the form

`Form.fields`:

Access the fields of `Form` instance from its `fields` attribute.

### Accessing "clean" data

`Form.cleaned_data`:

get cleaned data after `Form.is_valid()`.

When the Form is valid, cleaned_data will include a key and value for all its fields, __even if the data didn’t include a value for some optional fields.__

## outputting forms as HTML

`Form.as_p()` & `Form.as_ul()` & `Form.as_table()`.

This default output is a two-column HTML table, with a `<tr>`for each field. Notice the following:

- For flexibility, the output does not include the `<table>` and `</table>` tags, nor does it include the `<form>` and `</form>`tags or an `<input type="submit">` tag. It’s your job to do that.

- Each field type has a default HTML representation. CharField is represented by an `<input type="text">` and EmailField by an `<input type="email">`. BooleanField(null=False) is represented by an `<input type="checkbox">`. Note these are merely sensible defaults; you can specify which HTML to use for a given field by using widgets, which we’ll explain shortly.

- The HTML name for each tag is taken directly from its attribute name in the ContactForm class.
The text label for each field – e.g. 'Subject:', 'Message:' and 'Cc myself:' is generated from the field name by converting all underscores to spaces and upper-casing the first letter. Again, note these are merely sensible defaults; you can also specify labels manually.

- Each text label is surrounded in an HTML `<label>` tag, which points to the appropriate form field via its id. Its id, in turn, is generated by prepending 'id_' to the field name. The id attributes and `<label>` tags are included in the output by default, to follow best practices, but you can change that behavior.

- The output uses HTML5 syntax, targeting `<!DOCTYPE html>`. For example, it uses boolean attributes such as checked rather than the XHTML style of checked='checked'.

### Styling required or erroneous form rows

`Form.error_css_class` & `Form.required_css_class`

The Form class has a couple of hooks you can use to add class attributes to required rows or to rows with errors: set the Form.error_css_class and/or Form.required_css_class attributes.

### Configuring form elements’ HTML id attributes and `<label>` tags

`Form.auto_id`

Use the auto_id argument to the Form constructor to control the id and label behavior. This argument must be `True`, `False` or a `string`.

If `auto_id` is `False`, then the form output will not include `<label>` tags nor id attributes.

If `auto_id` is set to `True`, then the form output will include `<label>` tags and will use the field name as its id for each form field.

If `auto_id` is set to a string containing the format character `'%s'`, then the form output will include `<label>` tags, and will generate id attributes based on the format string. For example, for a format string `'field_%s'`, a field named subject will get the id value `'field_subject'`.

If `auto_id` is set to any other true value – such as a string that doesn’t include `%s` – then the library will act as if `auto_id` is `True`.

By default, `auto_id` is set to the string `'id_%s'`.

`Form.label_suffix`

A translatable string (defaults to a colon (:) in English) that will be appended after any label name when a form is rendered.

`Form.use_required_attribute`

When set to `True` (the default), required form fields will have the `required` HTML attribute.

### configuring the rendering of a form's widgets

`Form.default_renderer`

Specifies the renderer to use for the form. Defaults to None which means to use the default renderer specified by the FORM_RENDERER setting.

how to use it.

```py
from django import forms

class MyForm(forms.Form):
    default_renderer = MyRenderer()

# OR

form = MyForm(renderer=MyRenderer())
```

### Notes on field ordering

`Form.field_order`:

By default `Form.field_order=None`, which retains the order in which you define the fields in your form class. If `field_order` is a list of field names, the fields are ordered as specified by the list and remaining fields are appended according to the default order. Unknown field names in the list are ignored. This makes it possible to disable a field in a subclass by setting it to None without having to redefine ordering.

You can also use the `Form.field_order` argument to a `Form` to override the field order. If a `Form` defines `field_order` and you include `field_order` when instantiating the Form, then the latter `field_order` will have precedence.

`Form.order_fields(field_order)`

You may rearrange the fields any time using order_fields() with a list of field names as in field_order.

### How errors are displayed

If you render a bound Form object, the act of rendering will automatically run the form’s validation if it hasn’t already happened, and the HTML output will include the validation errors as a `<ul class="errorlist">` near the field.

### customizing the error list format

By default, forms use `django.forms.utils.ErrorList` to format validation errors. If you’d like to use an alternate class for displaying errors, you can pass that in at construction time.

### More granular output

about [BoundField](https://docs.djangoproject.com/en/3.1/ref/forms/api/#django.forms.BoundField)

### Customizing BoundField

If you need to access some additional information about a form field in a template and using a subclass of `Field` isn’t sufficient, consider also customizing `BoundField`.

A custom form field can override `get_bound_field()`:

`Field.get_bound_field(form, field_name)`
> Takes an instance of Form and the name of the field. The return value will be used when accessing the field in a template. Most likely it will be an instance of a subclass of BoundField.

## Binding uploaded files to a form

[Binding uploaded files to a form](https://docs.djangoproject.com/en/3.1/ref/forms/api/#binding-uploaded-files-to-a-form)

## testing for multipart forms

`Form.is_multipart()`

If you’re writing reusable views or templates, you may not know ahead of time whether your form is a multipart form or not. The is_multipart() method tells you whether the form requires multipart encoding for submission.

## Subclassing forms

same to python normal class inherit.

It’s possible to declaratively remove a Field inherited from a parent class by setting the name of the field to None on the subclass.

## Prefixes for forms

You can put several Django forms inside one `<form>` tag. To give each Form its own namespace, use the prefix keyword argument.

```py
mother = PersonForm(prefix="mother")
```
