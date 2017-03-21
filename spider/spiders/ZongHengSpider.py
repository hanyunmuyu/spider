# -*- coding: utf-8 -*-
import scrapy
from spider.items import ZonghengItem, ZonghengBookDetailItem
from scrapy import Request
from scrapy.spider import CrawlSpider, Rule
from scrapy.linkextractors import LinkExtractor


class ZonghengspiderSpider(scrapy.Spider):
    name = "ZongHengSpider"
    allowed_domains = ["zongheng.com"]
    start_urls = [
        'http://book.zongheng.com/store.html'
    ]

    def __init__(self, name=None, **kwargs):
        super().__init__(name, **kwargs)
        for i in range(1000):
            self.start_urls.append('http://book.zongheng.com/store/c0/c0/b0/u0/p%s/v9/s9/t0/ALL.html' % (str(i)))

    def parse(self, response):
        for li in response.xpath("/html/body/div[4]/div[7]/div/div[1]/div/ul/li"):
            item = ZonghengItem()
            item['category'] = li.xpath('./span[1]/a/text()').extract()
            item['bookLink'] = li.xpath('./span[2]/a[1]/@href').extract()
            item['bookTitle'] = li.xpath('./span[2]/a[1]/text()').extract()
            item['newChapterLink'] = li.xpath('./span[2]/a[2]/@href').extract()
            item['newChapterTitle'] = li.xpath('./span[2]/a[2]/text()').extract()
            item['textNumber'] = li.xpath('./span[3]/text()').extract()
            item['author'] = li.xpath('./span[4]/a/text()').extract()
            yield item
            if len(item['bookLink']) > 0:
                yield Request(item['bookLink'][0], callback=self.parse_detail)
                pass

    def parse_detail(self, response):
        href = response.xpath("/html/body/div[4]/div/div[1]/div/div/div/div[2]/div[4]/span[2]/a/@href").extract()
        item = ZonghengBookDetailItem()
        item['bookCover'] = response.xpath("/html/body/div[4]/div/div[1]/div/div/div/div[1]/p/a/img/@src").extract()
        item['bookDescription'] = response.xpath(
            "/html/body/div[4]/div/div[1]/div/div/div/div[2]/div[2]/p/text()").extract()
        item['bookKeyWord'] = response.xpath(
            "/html/body/div[4]/div/div[1]/div/div/div/div[2]/div[3]/a/text()").extract()
        item['link'] = response.url
        yield item
        # yield Request(href[0], callback=self.parse_chapter)

    def parse_chapter(self, response):
        tdList = response.xpath("//td[@class='chapterBean']")
        if len(tdList):
            for td in tdList:
                href = td.xpath('./a/@href').extract()
                title = td.xpath('./a/text()').extract()
                updateInfo = td.xpath('./a/@title').extract()
