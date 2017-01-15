import datetime
import json

from fb_crawler import get_by_api as get_fb
from weibo_crawler_old import get_by_api as get_sina
from twitter_crawler import get_by_api as get_twitter
from youtube_crawler import YoukuCrawler
from youku_crawler import get_by_api as get_youku
from weixin_crawler import get_by_request as get_weixin
from instagram_crawler import get_by_api as get_instagram

def main():
    platform = ['facebook', 'weibo', 'twitter', 'youtube', 'youku', 'weixin', 'instagram']
    result = []
    for i in platform:
        data = '{}'

        if i == 'facebook':
            data = get_fb()
        elif i == 'weibo':
            data = get_sina()
        elif i == 'twitter':
            data = get_twitter()
        elif i == 'youtube':
            c = YoukuCrawler()
            data = c.get_videos_info()
        elif i == 'youku':
            data = get_youku()
        elif i == 'weixin':
            data = get_weixin()
        elif i == 'instagram':
            data = get_instagram()

        data = json.loads(data)
        today = datetime.datetime.now().strftime('%Y-%m-%d')
        temp = {'platform': i, 'data': data, 'date': today}
        result.append(temp)
    jsonResult = json.dumps(result)
    print  jsonResult
    return jsonResult


if __name__ == "__main__":
    main()
