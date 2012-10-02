Django-Redactor
================


This package helps integrate the `Redactor <http://redactorjs.com/>`_ Javascript WYSIWYG-editor in Django.

Installation
----------------

#. Add the ``redactor`` directory to your Python path.
#. Add the ``redactor`` application to your `INSTALLED_APPS <https://docs.djangoproject.com/en/1.4/ref/settings/#installed-apps>`_ setting.

Usage
----------------

The redactor app provides a Django widget called ``RedactorEditor``. It is a drop-in replacement for any ``TextArea`` widget. Example usage::

    from django import forms
    from django.db import models

    from redactor.widgets import RedactorEditor

    class MyForm(forms.Form):
        about_me = forms.CharField(widget=RedactorEditor())


You can also customize any of the Redactor editor's `settings <http://redactorjs.com/docs/settings/>`_ when instantiating the widget::

    class MyForm(forms.Form):
    
        about_me = forms.CharField(widget=RedactorEditor(redactor_settings={
            'autoformat': True,
            'overlay': False
        }))


Django-redactor also includes a widget with some some customizations that make it function and look better in the Django admin::

    class MyAdmin(admin.ModelAdmin):
        formfield_overrides = {
                models.TextField: {'widget': AdminRedactorEditor},
        }

Finally, you can connect a custom CSS file to the editable area of the editor::

    class MyForm(forms.Form):
        about_me = forms.CharField(widget=RedactorEditor(
            redactor_css="styles/text.css")
        )

Paths used to specify CSS can be either relative or absolute. If a path starts with '/', 'http://' or 'https://', it will be interpreted as an absolute path, and left as-is. All other paths will be prepended with the value of the ``STATIC_URL`` setting (or ``MEDIA_URL`` if static is not defined).

For the sake of convenience, there is also a form field that can be used that accepts the same inputs. This field can be used anywhere ``forms.CharField`` can and accepts the same arguments, but always renders a Redactor widget::

    from redactor.fields import RedactorField

    class MyForm(forms.Form):
        about_me = RedactorField(
            in_admin=True,
            redactor_css="styles/text.css",
            redactor_settings={'overlay': True}
        )

Internationalization
^^^^^^^^^^^^^^^^^^^^^^^^^

If you wish to use Redactor in other languages, you'll need to specify the setting and make sure the correct language file is loaded::

    class MyForm(forms.Form):

        class Media:
            js = ('django-redactor/redactor/langs/es.js',)
    
        about_me = forms.CharField(widget=RedactorEditor(redactor_settings={
            'autoformat': True,
            'lang': 'es',
            'overlay': False
        }))



Django-Redactor is licensed under a `Creative Commons Attribution-NonCommercial 3.0 <http://creativecommons.org/licenses/by-nc/3.0/>`_ license.
