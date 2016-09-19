from __future__ import absolute_import

from django import forms
from exam import fixture

from sentry.testutils import TestCase
from sentry.web.forms import OriginsField


class OriginsFieldTest(TestCase):
    @fixture
    def field(self):
        return OriginsField()

    def test_supports_wildcards(self):
        value = '*'
        result = self.field.clean(value)
        self.assertEquals(result, ['*'])

    def test_supports_wildcard_domains(self):
        value = '*.example.com'
        result = self.field.clean(value)
        self.assertEquals(result, ['*.example.com'])

    def test_supports_base_domains(self):
        value = 'example.com'
        result = self.field.clean(value)
        self.assertEquals(result, ['example.com'])

    def test_does_not_support_port(self):
        value = 'http://example.com:80'
        with self.assertRaises(forms.ValidationError):
            self.field.clean(value)

        value = 'example.com:80'
        with self.assertRaises(forms.ValidationError):
            self.field.clean(value)

    def test_doesnt_support_domain_with_port(self):
        value = 'example.com:80'
        with self.assertRaises(forms.ValidationError):
            self.field.clean(value)

    def test_doesnt_support_wildcard_domain_with_port(self):
        value = '*.example.com:80'
        with self.assertRaises(forms.ValidationError):
            self.field.clean(value)

    def test_supports_localhost(self):
        value = 'localhost'
        result = self.field.clean(value)
        self.assertEquals(result, ['localhost'])
