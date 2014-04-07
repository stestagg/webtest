import collections


class Context(collections.MutableMapping):

    def __init__(self, parent=None):
        self.parent = parent
        self._items = dict()
        self._hidden_keys = set()

    def __getitem__(self, name):
        if name in self._items:
            return self._items[name]
        if name in self._hidden_keys or self.parent is None:
            raise KeyError(name)
        return self.parent[name]

    def __setitem__(self, name, value):
        self._items[name] = value

    def __delitem__(self, name):
        if name not in self:
            raise KeyError(name)
        if name in self._items:
            del self._items[name]
        self._hidden_keys.add(name)

    def _keys(self, seen=frozenset()):
        for key in self._items.keys():
            if key not in seen:
                yield key
                seen.add(key)
        seen.update(self._hidden_keys)
        if self.parent is not None:
            for key in self.parent._keys(seen):
                yield key

    def __iter__(self):
        return self._keys()

    def __len__(self):
        return len(self._keys)

    def new(self):
        return Context(self)