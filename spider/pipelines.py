# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html
import pymysql
from spider import settings
import time

class ZongHengPipeline(object):
    def __init__(self):
        self.connect = pymysql.connect(
            host=settings.MYSQL_HOST,
            db=settings.MYSQL_DBNAME,
            user=settings.MYSQL_USER,
            passwd=settings.MYSQL_PASSWD,
            charset='utf8',
            use_unicode=True)
        self.cursor = self.connect.cursor()

    def process_item(self, item, spider):
        # print(str(item.__class__) == "<class 'spider.items.ZonghengItem'>")
        # print(item['author'])
        # f = open("/home/hanyun/spider/log.log", 'a')
        # f.write(str(item.__class__) + '\n')   textNumber
        # f.close()
        sql = """
INSERT INTO app.lee_book (book_name, book_author, book_href, book_category, book_text_number, book_add_time)
 VALUES ('%s','%s','%s','%s','%s','%s')""" % (
        item['bookTitle'][0], item['author'][0], item['bookLink'][0], item['category'][0], int(item['textNumber'][0]),int(time.time()))
        print(sql)
        self.cursor.execute(sql)
        self.connect.commit()
