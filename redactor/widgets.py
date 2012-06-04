from django.forms import Media, Textarea
from django.utils.safestring import mark_safe
from django.utils import simplejson as json


class RedactorEditor(Textarea):
    """
    A widget that renders a <textarea> element as a Redactor rich tech editor.

    It  an be configured via the ``redactor_settings`` keyword argument. See
    the `API docs <http://redactorjs.com/docs/settings>`_ for available
    settings::

        >>> RedactorEditor(redactor_settings={
            'lang': 'en',
            'toolbar': 'default',
            'load': True,
            'path': False,
            'focus': False,
        })

    """
    default_settings = {
        'lang': 'en',
        'toolbar': 'default',
        'load': True,
        'path': False,
        'focus': False,
        'autoresize': True
    }
    script_tag = '<script>Redactor.register(%s);</script>'

    def __init__(self, attrs=None, in_admin=False, redactor_settings=None):
        super(RedactorEditor, self).__init__(attrs=attrs)
        self.redactor_settings = redactor_settings
        self.in_admin = in_admin

    @property
    def media(self):
        js = (
            'redactor/jquery-1.7.min.js',
            'redactor/redactor.min.js',
            'redactor/setup.js',
        )
        css = {
            'screen': [
                'redactor/css/redactor.css',
            ]
        }

        if self.in_admin:
            css['screen'].append('redactor/css/django_admin.css')
        return Media(css=css, js=js)

    def render(self, name, value, attrs=None):
        html_class_name = attrs.get('class', '')
        redactor_class = html_class_name and " redactor_content" or "redactor_content"
        html_class_name += redactor_class
        attrs['class'] = html_class_name
        html = super(RedactorEditor, self).render(name, value, attrs=attrs)
        settings = self.redactor_settings or self.default_settings
        settings['in_admin'] = self.in_admin
        html += self.script_tag % json.dumps(settings)
        return mark_safe(html)
