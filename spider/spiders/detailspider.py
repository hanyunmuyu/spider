# -*- coding: utf-8 -*-
import scrapy
from spider import redis
from spider import settings
import os
import re
import time
from spider.items import ZonghengChapterDetail


class DetailspiderSpider(scrapy.Spider):
    name = "detailspider"
    allowed_domains = ["zongheng.com"]

    # start_urls = ['http://zongheng.com/']

    def __init__(self, name=None, **kwargs):
        super().__init__(name, **kwargs)
        links = redis.redisConnect.smembers(settings.CHAPTER_SET)
        if len(links) > 0:
            for link in links:
                self.start_urls.append(str(link, encoding='utf8'))

    def parse(self, response):
        url = response.url
        find = re.findall('\d+', url)
        absPath = os.path.abspath('.') + '/book'
        bookDir = absPath + '/zh/' + str(find[0])
        bookChapterPath = absPath + '/zh/' + str(find[0]) + '/' + str(find[1]) + '.txt'
        bookChapterRelativePath = '/zh/' + str(find[0]) + '/' + str(find[1]) + '.txt'
        if not os.path.exists(bookDir):
            os.makedirs(bookDir)
        content = response.xpath("//div[@id='chapterContent']/p/text()").extract()
        textNumber = response.xpath('//*[@id="uiContentPanel"]/div[7]/span/em[2]/span/text()').extract()[0]
        textNumber = int(textNumber)
        updateTime = response.xpath('//*[@id="uiContentPanel"]/div[7]/span/em[1]/span/text()').extract()[0]
        updateTime = time.mktime(time.strptime(updateTime, '%Y-%m-%d %H:%M:%S'))
        if len(content) > 0:
            f = open(bookChapterPath, 'a')
            f.write('')
            for text in content:
                f.write(text.strip() + '\n')
            f.close()
        item = ZonghengChapterDetail()
        item['chapterPath'] = bookChapterRelativePath
        item['chapterTextNumber'] = textNumber
        item['updateAt'] = updateTime
        item['chapterHref'] = url
        yield item
