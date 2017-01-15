# -*- coding: UTF-8 -*-
import re
import urllib2
import json
from selenium import webdriver
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.support.ui import WebDriverWait
import ssl
from functools import wraps


def get_by_api():
    app_id = '1598022290502419'
    app_secret = 'f0fc5a210b5531987cbc671a6c3d864f'
    access_token = app_id + '|' + app_secret
    username = 'Insta360VRVideoCamera'
    url = 'https://graph.facebook.com/' + username + '/?fields=fan_count&access_token=' + access_token
    headers = {}
    headers['Host'] = 'graph.facebook.com'
    headers['Connection'] = 'keep-alive'
    headers['Upgrade-Insecure-Requests'] = '1'
    headers['Cache-Control'] = 'max-age=0'

    request = urllib2.Request(url = url, headers = headers)
    response = urllib2.urlopen(request)
    page = response.read()
    # print page
    jsonData = json.loads(page, encoding="utf-8")
    fans = jsonData['fan_count']
    print fans
    return fans


def sslwrap(func):
    @wraps(func)
    def bar(*args, **kw):
        kw['ssl_version'] = ssl._PROTOCOL_NAMES
        return func(*args, **kw)
    return bar


def get_by_request():
    ssl.wrap_socket = sslwrap(ssl.wrap_socket)
    username = 'Insta360VRVideoCamera'
    url = 'https://www.facebook.com/plugins/fan.php?id=' + username
    headers = {}
    headers['Host'] = 'www.facebook.com'
    # headers['User-Agent'] = 'Mozilla/5.0 (Windows NT 10.0; WOW64; rv:49.0) Gecko/20100101 Firefox/49.0'
    # headers['Accept'] = 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8'
    # headers['Connection'] = 'keep-alive'
    # headers['Upgrade-Insecure-Requests'] = '1'
    request = urllib2.Request(url = url,headers=headers)
    response = urllib2.urlopen(request)
    page = response.read()
    pattern = re.compile("<div class=\"_1drq\" style=\"max-width: 220px;\">(.{0,10})\s", re.S)
    items = re.findall(pattern, page)
    # print page.decode("UTF-8")
    fans = int(items[0].replace(',',''))
    print fans
    return fans


def get_by_selenium():
    username = 'Insta360VRVideoCamera'
    url = 'https://www.facebook.com/plugins/fan.php?id=' + username
    cap = webdriver.DesiredCapabilities.PHANTOMJS
    cap["phantomjs.page.settings.resourceTimeout"] = 1000
    cap["phantomjs.page.settings.loadImages"] = False
    cap["phantomjs.page.settings.localToRemoteUrlAccessEnabled"] = True
    cap["userAgent"] = "Mozilla/5.0 (Windows NT 6.1; WOW64; rv:47.0) Gecko/20100101 Firefox/47.0"
    cap["XSSAuditingEnabled"] = True
    driver = webdriver.PhantomJS(desired_capabilities=cap,
                                      service_args=['--ignore-ssl-errors=true', '--ssl-protocol=any',
                                                    '--web-security=true'])
    # driver = webdriver.Chrome()
    driver.get(url)
    wait = WebDriverWait(driver, 20)
    # print driver.page_source
    try:
        string = wait.until(lambda x: x.find_elements_by_class_name('_1drq')[0].text)
    except TimeoutException:
        string = 0
    pattern = re.compile("\d", re.S)
    items = re.findall(pattern, string)
    temp = ''
    for item in items:
        temp += item
    fans = int(temp)
    print fans
    driver.quit()
    return fans

if __name__ == "__main__":
    # get_by_request()
    # get_by_selenium()
    get_by_api()