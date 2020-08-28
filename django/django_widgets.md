# django widgets

`Widgets` should not be confused with the form fields. Form fields deal with the logic of input validation and are used directly in templates. __Widgets deal with rendering of HTML form input elements on the web page and extraction of raw submitted data. However, widgets do need to be assigned to form fields.__

## Specifying widgets

Whenever you specify a field on a form, Django will use a default widget that is appropriate to the type of data that is to be displayed. If you want to use a different widget for a field, you can use the widget argument on the field definition.

## Setting arguments for widgets

Many widgets have optional extra arguments; they can be set when defining the widget on the field.

## Customizing widget instances

When Django renders a widget as HTML, it only renders very minimal markup - __Django doesn’t add class names, or any other widget-specific attributes__. This means, for example, that all `TextInput` widgets will appear the same on your Web pages.

### Styling widget instances

If you want to make one widget instance look different from another, you will need to specify additional attributes at the time when the widget object is instantiated and assigned to a form field (and perhaps add some rules to your CSS files).

`Widget.attrs`:

```py
class CommentForm(forms.Form):
    name = forms.CharField(widget=forms.TextInput(attrs={'class': 'special'}))
    url = forms.URLField()
    comment = forms.CharField(widget=forms.TextInput(attrs={'size': '40'}))

# OR

class CommentForm(forms.Form):
    name = forms.CharField()
    url = forms.URLField()
    comment = forms.CharField()

    name.widget.attrs.update({'class': 'special'})
    comment.widget.attrs.update(size='40')

# Or if the field isn’t declared directly on the form (such as model form fields), you can use the Form.fields attribute:

class CommentForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['name'].widget.attrs.update({'class': 'special'})
        self.fields['comment'].widget.attrs.update(size='40')
```

### Styling widget classes

#### Assets as a static definition

```py
from django import forms

class CalendarWidget(forms.TextInput):
    class Media:
        css = {
            'all': ('pretty.css',)
        }
        js = ('animations.js', 'actions.js')
```

This static definition is converted at runtime into a widget property named media. The list of assets for a CalendarWidget instance can be retrieved through this property:

```sh
>>> w = CalendarWidget()
>>> print(w.media)
<link href="http://static.example.com/pretty.css" type="text/css" media="all" rel="stylesheet">
<script src="http://static.example.com/animations.js"></script>
<script src="http://static.example.com/actions.js"></script>
```

#### css

A dictionary describing the CSS files required for various forms of output media.

__The keys in the dictionary are the output media types__. These are the same types accepted by CSS files in media declarations: ‘all’, ‘aural’, ‘braille’, ‘embossed’, ‘handheld’, ‘print’, ‘projection’, ‘screen’, ‘tty’ and ‘tv’. __If you need to have different stylesheets for different media types, provide a list of CSS files for each output medium__.

If a group of CSS files are appropriate for multiple output media types, __the dictionary key can be a comma separated list of output media types__.

```py
class Media:
    css = {
        'screen': ('pretty.css',),
        'tv,projector': ('lo_res.css',),
        'print': ('newspaper.css',)
    }
```

#### extend

__By default, any object using a static Media definition will inherit all the assets associated with the parent widget__. This occurs regardless of how the parent defines its own requirements.

If you don’t want Media to be inherited in this way, add an `extend=False` declaration to the Media declaration.

#### Media as a dynamic property

If you need to perform some more sophisticated manipulation of asset requirements, you can define the media property directly. This is done by defining a widget property that returns an instance of `forms.Media`. The constructor for `forms.Media` accepts `css` and `js` keyword arguments in the same format as that used in a static media definition.

```py
class CalendarWidget(forms.TextInput):
    @property
    def media(self):
        return forms.Media(css={'all': ('pretty.css',)},
                           js=('animations.js', 'actions.js'))
```

#### Paths in asset definitions

To find the appropriate prefix to use, Django will check if the `STATIC_URL` setting is not None and automatically fall back to using `MEDIA_URL`.

#### Media objects

If you only want files of a particular type, you can use the subscript operator to filter out a medium of interest. For example:

```sh
>>> print(w.media)
<link href="http://static.example.com/pretty.css" type="text/css" media="all" rel="stylesheet">
<script src="http://static.example.com/animations.js"></script>
<script src="http://static.example.com/actions.js"></script>

>>> print(w.media['css'])
<link href="http://static.example.com/pretty.css" type="text/css" media="all" rel="stylesheet">
```

#### Combining Media objects

`Media` objects can also be added together. When two Media objects are added, the resulting Media object contains the union of the assets specified by both.

#### Order of assets

The order in which assets are inserted into the DOM is often important. For example, you may have a script that depends on jQuery. __Therefore, combining Media objects attempts to preserve the relative order in which assets are defined in each Media class__.

#### Media In Forms

__Widgets aren’t the only objects that can have media definitions – forms can also define media__. The rules for media definitions on forms are the same as the rules for widgets: declarations can be static or dynamic; path and inheritance rules for those declarations are exactly the same.

Regardless of whether you define a media declaration, all Form objects have a media property. The default value for this property is the result of adding the media definitions for all widgets that are part of the form.

__If you want to associate additional assets with a form – for example, CSS for form layout – add a Media declaration to the form__.














