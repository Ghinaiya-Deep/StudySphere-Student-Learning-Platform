"""
Tiny compatibility shim for the removed `cgi` stdlib module on Python 3.13+

This implements a minimal subset of the API Django 3.2 may import at startup
so the development server can run. It's a short-term workaround — prefer
running the project on Python 3.11 for full compatibility.
"""
from html import escape as html_escape
from urllib.parse import parse_qs

def parse_header(value):
    """Parse a Content-Type-like header into (main_value, params_dict).

    Example: 'text/html; charset=utf-8' -> ('text/html', {'charset': 'utf-8'})
    """
    if not value:
        return '', {}
    parts = [p.strip() for p in value.split(';')]
    main = parts[0]
    params = {}
    for p in parts[1:]:
        if '=' in p:
            k, v = p.split('=', 1)
            params[k.strip().lower()] = v.strip().strip('"')
    return main, params

class FieldStorage:
    """Very small stub of cgi.FieldStorage.

    This does not implement full form/file parsing. It's sufficient to avoid
    import-time failures in libraries that import FieldStorage but don't use
    its full functionality during normal page rendering in this project.
    """
    def __init__(self, *args, **kwargs):
        # Keep minimal attributes used by some codepaths
        self.value = None
        self.filename = None
        self.file = None

    def getvalue(self, *args, **kwargs):
        return self.value

    # Provide a dictionary-like interface in case someone treats it like one
    def __getitem__(self, key):
        raise KeyError(key)

    def __contains__(self, key):
        return False

# Re-export minimal helpers
escape = html_escape
parse_qs = parse_qs

__all__ = ['parse_header', 'FieldStorage', 'escape', 'parse_qs']
