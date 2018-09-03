# -*- coding: UTF-8 -*-
import urllib2
import json
import time
import datetime


def get_by_api():
    app_id = ''
    app_secret = ''
    access_token = app_id + '|' + app_secret
    username = 'Insta360VRVideoCamera'
    url = 'https://graph.facebook.com/' + username + '/posts?fields=shares,message,comments.limit(0).summary(true),likes.limit(0).summary(true),created_time,id,link&limit=100&access_token=' + access_token
    headers = {}
    headers['Host'] = 'graph.facebook.com'
    headers['Connection'] = 'keep-alive'
    headers['Upgrade-Insecure-Requests'] = '1'
    headers['Cache-Control'] = 'max-age=0'
    now = time.mktime(datetime.date.today().timetuple())
    week_ago = now - (3600 * 24 * 7)
    today = datetime.datetime.now().strftime('%Y-%m-%d')
    share_total = 0
    like_total = 0
    comment_total = 0
    while True:
        request = urllib2.Request(url = url, headers = headers)
        response = urllib2.urlopen(request)
        page = response.read()
        jsonData = json.loads(page, encoding="utf-8")
        data = jsonData['data']
        for item in data:
            share = item['shares']['count'] if item.has_key('shares') else 0
            temp = time.mktime(time.strptime(item['created_time'], "%Y-%m-%dT%H:%M:%S+0000"))
            if temp >= week_ago:
                share_total += int(share)
                like_total += int(item['likes']['summary']['total_count'])
                comment_total += int(item['comments']['summary']['total_count'])
        if len(data) == 0:
            break
        paging = jsonData['paging'] if jsonData.has_key('paging') else {}
        url = paging['next'] if paging.has_key('next') else ''
    result = {
        'platform': 'facebook',
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

if __name__ == '__main__':
    get_by_api()
