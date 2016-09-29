# -*- coding: UTF-8 -*-
import re
import urllib2
from selenium import webdriver
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.support.ui import WebDriverWait

def get_by_request():
    username = 'insta360'
    url = 'http://weibo.cn/'+ username
    headers = {}
    headers['Host'] = 'weibo.cn'
    headers['User-Agent'] = 'Mozilla/5.0 (Windows NT 10.0; WOW64; rv:49.0) Gecko/20100101 Firefox/49.0'
    # headers['Accept'] = 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8'
    headers['Cookie'] = '_T_WM=d2e28a98d3031cf98e282a29740b5f24'
    # headers['Connection'] = 'keep-alive'
    # headers['Upgrade-Insecure-Requests'] = '1'
    request = urllib2.Request(url = url, headers=headers)
    response = urllib2.urlopen(request)
    page = response.read()
    pattern = re.compile("\[(.{0,10})\]</a>&nbsp;<a href=", re.S)
    items = re.findall(pattern, page)
    # print page.decode("UTF-8")
    fans = int(items[1])
    print fans
    return fans


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
    cap["cookie"] = 'UOR=www.umeng.com,widget.weibo.com,www.insta360.com; SINAGLOBAL=6982249232630.452.1472299450582; ULV=1475028466086:3:2:2:8231266012653.427.1475028466020:1474966940284; SUB=_2AkMgtrrUf8NhqwJRmP0czWrmZY53wgjEieLBAH7sJRMxHRl-yT83qm8AtRCo0NEVwCee4iQkVabYZqZ8gEhMng..; SUBP=0033WrSXqPxfM72-Ws9jqgMF55529P9D9WWT6ckK7WZ-8GkEahm6SKw1; TC-Page-G0=0cd4658437f38175b9211f1336161d7d; _s_tentry=-; Apache=8231266012653.427.1475028466020'
    driver = webdriver.PhantomJS(desired_capabilities=cap,
                                      service_args=['--ignore-ssl-errors=true', '--ssl-protocol=any',
                                                    '--web-security=true'])
    # driver = webdriver.Chrome()
    driver.get(url)
    wait = WebDriverWait(driver, 20)
    # print driver.page_source
    try:
        result = int(
            wait.until(lambda x: x.find_element_by_xpath('/html/body/div[3]/div/a[2]').text[3:-1]))
    except TimeoutException:
        result = 0
    print result
    driver.quit()
    return result

if __name__ == "__main__":
    get_by_request()
    get_by_selenium()