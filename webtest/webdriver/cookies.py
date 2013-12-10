import collections


class Cookie(collections.MutableMapping):

    def __init__(self, cookies, data):
        self.cookies = cookies
        self.data = data.copy()

    def __getitem__(self, name):
        return self.data[name]

    def __setitem__(self, name, value):
        rv = super(Cookie, self).__setitem__(name, value)
        self.cookies._update(self)
        return rv

    def __iter__(self):
        return iter(self.data)

    def __len__(self):
        return len(self.data)

    def __eq__(self, other):
        if isinstance(other, dict):
            return self.data == other
        else:
            return self.data == other.data

    def __delitem__(self, key):
        del self.data[key]
        self.cookies._update(self)

    def __repr__(self):
        return "<Cookie: %r>" % (self.data, )


class Cookies(collections.MutableSet):

    def __init__(self, session):
        self.session = session

    def _send(self, method, *args, **kwargs):
        return self.session._send(method, *args, **kwargs)

    @property
    def _cookies(self):
        return self._send("GET", "cookie")

    def __contains__(self, cookie):
        for item in self:
            if cookie == item:
                return True
        return False

    def __iter__(self):
        return (Cookie(self, data) for data in self._cookies)

    def __len__(self):
        return len(self._cookies)

    def __getitem__(self, name):
        for item in self:
            if item.get("name") == name:
                return item
        raise KeyError(name)

    def add(self, value):
        if isinstance(value, Cookie):
            if value.cookies is not self:
                value = Cookie(self, value.data)
        else:
            value = Cookie(self, value)
        self._update(self, value)

    def discard(self, value):
        for item in self:
            if item == value:
                self._send("DELETE", "cookie", item["name"])

    def _update(self, cookie):
        self._send("POST", "cookie", cookie=cookie)

    def clear(self):
        self._send("DELETE", "cookie")