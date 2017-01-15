# -*- coding: UTF-8 -*-
import urllib2
import json
import ssl
import urllib


def get_by_api():
    url = 'https://api.weixin.qq.com/cgi-bin/user/get'
    token = get_token()
    value = {}
    value['access_token'] = token
    value['next_openid'] = ''
    data = urllib.urlencode(value)
    request = urllib2.Request(url = url, data = data)
    response = urllib2.urlopen(request)
    page = response.read()
    print page
    data = json.loads(page, encoding="utf-8")
    fans = 0
    try:
        fans = data['total']
    except KeyError:
        pass
    print fans
    return fans


def get_token():
    url = 'https://api.weixin.qq.com/cgi-bin/token'
    value = {}
    value['grant_type'] = 'client_credential'
    value['appid'] = 'wxa01ae38d52e5b020'
    value['secret'] = 'c19d7334e7e6be29888d2ed728972318'
    data = urllib.urlencode(value)
    request = urllib2.Request(url = url, data = data)
    response = urllib2.urlopen(request)
    page = response.read()
    print page
    data = json.loads(page, encoding="utf-8")
    result = ''
    try:
        result = data['access_token']
    except KeyError:
        pass
    return result

if __name__ == "__main__":
    get_by_api()