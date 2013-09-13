[![Build Status](https://travis-ci.org/lukesneeringer/django-gollum.png?branch=master)](https://travis-ci.org/lukesneeringer/django-gollum) [![Coverage](https://coveralls.io/repos/lukesneeringer/django-gollum/badge.png?branch=master)](https://coveralls.io/r/lukesneeringer/django-gollum)

This is **django-gollum**, a better way to mess with styling Django forms. gollum provides a better way to specify just the HTML Attributes and CSS classes you need on a Form subclass.

### Installation

To install django-gollum, just use:

    pip install django-gollum

### Getting Started

Adding HTML or CSS to a Django Form with gollum is easy:

  1. Subclass `gollum.forms.Form` or `gollum.forms.ModelForm`.
  2. Add a Attrs or CSS inner class specifying fields with extra HTML attributes or CSS, respectively.

Here's an example:

```python
from gollum import forms

class MyForm(forms.Form):
    foo = models.CharField(max_length=50)
    bar = models.IntegerField()

    class Attrs:
        bar = { 'placeholder': 25 }

    class CSS:
        foo = 'green'
        bar = ['purple', 'translucent']
```

When this form is rendered in the template, the "foo" `<input>` tag will have the "green" CSS class applied, and the "bar" `<input>` will have both "purple" and "translucent" applied. Additionally, the "bar" `<input>` would have `placeholder="25"` set as an HTML attribute.

### Documentation

Documentation is available at [Read the Docs][1].

  [1]: https://django-gollum.readthedocs.org/

### License

New BSD
