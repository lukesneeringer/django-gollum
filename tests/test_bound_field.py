from django.conf import settings
from django.test.utils import override_settings
from gollum import forms
from gollum.fields import BoundField
import re
import six
import unittest


class BoundFieldSuite(unittest.TestCase):
    """A group of tests to establish that the BoundField subclass
    works as intended.
    """
    def setUp(self):
        # Save the form class to the instance.
        class MyForm(forms.Form):
            foo = forms.CharField()
            bar = forms.IntegerField(required=False)
        self.form_class = MyForm

        # Save BoundFields for foo and bar.
        form = MyForm()
        self.foo_bf = form['foo']
        self.bar_bf = form['bar']

    def test_plain_bound_field(self):
        """Estblish that a plain call to BoundField.as_widget with
        no special settings works as expected.
        """
        output = six.text_type(self.foo_bf)
        assert '<input' in output
        assert 'id="id_foo"' in output
        assert 'name="foo"' in output

    def test_global_attrs(self):
        """Establish that the `FORM_GLOBAL_ATTRS` setting sets
        the global attributes expected.
        """
        with override_settings(FORM_GLOBAL_ATTRS={ 'data-id': 1234 }):
            output = six.text_type(self.foo_bf)
        assert 'data-id="1234"' in output

    def test_required_attrs(self):
        """Establish that the `FORM_REQUIRED_ATTRS` setting causes
        the expected attributes to be set.
        """
        with override_settings(FORM_REQUIRED_ATTRS={ 'required': 'true' }):
            foo_output = six.text_type(self.foo_bf)
            bar_output = six.text_type(self.bar_bf)
        assert 'required="true"' in foo_output
        assert 'required="true"' not in bar_output

    def test_optional_attrs(self):
        """Establish that the `FORM_OPTIONAL_ATTRS` setting causes
        the expected attributes to be set.
        """
        with override_settings(FORM_OPTIONAL_ATTRS={ 'placeholder': 'opt' }):
            foo_output = six.text_type(self.foo_bf)
            bar_output = six.text_type(self.bar_bf)
        assert 'placeholder="opt"' not in foo_output
        assert 'placeholder="opt"' in bar_output

    def test_required_css_class(self):
        """Establish that the `FORM_REQUIRED_CSS_CLASS` setting works
        as intended.
        """
        with override_settings(FORM_REQUIRED_CSS_CLASS='required'):
            foo_output = six.text_type(self.foo_bf)
            bar_output = six.text_type(self.bar_bf)
        assert re.search(r'class="[\s\w-]*required[\s\w-]*"', foo_output)
        assert not re.search(r'class="[\s\w-]*required[\s\w-]*"', bar_output)

    def test_error_css_class(self):
        """Establish that the `FORM_ERROR_CSS_CLASS` setting works
        as intended.
        """
        form = self.form_class({ 'foo': 'eggs', 'bar': 'baz' })
        form.is_valid()
        with override_settings(FORM_ERROR_CSS_CLASS='error'):
            foo_output = six.text_type(form['foo'])
            bar_output = six.text_type(form['bar'])
        assert not re.search(r'class="[\s\w-]*error[\s\w-]*"', foo_output)
        assert re.search(r'class="[\s\w-]*error[\s\w-]*"', bar_output)

    def test_global_css_class(self):
        """Establish that the `FORM_GLOBAL_CSS_CLASS` setting works
        as intended.
        """
        form = self.form_class({ 'foo': 'eggs', 'bar': 'baz' })
        form.is_valid()
        with override_settings(FORM_GLOBAL_CSS_CLASS='global'):
            foo_output = six.text_type(form['foo'])
            bar_output = six.text_type(form['bar'])
        assert re.search(r'class="[\s\w-]*global[\s\w-]*"', foo_output)
        assert re.search(r'class="[\s\w-]*global[\s\w-]*"', bar_output)

    def test_css_from_widget_class(self):
        """Establish that a CSS class on a widget itself is included
        in the BoundField output.
        """
        # Create a form and get the necessary BoundField.
        class NewForm(forms.Form):
            foo = forms.CharField()
            class CSS:
                foo = 'pure-u-1'
        bf = NewForm()['foo']

        # Establish that the class is present.
        assert 'class=" pure-u-1"' in six.text_type(bf)

    def test_direct_css_class_string(self):
        """Establish that a directly specified CSS class is processed
        as intended.
        """
        output = self.foo_bf.as_widget(css_classes='spam eggs')
        assert re.search(r'class="[\s\w-]*spam[\s\w-]*"', output)
        assert re.search(r'class="[\s\w-]*eggs[\s\w-]*"', output)

    def test_direct_css_class_bytes(self):
        """Establish that a directly specified CSS class is processed
        as intended if it is sent down as a bytes object.
        """
        output = self.foo_bf.as_widget(css_classes='baz'.encode('utf8'))
        assert re.search(r'class="[\s\w-]*baz[\s\w-]*"', output)

    def test_direct_attr_specification(self):
        """Establish that directly specifying an attribute to .as_widget
        still works as intended.
        """
        output = self.foo_bf.as_widget(attrs={ 'required': 'true'})
        assert 'required="true"' in output
