import webtest.webdriver.drivers.remote as remote

dd = remote.Driver(port=9515)

with dd.session() as session:
    session.url = "http://www.google.com"
    #session.execute_js("alert('hi')")
    print list(session.cookies)
    print session.cookies["PREF"]
