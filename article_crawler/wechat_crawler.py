# -*- coding: UTF-8 -*-
import urllib2
import urllib
import json


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
    # headers['Accept'] = 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8'
    # headers['Connection'] = 'keep-alive'

    value = {}
    value['uuid'] = '91B514A33A4D2FA4C1E923ABDA595A90'
    value['nonce'] = '3679c0e73'
    value['xyz'] = '6cdb1d7fbdeea8afe76a21479f46f0b2'
    data = urllib.urlencode(value)
    request = urllib2.Request(url = url,data = data, headers = headers)
    response = urllib2.urlopen(request)
    page = response.read()
    # print page
    result = json.loads(page, encoding="utf-8")
    articles = result['value']['lastestArticle']
    result = []
    for article in articles:
        temp = {
            'account': article['account'],
            'title': article['title'],
            'id': article['messageId'],
            'public_time': article['publicTime'],
            'date': article['publicTime'][:10],
            'view': article['clicksCount'],
            'like': article['likeCount'],
            'link': article['url'],
        }
        result.append(temp)
    jsonResult = json.dumps(result)
    print  jsonResult
    return jsonResult

if __name__ == '__main__':
    get_by_request()