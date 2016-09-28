import datetime
import json

from fb_crawler import get_by_request as get_fb_fans
from weibo_crawler import get_by_request as get_sina_fans
from twitter_crawler import get_by_request as get_twitter_fans
from youtube_crawler import get_by_request as get_youtube_fans
from youku_crawler import get_by_request as get_youku_fans


def main():
    platform = ['facebook', 'weibo', 'twitter', 'youtube', 'youku']
    result = []
    for i in platform:
        fans = 0

        if i == 'facebook':
            fans = get_fb_fans()
        elif i == 'weibo':
            fans = get_sina_fans()
        elif i == 'twitter':
            fans = get_twitter_fans()
        elif i == 'youtube':
            fans = get_youtube_fans()
        elif i == 'youku':
            fans = get_youku_fans()

        today = datetime.datetime.now().strftime('%Y-%m-%d')
        temp = {'platform': i, 'fans': fans, 'date': today}
        result.append(temp)
    jsonResult = json.dumps(result)
    print  jsonResult
    return jsonResult


if __name__ == "__main__":
    main()
