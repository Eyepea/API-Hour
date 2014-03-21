import collections
import functools
import re


Attrs = collections.namedtuple('Attrs', 'url method dynamic')


def rest(url, method):
    method = method.upper()
    assert method in ('GET', 'POST', 'PUT', 'DELETE'), method
    def wrapper(func):
        @functools.wraps(func)
        def wrapped(self, *args, **kwargs):
            return func(self, *args, **kwargs)
        wrapped.__rest__ = Attrs(url, method, False)
        return wrapped
    return wrapper


class Node:
    def __init__(self, resource=None):
        self.children = []
        self.resource = resource

    def find(self, part=None, *tail):
        variables = {}
        if not tail and part is None:
            if self.resource is not None:
                return resource, True
            else:
                return None, True
        for node in self.children:
            match, varname = node.match(part)
            if match:
                if varname is not None:
                    variables[varname] = part
                yield from node.find(*tail)


class Plain(Node):
    def __init__(self, name, resource=None):
        super().__init__(resource)
        self.name = name

    def match(self, part):
        return self.name == self.part, None


class Dyn:
    def __init__(self, varname, resource=None):
        super().__init__(resource)
        self.varname = varname

    def match(self, part):
        return True, self.varname


class Router:

    DYN = re.compile('^{([_a-zA-Z][_a-zA_Z0-9]*)}$')
    PLAIN = re.compile('^([_a-zA-Z][_a-zA_Z0-9]*)$')

    def __init__(self):
        self._table = {}

    def add_handler(self, handler):
        for name in dir(handler):
            val = getattr(handler, name)
            rest = getattr(val, '__rest__', None)
            if rest:
                self._table[(rest.url, rest.method)] = val

    def _parse_url(self, url):
        parts = url.split('/')

        for part in parts:
            match = self.DYN.match(part)
            if match is not None:
                name = match.group(1)
            else:
                match = self.PLAIN.match(part)
                if match is not None:
                    name = match.group(1)
                else:
                    raise RuntimeError("Bad url spec: {}".format(url))

    def match(self, url):
        for part in parts:
            
