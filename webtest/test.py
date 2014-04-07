import webtest.webdriver.drivers.phantom as phantom

dd = phantom.Driver(port=9515)


with dd.session() as session:
    session.url = "http://www.google.com"
    print  session.by_id("gs_id0").by_id("gs_tti0").by_id("gbqfq")
    tds = session.by_tag("td", all=True)
    print session.execute_js("return arguments[0];", tds)
    import time; time.sleep(10)