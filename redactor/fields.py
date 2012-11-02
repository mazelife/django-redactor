from django.forms.fields import CharField

from redactor.widgets import RedactorEditor


class RedactorField(CharField):
    """
    A ``CharField`` whose default widget is  a ``RedactorEditor``.
    Takes the following three additional args that are passed through to the
    widget constructor::

    class MyForm(forms.Form):
        my_field = RedactorField(
            redactor_css="styles/bodycopy.css",
            redactor_settings={'lang': 'es'}
        )

    """

    widget = RedactorEditor

    def __init__(self, *args, **kwargs):
        widget_kwargs = {}
        # Remove extra field kwargs: they will be used to instantiate the widget.
        for extra_kwarg in ('redactor_css', 'redactor_settings'):
            if extra_kwarg in kwargs:
                widget_kwargs[extra_kwarg] = kwargs.pop(extra_kwarg)

        super(RedactorField, self).__init__(*args, **kwargs)

        # Pass any keyword arguments to the Widget.
        if widget_kwargs:
            widget = kwargs.get('widget', None) or RedactorEditor
            if isinstance(widget, type):
                widget = widget(**widget_kwargs)
            if 'localize' in kwargs:
                widget.is_localized = True
            widget.is_required = kwargs.get('required', False)
            extra_attrs = self.widget_attrs(widget)
            if extra_attrs:
                widget.attrs.update(extra_attrs)
            self.widget = widget


try:
    from south.modelsinspector import add_introspection_rules
except ImportError:
    pass
else:
    add_introspection_rules([
        (
            (RedactorField, ),
            [],
            {
                "null": ["null", {"default": True}],
                "blank": ["blank", {"default": True}],
                "max_length": ["max_length", {"default": None}],
            },
        ),
    ], ["^redactor\.fields\.RedactorField"])
