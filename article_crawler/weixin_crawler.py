# -*- coding: UTF-8 -*-
import urllib2
import urllib
import json
import time
import datetime


def get_by_request():
    username = 'Insta360_official'
    url = 'http://www.newrank.cn/xdnphb/detail/getAccountArticle'
    headers = {}
    headers['Host'] = 'www.newrank.cn'
    headers['Referer'] = 'http://www.newrank.cn/public/info/detail.html?account=' + username
    headers['Cookie'] = 'userFaceTip=userFaceTip; CNZZDATA1253878005=1419576409-1475115174-%7C1475115174; Hm_lvt_a19fd7224d30e3c8a6558dcb38c4beed=1475116869; Hm_lpvt_a19fd7224d30e3c8a6558dcb38c4beed=1475116869; userFaceTip=userFaceTip'
    headers['User-Agent'] = 'Mozilla/5.0 (Windows NT 10.0; WOW64; rv:49.0) Gecko/20100101 Firefox/49.0'
    headers['X-Requested-With'] = 'XMLHttpRequest'
    headers['Content-Type'] = 'application/x-www-form-urlencoded; charset=UTF-8'

    value = {}
    value['flag'] = 'true'
    value['uuid'] = '91B514A33A4D2FA4C1E923ABDA595A90'
    value['nonce'] = '3679c0e73'
    value['xyz'] = '6cdb1d7fbdeea8afe76a21479f46f0b2'
    data = urllib.urlencode(value)
    request = urllib2.Request(url = url,data = data, headers = headers)
    response = urllib2.urlopen(request)
    page = response.read()
    now = time.mktime(datetime.date.today().timetuple())
    week_ago = now - (3600 * 24 * 7)
    today = datetime.datetime.now().strftime('%Y-%m-%d')
    like_total = 0
    view_total = 0
    result = json.loads(page, encoding="utf-8")
    articles = result['value']['lastestArticle']
    for article in articles:
        temp = time.mktime(time.strptime(article['publicTime'], "%Y-%m-%d %H:%M:%S"))
        if temp >= week_ago:
            view_total += int(article['clicksCount'])
            like_total += int(article['likeCount'])
    result = {
        'platform': 'weixin',
        'date': today,
        'comment': 0,
        'like': like_total,
        'share': 0,
        'dislike': 0,
        'view': view_total
    }
    jsonResult = json.dumps(result)
    print  jsonResult
    return jsonResult

if __name__ == '__main__':
    get_by_request()