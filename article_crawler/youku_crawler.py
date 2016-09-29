# -*- coding: UTF-8 -*-
import re
import urllib2
import json
from selenium import webdriver
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.support.ui import WebDriverWait


class YoukuCrawler:
    def __init__(self):
        self.totalPage = 1
        self.video_ids = []
        self.url = 'http://i.youku.com/i/UMjk1ODg3NDgwOA==/videos'
        client_id = 'b10ab8588528b1b1'
        self.api = 'https://openapi.youku.com/v2/videos/show_basic_batch.json?client_id=' + client_id
        cap = webdriver.DesiredCapabilities.PHANTOMJS
        cap["phantomjs.page.settings.resourceTimeout"] = 1000
        cap["phantomjs.page.settings.loadImages"] = False
        cap["phantomjs.page.settings.localToRemoteUrlAccessEnabled"] = True
        cap["userAgent"] = "Mozilla/5.0 (Windows NT 6.1; WOW64; rv:47.0) Gecko/20100101 Firefox/47.0"
        cap["XSSAuditingEnabled"] = True
        self.driver = webdriver.PhantomJS(desired_capabilities=cap,
                                          service_args=['--ignore-ssl-errors=true', '--ssl-protocol=any',
                                                        '--web-security=true'])
        # driver = webdriver.Chrome()

    def main(self):
        self.get_video_ids()
        return self.get_videos_info()

    def get_video_ids(self):
        self.driver.get(self.url + "?page=1")
        # print driver.page_source
        wait = WebDriverWait(self.driver, 20)
        try:
            wait.until(lambda x: x.find_elements_by_class_name("yk-pages"))
            self.totalPage = int(wait.until(lambda x: x.find_elements_by_class_name("yk-pages")[0].find_element_by_xpath("./li[last()-1]").text))
        except TimeoutException:
            self.totalPage = 1
        for i in range(1, self.totalPage + 1):
            if i != 1:
                self.driver.get(self.url + "?page=" + str(i))
            warp = wait.until(lambda x: x.find_elements_by_class_name("items"))[0]
            elements = warp.find_elements_by_class_name('va')
            for element in elements:
                link = element.find_element_by_xpath('./div[3]/div[1]/a').get_attribute("href")
                pattern = re.compile("/id_(.*)\.html$", re.S)
                items = re.findall(pattern, link)
                id = items[0]
                self.video_ids.append(id)


    def get_videos_info(self):
        result = []
        url = self.api + '&video_ids='
        for i in self.video_ids:
            url = url + i + ','
        request = urllib2.Request(url=url)
        response = urllib2.urlopen(request)
        page = response.read()
        videos = json.loads(page, encoding="utf-8")['videos']
        for video in videos:
            temp = {
                'account': video['user']['name'],
                'title': video['title'],
                'id': video['id'],
                'public_time': video['published'],
                'date': video['published'][:10],
                'view': video['view_count'],
                'up': video['up_count'],
                'down': video['down_count'],
                'favorite': video['favorite_count'],
                'comment': video['comment_count'],
                'link': video['link'],
            }
            result.append(temp)
        jsonResult = json.dumps(result)
        print  jsonResult
        return jsonResult


if __name__ == "__main__":
    c = YoukuCrawler()
    c.main()