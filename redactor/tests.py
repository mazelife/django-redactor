import unittest

from django import forms

from redactor import fields, widgets


class MyForm(forms.Form):
    text = forms.CharField(widget=widgets.RedactorEditor())


class MyAdminForm(forms.Form):
    """ Uses a redactor widget."""
    text = forms.CharField(widget=widgets.RedactorEditor(in_admin=True))


class MyOtherAdminForm(forms.Form):
    """ Uses a redactor field."""
    text = fields.RedactorField(in_admin=True)


class MySpanishForm(forms.Form):
    """ Uses a redactor widget."""
    text = forms.CharField(widget=widgets.RedactorEditor(redactor_settings={
        'lang': 'es'
    }))


class MyOtherSpanishForm(forms.Form):
    """ Uses a redactor field."""
    text = fields.RedactorField(redactor_settings={
        'lang': 'es'
    })


class RedactorTests(unittest.TestCase):

    def test_field_rendering(self):
        """
        Ensure a widget and a field render the same way.
        """
        form_with_widget = MySpanishForm()
        form_with_field = MyOtherSpanishForm()
        self.assertEqual(
            form_with_widget.as_p(),
            form_with_field.as_p()
        )
        form_with_widget = MyAdminForm()
        form_with_field = MyOtherAdminForm()
        self.assertEqual(
            form_with_widget.as_p(),
            form_with_field.as_p()
        )

    def test_widget_rendering(self):
        """
        Ensure that the form widget renders as expected.
        """
        form = MyForm()
        html = form.as_p()
        js = (
            'Redactor.register({"lang": "en", "load": true, "in_admin": false, '
            '"focus": false, "autoresize": true, "path": false, "toolbar": "default"});'
        )
        el = (
            '<textarea id="id_text" class="redactor_content" rows="10" '
            'cols="40" name="text">'
        )
        self.assertTrue(js in html)
        self.assertTrue(el in html)
        self.assertFalse('django_admin.css' in "".join(form.media.render_css()))

        admin_form = MyAdminForm()
        admin_html = admin_form.as_p()
        self.assertTrue('"in_admin": true' in admin_html)
        self.assertTrue('django_admin.css' in "".join(admin_form.media.render_css()))

        spanish_form = MySpanishForm()
        spanish_html = spanish_form.as_p()
        spanish_js = 'Redactor.register({"lang": "es", "in_admin": false});'
        self.assertTrue(spanish_js in spanish_html)
        self.assertFalse('django_admin.css' in "".join(spanish_form.media.render_css()))        