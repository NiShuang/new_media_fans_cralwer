# -*- coding: UTF-8 -*-
import urllib2
import urllib
import json
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
    def main(self):
        self.get_video_ids()
        return self.get_videos_info()

    def get_video_ids(self):
        url = self.list_api
        # print url
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

        # print len(self.video_ids)


    def get_videos_info(self):
        result = []
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
                # print results.url
                # print page
                videos = json.loads(page, encoding="utf-8")['items']
                for video in videos:
                    try:
                        like_count = video['statistics']['likeCount']
                    except KeyError:
                        like_count = 0
                    try:
                        dislike_count = video['statistics']['dislikeCount']
                    except KeyError:
                        dislike_count = 0
                    temp = {
                        'account': video['snippet']['channelTitle'],
                        'title': video['snippet']['title'],
                        'id': video['id'],
                        'public_time': video['snippet']['publishedAt'],
                        'date': video['snippet']['publishedAt'][:10],
                        'view': video['statistics']['viewCount'],
                        'like': like_count,
                        'dislike': dislike_count,
                        'favorite': video['statistics']['favoriteCount'],
                        'comment': video['statistics']['commentCount'],
                        'link': 'https://www.youtube.com/watch?v=' + video['id'],
                    }
                    result.append(temp)
                    query = ''
        # print len(result)
        jsonResult = json.dumps(result)
        print  jsonResult
        return jsonResult


if __name__ == "__main__":
    c = YoukuCrawler()
    c.main()