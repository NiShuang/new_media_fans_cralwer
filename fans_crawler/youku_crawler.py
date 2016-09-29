# -*- coding: UTF-8 -*-
import urllib2
import re
import json
from selenium import webdriver
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.support.ui import WebDriverWait

def get_by_request():
    url = 'http://i.youku.com/i/UMjk1ODg3NDgwOA=='
    headers = {}
    headers['Host'] = 'i.youku.com'
    headers['Referer'] = 'http://www.insta360.com/'
    headers['User-Agent'] = 'Mozilla/5.0 (Windows NT 10.0; WOW64; rv:49.0) Gecko/20100101 Firefox/49.0'
    # headers['Accept'] = 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8'
    # headers['Connection'] = 'keep-alive'
    headers['Upgrade-Insecure-Requests'] = '1'
    request = urllib2.Request(url = url, headers=headers)
    response = urllib2.urlopen(request)
    page = response.read()
    # print page
    pattern = re.compile("<li class=\"splite\"></li><li class=\"snum\" title=\"(.{0,10})\"><em>", re.S)
    items = re.findall(pattern, page)
    fans = int(items[0])
    print fans
    return fans

def get_by_api():
    url = 'https://openapi.youku.com/v2/users/friendship/followers.json?client_id=b10ab8588528b1b1&user_id=UMjk1ODg3NDgwOA=='
    request = urllib2.Request(url = url)
    response = urllib2.urlopen(request)
    page = response.read()
    result = json.loads(page, encoding="utf-8")
    fans = int(result['total'])
    print fans
    return fans

def get_by_selenium():
    url = 'http://i.youku.com/i/UMjk1ODg3NDgwOA=='
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
    print driver.page_source
    try:
        fans = int(wait.until(lambda x: x.find_elements_by_class_name('snum')[0].find_element_by_xpath('em').text))
    except TimeoutException:
        fans = 0
    print fans
    driver.quit()
    return fans

if __name__ == "__main__":
    get_by_api()
    # get_by_selenium()
