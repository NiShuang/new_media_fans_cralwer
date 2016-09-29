# -*- coding: UTF-8 -*-
import re
import urllib2
import time
from selenium import webdriver
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.support.ui import WebDriverWait

def get_by_selenium():
    username = 'insta360'
    url = 'http://weibo.cn/'+ username
    cap = webdriver.DesiredCapabilities.PHANTOMJS
    cap["phantomjs.page.settings.resourceTimeout"] = 1000
    cap["phantomjs.page.settings.loadImages"] = False
    cap["phantomjs.page.settings.localToRemoteUrlAccessEnabled"] = True
    cap["userAgent"] = "Mozilla/5.0 (Windows NT 6.1; WOW64; rv:47.0) Gecko/20100101 Firefox/47.0"
    cap["XSSAuditingEnabled"] = True
    cap["host"] = 'weibo.cn'
    # cap["cookie"] = '_T_WM=d2e28a98d3031cf98e282a29740b5f24; SUB=_2A2566MQNDeTxGeRJ7VYX8CzFyDmIHXVWEuxFrDV6PUJbkdAKLU_GkW1OqRtS_kr8ak-kdubq12_Bbpo41w..; gsid_CTandWM=4uona6911nQUejIzV9kdEbBcmf5'
    driver = webdriver.PhantomJS(desired_capabilities=cap,
                                      service_args=['--ignore-ssl-errors=true', '--ssl-protocol=any',
                                                    '--web-security=true'])
    # driver = webdriver.Chrome()
    driver.get('http://baidu.com')
    driver.add_cookie({'name': '_T_WM', 'value': 'd2e28a98d3031cf98e282a29740b5f24'})
    driver.add_cookie({'name': 'SUB', 'value': '_2A2566MQNDeTxGeRJ7VYX8CzFyDmIHXVWEuxFrDV6PUJbkdAKLU_GkW1OqRtS_kr8ak-kdubq12_Bbpo41w..'})
    driver.add_cookie({'name': 'gsid_CTandWM', 'value': '4uona6911nQUejIzV9kdEbBcmf5'})
    driver.get(url)

    wait = WebDriverWait(driver, 20)
    print driver.page_source
    try:
        result = int(
            wait.until(lambda x: x.find_element_by_xpath('/html/body/div[3]/div/a[2]').text[3:-1]))
    except TimeoutException:
        result = 0
    print result
    time.sleep(10)
    driver.quit()
    return result

if __name__ == "__main__":
    get_by_selenium()