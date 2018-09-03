# -*- coding: UTF-8 -*-
import urllib2
import json
import ssl
import urllib
from functools import wraps


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


def get_by_api():
    username = 'insta360'
    url = 'https://api.twitter.com/1.1/users/show.json?include_entities=fasle&screen_name=' + username
    oauth = OAuth()
    headers = {}
    headers['Host'] = 'api.twitter.com'
    headers['X-Target-URI'] = 'https://api.twitter.com'
    headers['Content-Type'] = 'application/x-www-form-urlencoded'
    headers['Connection'] = 'keep-alive'
    headers['Authorization'] = oauth
    request = urllib2.Request(url = url, headers = headers)
    response = urllib2.urlopen(request)
    page = response.read()
    print page
    data = json.loads(page, encoding="utf-8")
    fans = data['followers_count']
    print fans
    return fans


def OAuth():
    ssl.wrap_socket = sslwrap(ssl.wrap_socket)
    url = 'https://api.twitter.com/oauth2/token'
    value = {}
    value['grant_type'] = 'client_credentials'
    value['client_id'] = ''
    value['client_secret'] = ''
    data = urllib.urlencode(value)
    request = urllib2.Request(url = url, data = data)
    response = urllib2.urlopen(request)
    page = response.read()
    data = json.loads(page, encoding="utf-8")
    result = data['token_type'] + ' ' + data['access_token']
    return result


def sslwrap(func):
    @wraps(func)
    def bar(*args, **kw):
        kw['ssl_version'] = ssl._PROTOCOL_NAMES
        return func(*args, **kw)
    return bar


if __name__ == "__main__":
    get_by_request()
    # get_by_api()
