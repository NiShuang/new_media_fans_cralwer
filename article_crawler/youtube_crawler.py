# -*- coding: UTF-8 -*-
import urllib2
import time
import json
import datetime
import requests


class YoukuCrawler:
    def __init__(self):
        self.video_ids = []
        self.maxResults = 50
        playlist_id = 'UU3qWcF49rv8VMZO7Vg6kj5w'
        self.app_key = 'AIzaSyBg_mtqCgH3mhrTFPVOqDnNeN8wVVO_s5I'
        self.list_api = 'https://www.googleapis.com/youtube/v3/playlistItems?maxResults=' + str(self.maxResults) + '&part=snippet&playlistId=' + playlist_id + '&key=' + self.app_key
        # self.info_api = 'https://www.googleapis.com/youtube/v3/videos?maxResults=50&part=snippet,statistics' + '&key=' + self.app_key
        self.info_api = 'https://www.googleapis.com/youtube/v3/videos'
        now = time.mktime(datetime.date.today().timetuple())
        self.week_ago = now - (3600 * 24 * 7)
        self.view_total = 0
        self.like_total = 0
        self.dislike_total = 0
        self.comment_total = 0
    def main(self):
        self.get_video_ids()
        return self.get_videos_info()

    def get_video_ids(self):
        url = self.list_api
        request = urllib2.Request(url=url)
        response = urllib2.urlopen(request)
        page = response.read()
        result = json.loads(page, encoding="utf-8")
        # total = int(result['pageInfo']['totalResults'])
        # perPage = int(result['pageInfo']['resultsPerPage'])
        # self.totalPage = (total/perPage) + (0 if (total%perPage)==0 else 1)
        videos = result['items']
        for video in videos:
            self.video_ids.append(video['snippet']['resourceId']['videoId'])

        while(result.has_key('nextPageToken')):
            url = self.list_api + '&pageToken=' + result['nextPageToken']
            request = urllib2.Request(url=url)
            response = urllib2.urlopen(request)
            page = response.read()
            result = json.loads(page, encoding="utf-8")
            videos = result['items']
            for video in videos:
                self.video_ids.append(video['snippet']['resourceId']['videoId'])


    def get_videos_info(self):
        url = self.info_api
        query = ''
        count = 0
        for i in self.video_ids:
            count += 1
            query = query + i + ','
            if count % self.maxResults == 0 or count == len(self.video_ids):
                query = query[:-1]
                results = requests.get(url,
                               params={'id': query, 'maxResults': self.maxResults, 'part': 'snippet,statistics', 'key': self.app_key})
                page = results.content
                videos = json.loads(page, encoding="utf-8")['items']
                for video in videos:
                    try:
                        like_count = int(video['statistics']['likeCount'])
                    except KeyError:
                        like_count = 0
                    try:
                        dislike_count = int(video['statistics']['dislikeCount'])
                    except KeyError:
                        dislike_count = 0
                    temp = time.mktime(time.strptime(video['snippet']['publishedAt'], "%Y-%m-%dT%H:%M:%S.000Z"))
                    if temp >= self.week_ago:
                        self.dislike_total += dislike_count
                        self.like_total += like_count
                        self.comment_total += int(video['statistics']['commentCount'])
                        self.view_total += int(video['statistics']['viewCount'])
                    query = ''
        today = datetime.datetime.now().strftime('%Y-%m-%d')
        result = {
            'platform': 'youtube',
            'date': today,
            'comment': self.comment_total,
            'like': self.like_total,
            'share': 0,
            'dislike': self.dislike_total,
            'view': self.view_total
        }
        jsonResult = json.dumps(result)
        print  jsonResult
        return jsonResult

if __name__ == "__main__":
    c = YoukuCrawler()
    c.main()