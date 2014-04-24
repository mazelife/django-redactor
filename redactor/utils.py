try:
    import json
except ImportError:
    from django.utils import simplejson as json

from django.utils.functional import Promise
try:
    from django.utils.encoding import force_unicode
except ImportError:
    from django.utils.encoding import force_text as force_unicode

class LazyEncoder(json.JSONEncoder):
    """Encodes django's lazy i18n strings.
    Used to serialize translated strings to JSON, because
    simplejson chokes on it otherwise.
    http://khamidou.com/django-translation-in-json.html
    """
    def default(self, obj):
        if isinstance(obj, Promise):
            return force_unicode(obj)
        return obj

