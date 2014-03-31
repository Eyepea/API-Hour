import collections


class _ReadonlyDict(collections.Mapping):

    __slots__ = ('_data',)

    def __init__(self, data):
        self._data = dict(data)

    def __getitem__(self, name):
        return self._data[name]

    def __len__(self):
        return len(self._data)

    def __iter__(self):
        return iter(self._data)

    def __repr__(self):
        return '<{} {!r}>'.format(self.__class__.__name__, self._data)
