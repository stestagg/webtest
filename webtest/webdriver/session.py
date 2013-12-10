import base64
import functools
import json

import requests

import webtest.webdriver.window
import webtest.webdriver.cookies


def setter(func):
    return property(None, func)


def simple_action(name):
    def action(self):
        return self._send("POST", name)
    action.__name__ = name
    return action


def simple_get(name):
    def get(self):
        return self._send("GET", name)
    get.__name__ = name
    return property(get)


def json_default(obj):
    print "!!!!", obj
    raise TypeError()



FIND_USING_MAP = {
    "class": "class name",
    "css": "css selector",
}


def named_finder(name):
    def finder(self, value):
        return self._find(name, value)
    finder.__name__ = "by_" + name
    return finder


class ElementFinder(object):

    def _find(self, using, value):
        self._send("POST", "element", using=using, value=value)

for name in ["css", "class", "id", "name", "tag", "xpath"]:
    setattr(ElementFinder, "by_" + name, named_finder(name)



class Session(object):

    def __init__(self, driver, session_id):
        self.driver = driver
        self.session_id = session_id
        try:
            self.implicit_timeout = 5 # Set the implicit timeout low because of built-in retry
        except:
            pass

    # Webdriver protocol implementation and helpers
    def _send(self, method, *path, **data):
        url = "%s/%s" % (self.driver.base_address,
                          "/".join(("session", self.session_id) + path))
        headers = {}
        if method == "GET":
            assert len(data) == 0
            body = None
        else:
            body = json.dumps(data, default=json_default)
            headers['Content-type'] = 'application/json'
            headers['Accept'] = 'application/json'
        response = getattr(requests, method.lower())(url, data=body, headers=headers).json()
        assert response["sessionId"] == self.session_id
        assert response["status"] == 0, response
        return response.get("value")

    def stop(self):
        self._send("DELETE")

    @property
    def url(self):
        return self._send("GET", "url")

    @url.setter
    def url(self, url):
        return self._send("POST", "url", url=url)

    @setter
    def page_load_timeout(self, value):
        return self._send("POST", "timeouts", type="page load", ms=value)

    @setter
    def script_timeout(self, value):
        return self._send("POST", "timeouts", type="script", ms=value)

    @setter
    def implicit_timeout(self, value):
        return self._send("POST", "timeouts", type="implicit", ms=value)

    @property
    def window(self):
        return webtest.webdriver.window.Window(self, self._send("GET", "window_handle"))

    @window.setter
    def window(self, value):
        if hasattr(value, "window_handle"):
            value = value.window_handle
        return self._send("POST", "window", name=value)

    @property
    def windows(self):
        handles = self._send("GET", "window_handles")
        return [webtest.webdriver.window.Window(self, id) for id in handles]

    @property
    def cookies(self):
        return webtest.webdriver.cookies.Cookies(self)

    back = simple_action("back")
    forward = simple_action("forward")
    refresh = simple_action("refresh")
    source = simple_get("source")
    title = simple_get("title")

    def execute_js(self, js, args=(), async=False):
        method = "execute_async" if async else "execute"
        return self._send("POST", method, script=js, args=args)

    def screenshot(self, save_to_file=None):
        screenshot = self._send("GET", "screenshot")
        png_data = base64.b64decode(screenshot)
        if save_to_file:
            if hasattr(save_to_file, "write"):
                save_to_file.write(png_data)
            else:
                with open(save_to_file, "wb") as fh:
                    fh.write(png_data)
        return png_data