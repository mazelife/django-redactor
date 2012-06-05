from urlparse import urljoin

from django.conf import settings
from django.forms import Media, Textarea
from django.utils.safestring import mark_safe
from django.utils import simplejson as json


class RedactorEditor(Textarea):
    """
    A widget that renders a <textarea> element as a Redactor rich tech editor.
    
    This widget has three additional keyword arguments that a typical ``Textarea``
    wiget does not. They are:
    
    ``redactor_settings`` - a dictionary of named settings and values. See the
    Redactor `API docs <http://redactorjs.com/docs/settings>`_ for available
    settings.
    
    ``redactor_css`` - a path to a CSS file to include in the editbale content 
    region of the widget. Paths used to specify media can be either relative or 
    absolute. If a path starts with '/', 'http://' or 'https://', it will be 
    interpreted as an absolute path, and left as-is. All other paths will be 
    prepended with the value of the ``STATIC_URL`` setting (or ``MEDIA_URL`` if
    static is not defined).
    
    `in_admin`` - set to ``True`` to configure redactor to work better in the Django
    admin.

    Example usage::

        >>> RedactorEditor(
                in_admin=True,
                redactor_css = 'styles/bodycopy.css',
                redactor_settings={
                    'lang': 'en',
                    'toolbar': 'default',
                    'load': True,
                    'path': False,
                    'focus': False,
                }
            )

    """

    script_tag = '<script>Redactor.register(%s);</script>'

    def __init__(self, attrs=None, in_admin=False, redactor_css=None, redactor_settings=None):
        super(RedactorEditor, self).__init__(attrs=attrs)
        default_settings = {
            'lang': 'en',
            'toolbar': 'default',
            'load': True,
            'path': False,
            'focus': False,
            'autoresize': True
        }
        self.redactor_settings = redactor_settings or default_settings
        self.redactor_settings['in_admin'] = in_admin
        self.in_admin = in_admin
        if redactor_css:
            self.redactor_settings['css'] = self.get_redactor_css_absolute_path(redactor_css)

    def get_redactor_css_absolute_path(self, path):
        if path.startswith(u'http://') or path.startswith(u'https://') or path.startswith(u'/'):
            return path
        else:
            if settings.STATIC_URL is None:
                prefix = settings.MEDIA_URL
            else:
                prefix = settings.STATIC_URL
            return urljoin(prefix, path)

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

        if self.redactor_settings['in_admin']:
            css['screen'].append('redactor/css/django_admin.css')
        return Media(css=css, js=js)

    def render(self, name, value, attrs=None):
        html_class_name = attrs.get('class', '')
        redactor_class = html_class_name and " redactor_content" or "redactor_content"
        html_class_name += redactor_class
        attrs['class'] = html_class_name
        html = super(RedactorEditor, self).render(name, value, attrs=attrs)
        html += self.script_tag % json.dumps(self.redactor_settings)
        return mark_safe(html)
