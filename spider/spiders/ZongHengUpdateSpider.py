# -*- coding: utf-8 -*-
import scrapy
import pymysql
from spider import settings


class ZonghengupdatespiderSpider(scrapy.Spider):
    name = "ZongHengUpdateSpider"
    allowed_domains = ["zongheng.com"]
    start_urls = [
    ]

    def __init__(self, name=None, **kwargs):
        super().__init__(name, **kwargs)
        self.connect = pymysql.connect(
            host=settings.MYSQL_HOST,
            db=settings.MYSQL_DBNAME,
            user=settings.MYSQL_USER,
            passwd=settings.MYSQL_PASSWD,
            charset='utf8',
            use_unicode=True)
        self.cursor = self.connect.cursor()
        sql = """
        SELECT *
FROM lee_book WHERE book_cover IS NULL LIMIT 1
        """
        self.cursor.execute(sql)
        book = self.cursor.fetchmany()
        self.start_urls.append(book[3])


def parse(self, response):
    bookCover = response.xpath("/html/body/div[4]/div/div[1]/div/div/div/div[1]/p/a/img/@src").extract()
    print(bookCover)
