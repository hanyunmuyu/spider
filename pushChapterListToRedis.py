from spider import redis
from spider import settings
import pymysql

connect = pymysql.connect(
    host=settings.MYSQL_HOST,
    db=settings.MYSQL_DBNAME,
    user=settings.MYSQL_USER,
    passwd=settings.MYSQL_PASSWD,
    charset='utf8',
    use_unicode=True)
cursor = connect.cursor()
cursor.execute("select * from lee_book_chapter WHERE chapter_path IS NULL limit 5000")
chapterList = cursor.fetchall()
if chapterList:
    for chapter in chapterList:
        redis.redisConnect.sadd(settings.CHAPTER_SET, chapter[4])
