from django import forms
from django.conf import settings
from gollum.utils import FieldValues
import unittest


class FieldValuesSuite(unittest.TestCase):
    """Test suite for assessing the FieldValues subclass of dict,
    and ensuring it gets values as I expect.
    """
    def test_attrs(self):
        """Establish that a FieldValues dict successfully imports
        an Attrs class.
        """
        # Define our fields and Attrs class.
        fields = {
            'foo': forms.CharField(max_length=50),
            'bar': forms.CharField(),
            'baz': forms.IntegerField(),
        }
        class Attrs:
            foo = { 'disabled': 'true' }
            baz = { 'data-spam': 'eggs' }

        # Make the initial FieldValues dict.
        fv = FieldValues()
        fv.update(fields, Attrs)

        # Take our temperature so far.
        self.assertEqual(fv, {
            'foo': { 'disabled': 'true' },
            'baz': { 'data-spam': 'eggs' },
        })

        # Add new attributes.
        class Attrs:
            foo = { 'disabled': 'false', 'required': 'true' }
        fv.update(fields, Attrs)

        # Make sure we have what we expect as the final answer.
        self.assertEqual(fv, {
            'foo': { 'disabled': 'false', 'required': 'true' },
            'baz': { 'data-spam': 'eggs' },
        })

    def test_css(self):
        """Establish that a FieldValues dict successfully imports
        a CSS class.
        """
        # Define our fields and CSS class
        fields = {
            'foo': forms.CharField(),
            'bar': forms.IntegerField(),
        }
        class CSS:
            foo = 'pure-u-1'
            bar = ['pure-u-2-3', 'pure-field']

        # Create our FieldValues dict.
        fv = FieldValues()
        fv.update(fields, CSS)

        # Ensure that we have what we expect.
        self.assertEqual(fv, {
            'foo': { 'pure-u-1' },
            'bar': { 'pure-u-2-3', 'pure-field' },
        })

        # Add a new CSS class to "foo".
        class CSS:
            foo = 'batman'
        fv.update(fields, CSS)

        # Ensure we still have what we expect.
        self.assertEqual(fv, {
            'foo': { 'pure-u-1', 'batman' },
            'bar': { 'pure-u-2-3', 'pure-field' },
        })

    def test_bad_class_name(self):
        """Establish that attempting to utilize FieldValues with an
        unexpected class name raises TypeError.
        """
        class Foo:
            bar = 'baz'
        fv = FieldValues()
        with self.assertRaises(TypeError):
            fv.update({ 'bar': None }, Foo)

    def test_bad_field(self):
        """Establish that if we attempt to define an attribute
        on a field that does not exist, that we raise KeyError.
        """
        class Attrs:
            bad = { 'disabled': 'true' }
        fv = FieldValues()
        with self.assertRaises(AttributeError):
            fv.update({}, Attrs)
