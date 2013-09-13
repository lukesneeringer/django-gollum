from django import forms as djforms
from gollum import forms
from gollum.fields import BoundField
import unittest


class FormSuite(unittest.TestCase):
    """A group of tests for testing the FormMarkupMixin, which is arguably
    the key offering of django-gollum.
    """
    def test_plain_form(self):
        """Establish that a regular form is created without incident
        ("do no harm").
        """
        # Make my form, and make an instance.
        class MyForm(forms.Form):
            foo = forms.CharField()
            bar = forms.IntegerField()
        form = MyForm()

        # Estblish that the instance looks more or less correct.
        self.assertIsInstance(form.fields['foo'], djforms.CharField)
        self.assertIsInstance(form.fields['bar'], djforms.IntegerField)

    def test_plain_form_bound(self):
        """Establish that a regular form is created with POST-like data
        without incident ("do no harm").
        """
        # Make my form, and make an instance.
        class MyForm(forms.Form):
            foo = forms.CharField()
            bar = forms.IntegerField()
        form = MyForm({ 'foo': 'baz', 'bar': '5' })

        # My data should be valid.
        self.assertEqual(form.is_valid(), True)

        # Check my data.
        self.assertEqual(form.cleaned_data['foo'], 'baz')
        self.assertEqual(form.cleaned_data['bar'], 5)

    def test_form_with_attrs(self):
        """Estblish that a form with an Attrs inner class gets
        the attrs as expected.
        """
        # Make my form and an instance.
        class AttrsForm(forms.Form):
            foo = forms.CharField()
            bar = forms.IntegerField()

            class Attrs:
                foo = { 'required': 'true' }
        form = AttrsForm()

        # Make sure my foo widget has a required attribute.
        self.assertEqual(form.fields['foo'].widget.attrs['required'], 'true')

    def test_form_with_css(self):
        """Establish that a form with a CSS inner class gets the
        CSS classes that we expect.
        """
        # Make my form and instance.
        class CSSForm(forms.Form):
            foo = forms.CharField()
            bar = forms.IntegerField()
            baz = forms.CharField()

            class CSS:
                foo = 'pure-u-1'
                baz = ['pure-u-2-3', 'pure-field']
        form = CSSForm()

        # Make sure my widgets have the expected attributes.
        self.assertEqual(form.fields['foo'].widget.css_classes, { 'pure-u-1' })
        self.assertEqual(
            form.fields['baz'].widget.css_classes,
            { 'pure-u-2-3', 'pure-field' },
        )
        self.assertEqual(
            hasattr(form.fields['bar'].widget, 'css_classes'),
            False,
        )

    def test_getitem(self):
        """Establish that our form sends back our specialized
        BoundField subclass.
        """
        # Make a form and instance.
        class MyForm(forms.Form):
            foo = forms.CharField()
        form = MyForm()

        # Get my bound field.
        bound_field = form['foo']

        # Ensure it's the class I expect -- mine.
        self.assertIsInstance(bound_field, BoundField)

    def test_bad_getitem(self):
        """Establish that if we try to retrieve a field that does not
        exist, that we raise KeyError.
        """
        # Make a form and instance.
        class MyForm(forms.Form):
            foo = forms.CharField()
        form = MyForm()

        # Try to get a bad field, and fail.
        with self.assertRaises(KeyError):
            form['bar']
