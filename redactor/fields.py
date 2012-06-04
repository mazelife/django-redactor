from django.forms.fields import CharField

from redactor.widgets import RedactorEditor

class RedactorField(CharField):
    """
    A ``CharField`` whose default widget is  a ``RedactorEditor``.
    Takes the following two additional args that are passed through to the
    widget constructor::
    
    class MyForm(forms.Form):
        my_field = RedactorField(
            in_admin=True,
            redactor_settings={'lang': 'es'}
        )
    
    """
    
    widget = RedactorEditor

    def __init__(self, *args, **kwargs):
        widget_kwargs = {}
        if 'redactor_settings' in kwargs:
            widget_kwargs['redactor_settings'] = kwargs.pop('redactor_settings')
        if 'in_admin' in kwargs:
            widget_kwargs['in_admin'] = kwargs.pop('in_admin')

        super(RedactorField, self).__init__(*args, **kwargs)
        
        # See if any of the keyword arguments to the constructor need to be
        # passed into the Widget.
        if widget_kwargs:
            # The parent class' (``CharField``) __init__ has made self.widget an
            # instance, we need the class again so we can re-instantiate it with
            # our own arguments.
            widget = kwargs.get('widget', None) or self.widget.__class__
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