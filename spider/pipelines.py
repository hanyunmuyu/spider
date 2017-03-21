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
        if str(item.__class__) == "<class 'spider.items.ZonghengItem'>":
            if len(item['bookLink']) == 0:
                return
            sql = "select * from lee_book WHERE book_href='%s'" % (item['bookLink'][0])
            self.cursor.execute(sql)
            book = self.cursor.fetchone()
            if book:
                # update
                pass
            else:
                sql = """INSERT INTO app.lee_book (book_name, book_author, book_href, book_category, book_text_number, book_add_time) VALUES ('%s', '%s', '%s', '%s', '%s', '%s')""" \
                      % (
                          item['bookTitle'][0], item['author'][0], item['bookLink'][0], item['category'][0],
                          int(item['textNumber'][0]), int(time.time()))
                self.cursor.execute(sql)
                self.connect.commit()
        elif str(item.__class__) == "<class 'spider.items.ZonghengBookDetailItem'>":
            sql = """update lee_book set book_cover='%s',book_description='%s',book_key_word='%s',book_add_time='%s' WHERE book_href='%s'""" % (
                item['bookCover'][0], ''.join(item['bookDescription']).replace('\n', '').replace('\t', ''),
                ''.join(item['bookKeyWord']).replace('\n', '').replace('\t', ''), int(time.time()), item['link'])
            self.cursor.execute(sql)
            self.connect.commit()
        elif str(item.__class__) == "<class 'spider.items.ZonghengChapter'>":
            if len(item):
                sql = "select * from lee_book_chapter WHERE chapter_href='%s'" % (item['title'][0])
                self.cursor.execute(sql)
                chapter = self.cursor.fetchone()
                if chapter:
                    return
                sql = "select * from lee_book where book_href='%s'" % (item['parentUrl'])
                self.cursor.execute(sql)
                book = self.cursor.fetchone()
                bookId = book[0]
                sql = "insert into lee_book_chapter (book_id,chapter_title,chapter_href,update_at) VALUES ('%s','%s','%s','%s')" % (
                    bookId, item['title'][0], item['url'][0],
                    int(time.time()))
                self.cursor.execute(sql)
                self.connect.commit()
