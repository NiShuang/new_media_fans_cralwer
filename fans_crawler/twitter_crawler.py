# -*- coding: UTF-8 -*-
import urllib2
import json


def get_by_request():
    username = 'insta360'
    url = 'https://cdn.syndication.twimg.com/widgets/followbutton/info.json?screen_names=' + username
    # headers = {}
    # headers['Host'] = 'www.facebook.com'
    # headers['User-Agent'] = 'Mozilla/5.0 (Windows NT 10.0; WOW64; rv:49.0) Gecko/20100101 Firefox/49.0'
    # headers['Accept'] = 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8'
    # headers['Connection'] = 'keep-alive'
    # headers['Upgrade-Insecure-Requests'] = '1'
    request = urllib2.Request(url = url)
    response = urllib2.urlopen(request)
    page = response.read()
    result = json.loads(page, encoding="utf-8")
    fans = result[0]['followers_count']
    print fans
    return fans


if __name__ == "__main__":
    get_by_request()
