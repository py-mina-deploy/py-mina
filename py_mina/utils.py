"""
Utilities
"""


class _ConfigAttributeDict(dict):
    """
    Dictionary subclass enabling attribute lookup/assignment of keys/values.
    For example::
        >>> m = _ConfigAttributeDict({'foo': 'bar'})
        >>> m.foo
        'bar'
        >>> m.foo = 'not bar'
        >>> m['foo']
        'not bar'
    ``_ConfigAttributeDict`` objects also provide ``.first()`` which acts like
    ``.get()`` but accepts multiple keys as arguments, and returns the value of
    the first hit, e.g.::
        >>> m = _ConfigAttributeDict({'foo': 'bar', 'biz': 'baz'})
        >>> m.first('wrong', 'incorrect', 'foo', 'biz')
        'bar'
    """

    def __getattr__(self, key):
        try:
            return self[key]
        except KeyError:
            # to conform with __getattr__ spec
            raise AttributeError(key)


    def __setattr__(self, key, value):
        self[key] = value


    def first(self, *names):
        for name in names:
            value = self.get(name)

            if value:
                return value


class _StateAttributeDict(dict):
    """
    Dictionary subclass enabling attribute lookup/assignment of keys/values.
    For example::
        >>> m = _StateAttributeDict({'foo': 'bar'})
        >>> m.foo
        'bar'
        >>> m.foo = 'not bar'
        >>> m['foo']
        'not bar'
    ``_StateAttributeDict`` objects also provide ``.succeeded([str])`` 
    """

    def __getattr__(self, key):
        try:
            return self[key]
        except KeyError:
            # to conform with __getattr__ spec
            raise AttributeError(key)


    def __setattr__(self, key, value):
        self[key] = value


    def succeeded(self, state_keys=[]):
        if len(state_keys) == 0: return False

        return all(state_keys.map(lambda x: self.get(x) == True))