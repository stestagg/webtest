import webtest.webdriver.driver

class Driver(webtest.webdriver.driver.Driver):

    NAME = "Remote"

    def __init__(self, *args, **kwargs):
        super(Driver, self).__init__(*args, **kwargs)
        self._host = None
        self._port = None

    def _start_server(self, host="localhost", port=9515):
        self._host = host
        self._port = port

    def _stop_server(self):
        pass

    @property
    def base_address(self):
        if self._host is None or self._port is None:
            raise Exception("Server not configured")
        return "http://%s:%s" % (self._host, self._port)

