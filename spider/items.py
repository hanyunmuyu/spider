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
    bookCover = scrapy.Field()
    bookDescription = scrapy.Field()
    bookKeyWord = scrapy.Field()
    link = scrapy.Field()


class ZonghengChapter(scrapy.Item):
    parentUrl = scrapy.Field()
    url = scrapy.Field()
    title = scrapy.Field()
    textNumber = scrapy.Field()


class ZonghengChapterDetail(scrapy.Item):
    chapterPath = scrapy.Field()
    chapterTextNumber = scrapy.Field()
    updateAt = scrapy.Field()
    chapterHref = scrapy.Field()
