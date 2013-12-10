
class Window(object): # Friend: Session

    def __init__(self, session, window_handle):
        self.window_handle = window_handle
        self.session = session

    def _send(self, method, *args, **kwargs):
        return self.session._send(method, "window", self.window_handle, *args, **kwargs)

    @property
    def size(self):
        return self._send("GET", "size")

    @size.setter
    def size(self, value):
        assert hasattr(value, "items")
        return self._send("POST", "size", **value)

    @property
    def position(self):
        return self._send("GET", "position")

    @position.setter
    def position(self, value):
        assert hasattr(value, "items")
        return self._send("POST", "position", **value)

    def maximize(self):
        return self._send("POST", "maximize")

    def focus(self):
        return self.session._send("POST", "window", name=self.window_handle)

    def close(self):
        self.focus()
        return self.session._send("DELETE", "window")