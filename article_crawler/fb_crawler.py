# -*- coding: UTF-8 -*-
import urllib2
import json


def get_by_api():
    result = []
    app_id = '1598022290502419'
    app_secret = 'f0fc5a210b5531987cbc671a6c3d864f'
    access_token = app_id + '|' + app_secret
    username = 'Insta360VRVideoCamera'
    url = 'https://graph.facebook.com/' + username + '/posts?fields=shares,message,comments.limit(0).summary(true),likes.limit(0).summary(true),created_time,id,link&limit=100&access_token=' + access_token
    headers = {}
    headers['Host'] = 'graph.facebook.com'
    headers['Connection'] = 'keep-alive'
    headers['Upgrade-Insecure-Requests'] = '1'
    headers['Cache-Control'] = 'max-age=0'

    while True:
        request = urllib2.Request(url = url, headers = headers)
        response = urllib2.urlopen(request)
        page = response.read()
        # print page
        jsonData = json.loads(page, encoding="utf-8")
        data = jsonData['data']
        for item in data:
            message = item['message'] if item.has_key('message') else ''
            share = item['shares']['count'] if item.has_key('shares') else 0
            link = item['link'] if item.has_key('link') else ''
            temp = {
                'account': username,
                'message': message,
                'id': item['id'],
                'public_time': item['created_time'],
                'date': item['created_time'][:10],
                'share': share,
                'like': item['likes']['summary']['total_count'],
                'comment': item['comments']['summary']['total_count'],
                'link': link,
            }
            # print temp
            result.append(temp)
        if len(data) == 0:
            break
        paging = jsonData['paging'] if jsonData.has_key('paging') else {}
        url = paging['next'] if paging.has_key('next') else ''
    # print len(result)
    jsonResult = json.dumps(result)
    print  jsonResult
    return jsonResult

if __name__ == '__main__':
    get_by_api()