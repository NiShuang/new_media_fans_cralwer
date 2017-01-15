# -*- coding: UTF-8 -*-
import urllib2
import json
import datetime
import time


def get_by_api():
    username = 'insta360official'
    url = 'https://www.instagram.com/' + username + '/media/'
    now = time.mktime(datetime.date.today().timetuple())
    week_ago = now - (3600 * 24 * 7)
    today = datetime.datetime.now().strftime('%Y-%m-%d')
    like_total = 0
    comment_total = 0
    view_total = 0
    request = urllib2.Request(url = url)
    response = urllib2.urlopen(request)
    page = response.read()
    print page
    jsonData = json.loads(page, encoding="utf-8")
    data = jsonData['items']
    for item in data:
        temp = int(item['created_time'])
        if temp >= week_ago:
            like_total += int(item['likes']['count'])
            comment_total += int(item['comments']['count'])
            if item.has_key('video_views'):
                view_total += int(item['video_views'])

    result = {
        'platform': 'instagram',
        'date': today,
        'comment': comment_total,
        'like': like_total,
        'share': 0,
        'dislike': 0,
        'view': view_total
    }
    jsonResult = json.dumps(result)
    print  jsonResult
    return jsonResult


# def get_by_api():
#     # user_id = '3590979919'  #insta360
#     user_id = '3655666981'    #cielni
#     # oauth = OAuth()
#     access_token = '3655666981.a84f3a3.300f1e9a34fb4df4acad0b6100dcdc79'
#     url = 'https://api.instagram.com/v1/users/' + user_id + '/media/recent/?access_token=' + access_token
#     now = time.mktime(datetime.date.today().timetuple())
#     week_ago = now - (3600 * 24 * 7)
#     today = datetime.datetime.now().strftime('%Y-%m-%d')
#     like_total = 0
#     comment_total = 0
#     request = urllib2.Request(url = url)
#     response = urllib2.urlopen(request)
#     page = response.read()
#     print page
#     jsonData = json.loads(page, encoding="utf-8")
#     data = jsonData['data']
#     for item in data:
#         temp = int(item['created_time'])
#         if temp >= week_ago:
#             like_total += int(item['likes']['count'])
#             comment_total += int(item['comments']['count'])
#     result = {
#         'platform': 'instagram',
#         'date': today,
#         'comment': comment_total,
#         'like': like_total,
#         'share': 0,
#         'dislike': 0,
#         'view': 0
#     }
#     jsonResult = json.dumps(result)
#     print  jsonResult
#     return jsonResult



def OAuth():
    url = 'https://www.instagram.com/oauth/authorize/?client_id=a84f3a3ec8c44dfbbe9d2e3f07dc9c97&redirect_uri=http://www.baidu.com&response_type=token'
    request = urllib2.Request(url = url)
    response = urllib2.urlopen(request)
    redirect_url = response.geturl()
    request = urllib2.Request(url=redirect_url)
    response = urllib2.urlopen(request)
    redirect_url = response.geturl()
    print redirect_url
    # data = json.loads(page, encoding="utf-8")


def get_by_request():
    username = 'insta360official'
    url = 'https://query.yahooapis.com/v1/public/yql?q=select%20*%20from%20html%20where%20url%3D%22https%3A%2F%2Fwww.instagram.com%2F' + username + '%2F%22%20and%20xpath%3D%22%2Fhtml%2Fbody%2Fscript%5B1%5D%22&format=json'
    headers = {}
    headers['Host'] = 'query.yahooapis.com'
    headers['Connection'] = 'keep-alive'
    headers['Origin'] = 'https://livecounts.net'
    headers['Pragma'] = 'no-cache'
    headers['Referer'] = 'https://livecounts.net/instagram/cielni'
    headers['User-Agent'] = 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/54.0.2840.99 Safari/537.36'
    request = urllib2.Request(url=url, headers=headers)
    response = urllib2.urlopen(request)
    page = response.read()
    print page
    jsonData = json.loads(page, encoding="utf-8")
    content = jsonData['query']['results']['script']['content']
    print content
    content = content[21:-1]
    print content
    content = json.loads(content, encoding="utf-8")
    fans = content['entry_data']['ProfilePage'][0]['user']['followed_by']['count']
    print fans
if __name__ == "__main__":
    # OAuth()
    # get_by_request()
    get_by_api()
