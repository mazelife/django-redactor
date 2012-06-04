import unittest

from django import forms

from redactor import widgets


class MyForm(forms.Form):
    text = forms.CharField(widget=widgets.RedactorEditor())


class MyAdminForm(forms.Form):
    text = forms.CharField(widget=widgets.RedactorEditor(in_admin=True))


class MySpanishForm(forms.Form):
    text = forms.CharField(widget=widgets.RedactorEditor(redactor_settings={
        'lang': 'es'
    }))


class RedactorTests(unittest.TestCase):

    def test_rendering(self):
        """
        Ensure that the form enders as expected.
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