1import copy
import contextlib
import requests
import json

import fin.module

import webtest.webdriver.session

OPTIONAL = "optional"
REQUIRED = "required"


class Driver(object):

    NAME = NotImplemented

    OPTIONAL = OPTIONAL
    REQUIRED = REQUIRED
    DEFAULT_FEATURES = {
        "javascriptEnabled": REQUIRED,
        "takesScreenshot": REQUIRED,
        "cssSelectorsEnabled": REQUIRED,
    }

    @classmethod
    def get_children(cls):
        fin.module.import_child_modules(["webtest", "drivers"])

    def __init__(self, *args, **kwargs):
        self.features = copy.deepcopy(self.DEFAULT_FEATURES)
        self._server_started = False


    def get_capabilities(self):
        optional = {}
        required = {}
        for key, value in self.features.iteritems():
            if value is OPTIONAL:
                optional[key] = value
            else:
                required[key] = value
        return optional, required

    # Should be defined by implementation-specific subclasses
    def _start_server(self, *args, **kwargs):
        raise NotImplementedError("_start_server")

    def _stop_server(self, *args, **kwargs):
        raise NotImplementedError("_stop_server")

    @property
    def base_address(self):
        raise NotImplementedError()

    @contextlib.contextmanager
    def _server(self):
        if self._server_started:
            yield
        else:
            self._start_server()
            self._server_started = True
            try:
                yield
            finally:
                self._stop_server()

    @contextlib.contextmanager
    def session(self):
        with self._server():
            session = self._start_session()
            try:
                yield session
            finally:
                session.stop()

    def _start_session(self):
        desired, required = self.get_capabilities()
        data = json.dumps({"desiredCapabilities": desired, "requiredCapabilities": required})
        headers = {'Content-type': 'application/json', 'Accept': 'application/json'}
        response = requests.post(self.base_address + "/session", data=data, headers=headers)
        # TODO: error handling (and error strategies)
        data = response.json()
        assert data["status"] == 0, data
        return webtest.webdriver.session.Session(self, data["sessionId"])
