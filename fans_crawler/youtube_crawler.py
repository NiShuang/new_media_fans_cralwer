# -*- coding: UTF-8 -*-
import urllib2
import re
import json
from selenium import webdriver
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.support.ui import WebDriverWait

def get_by_request():
    url = 'https://www.youtube.com/channel/UC3qWcF49rv8VMZO7Vg6kj5w'
    headers = {}
    headers['Host'] = 'www.youtube.com'
    headers['Referer'] = 'http://www.insta360.com/'
    # headers['User-Agent'] = 'Mozilla/5.0 (Windows NT 10.0; WOW64; rv:49.0) Gecko/20100101 Firefox/49.0'
    # headers['Accept'] = 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8'
    # headers['Connection'] = 'keep-alive'
    # headers['Upgrade-Insecure-Requests'] = '1'
    request = urllib2.Request(url = url, headers=headers)
    response = urllib2.urlopen(request)
    page = response.read()
    # print page
    pattern = re.compile("subscribers\">(.*)</span>  <span class=\"yt-subscription-button-disabled-mask\"", re.S)
    items = re.findall(pattern, page)
    fans = int(items[0])
    print fans
    return fans


def get_by_api():
    url = 'https://www.googleapis.com/youtube/v3/channels?part=statistics&id=UC3qWcF49rv8VMZO7Vg6kj5w&key=AIzaSyBg_mtqCgH3mhrTFPVOqDnNeN8wVVO_s5I'
    request = urllib2.Request(url = url)
    response = urllib2.urlopen(request)
    page = response.read()
    result = json.loads(page, encoding="utf-8")
    fans = int(result['items'][0]['statistics']['subscriberCount'])
    print fans
    return fans


def get_by_selenium():
    url = 'https://www.youtube.com/channel/UC3qWcF49rv8VMZO7Vg6kj5w'
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
        fans = int(wait.until(lambda x: x.find_elements_by_class_name('yt-subscription-button-subscriber-count-branded-horizontal')[0].text))
    except TimeoutException:
        fans = 0
    print fans
    driver.quit()
    return fans

if __name__ == "__main__":
    get_by_api()
    # get_by_selenium()
