Django-Redactor
================


This package helps integrate the `Redactor <http://redactorjs.com/>`_ Javascript WYSIWYG-editor in Django.

Installation
----------------

# Add the ``redactor`` directory to your Python path.
# Add the ``redactor`` application to your `INSTALLED_APPS <https://docs.djangoproject.com/en/1.4/ref/settings/#installed-apps>`_ setting.

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
            'lang': 'es',
            'overlay': False
        }))


Django-redactor also includes some some customizations that make it function and look better in the Django admin. You should turn those on if you are using this widget in the admin::

    class MyAdmin(admin.ModelAdmin):
        formfield_overrides = {
                'widget': RedactorEditor(in_admin=True)
            }
        }