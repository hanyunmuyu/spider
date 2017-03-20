# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy


##首页列表模型
class ZonghengItem(scrapy.Item):
    category = scrapy.Field()
    bookLink = scrapy.Field()
    bookTitle = scrapy.Field()
    newChapterLink = scrapy.Field()
    newChapterTitle = scrapy.Field()
    textNumber = scrapy.Field()
    author = scrapy.Field()
class ZonghengBookDetailItem(scrapy.Item):
    pass