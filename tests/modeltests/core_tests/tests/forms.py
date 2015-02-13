from django.test import TestCase
from django.test.client import RequestFactory
from django import forms

from modeltests.core_tests.widgy_config import widgy_site
from modeltests.core_tests.models import VariegatedFieldsWidget, WidgetWithHTMLHelpText

from widgy.widgets import DateTimeWidget, DateWidget, TimeWidget


factory = RequestFactory()


class TestFormCreation(TestCase):
    def test_field_with_choices(self):
        widget = VariegatedFieldsWidget.add_root(widgy_site)
        form_class = widget.get_form_class(request=None)()
        self.assertIsInstance(form_class.fields['color'].widget, forms.Select)

    def test_date_fields(self):
        widget = VariegatedFieldsWidget.add_root(widgy_site)
        form_class = widget.get_form_class(request=None)()

        self.assertIsInstance(form_class.fields['date'].widget, DateWidget)
        self.assertIsInstance(form_class.fields['time'].widget, TimeWidget)
        self.assertIsInstance(form_class.fields['datetime'].widget, DateTimeWidget)


class TestFieldAsDiv(TestCase):
    def test_field_as_div_allows_html_in_help_text(self):
        widget = WidgetWithHTMLHelpText.add_root(widgy_site)
        request = factory.get('/')
        rendered_form = widget.get_form_template(request)
        self.assertIn('Your<br>Name', rendered_form)
