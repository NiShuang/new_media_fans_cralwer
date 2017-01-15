# -*- coding: UTF-8 -*-
import urllib
import urllib2
import datetime
import time
import json
import requests
import base64
from selenium import webdriver
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.support.ui import WebDriverWait

# def get_by_api():
#     url = 'https://api.weibo.com/2/statuses/user_timeline.json'
#     access_token= oauth()
#     value = {}
#     value['trim_user'] = '1'
#     value['count'] = '100'
#     value['access_token'] = access_token
#     data = urllib.urlencode(value)
#     results = requests.get(url=url, params=data)
#     page = results.content
#     print page
#
# def oauth():
#     url = 'https://api.weibo.com/oauth2/access_token'
#     value = {}
#     value['client_id'] = '2397089507'
#     value['redirect_uri'] = 'http://www.baidu.com'
#     value['client_secret'] = '59a24c6051d6fdbb144a5b9e4f15b0d1'
#     value['grant_type'] = 'authorization_code'
#     value['code'] = '90b5cd7549e8461fdef063828eee498c'
#     data = urllib.urlencode(value)
#     results = requests.post(url=url, params=data)
#     print results.content
#     data = json.loads(results.content, encoding="utf-8")
#     ## 需要判断返回是否正常
#     access_token = data['access_token']
#     return access_token

def get_by_api():
    url = 'https://api.weibo.com/2/statuses/user_timeline.json?page=1'
    username = 'newmedia@vzhibo.tv'
    password = 'lanfeng123'
    value = {}
    value['trim_user'] = '1'
    value['count'] = '100'
    value['source'] = '218121934'
    data = urllib.urlencode(value)
    base64string = base64.encodestring(
        '%s:%s' % (username, password))[:-1]  # 注意哦，这里最后会自动添加一个\n
    authheader = "Basic %s" % base64string
    header = {}
    header['Authorization'] = authheader
    now = time.mktime(datetime.date.today().timetuple())
    week_ago = now - (3600 * 24 * 7)
    today = datetime.datetime.now().strftime('%Y-%m-%d')
    share_total = 0
    like_total = 0
    comment_total = 0
    results = requests.get(url=url, params=data, headers=header)
    page = results.content
    print page
    jsonData = json.loads(page, encoding="utf-8")
    data = jsonData['statuses']
    for item in data:
        temp = time.mktime(time.strptime(item['created_at'], "%a %b %d %H:%M:%S +0800 %Y"))
        if temp >= week_ago:
            share_total += int(item['reposts_count'])
            like_total += int(item['attitudes_count'])
            comment_total += int(item['comments_count'])
    result = {
        'platform': 'weibo',
        'date': today,
        'comment': comment_total,
        'like': like_total,
        'share': share_total,
        'dislike': 0,
        'view': 0
    }
    jsonResult = json.dumps(result)
    print  jsonResult
    return jsonResult

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
    get_by_api()