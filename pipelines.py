# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html
import os

import pymysql
from twisted.enterprise import adbapi

# class MeiZiPipeline(ImagesPipeline):
#     pass
# class PiaoHuaPipeline(object):
#     client=MongoClient('120.27.244.128',27017)
#     db = client.pythondb
#     posts = db.posts
#     its=item
#     posts.insert(item)
#
#     pass
from demo3.items import Book


# class Demo3Pipeline(object):
#     def process_item(self, item, spider):
#         return item


class CrawlerScrapyPipeline(object):
    def __init__(self, dbpool):
        self.dbpool = dbpool

    def process_item(self, item, spider):
        query=''
        if isinstance(item,Book):
            query = self.dbpool.runInteraction(
            self.insert_book, item)
        else:
            query=self.dbpool.runInteraction(self.insert_chapter,item)
        query.addErrback(self._handle_error, item, spider)  # 调用异常处理方法
        return item
        # 写入数据库中

    def insert_chapter(self, tx, item):
        sql="insert into chapter(chapter_id,book_id,chapter_name) values (%s,%s,%s)"
        params=(item['chapter_id'],item['book_id'],item['chapter_name'])
        tx.execute(sql,params)

    def insert_book(self, tx, item):
        # print item['name']
        sql = "insert into book(id,book_name,book_desc,author,category,cover,hot,last_chapter,status,u_time) values(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)"
        params = (
        item["id"], item["book_name"], item["book_desc"], item["author"], item["category"], item["cover"], item["hot"],
        item["last_chapter"], item["status"], item["u_time"])
        tx.execute(sql, params)

    # 错误处理方法
    def _handle_error(self, failue, item, spider):
        print(failue, item)

    @classmethod
    def from_settings(cls, settings):
        '''1、@classmethod声明一个类方法，而对于平常我们见到的则叫做实例方法。
           2、类方法的第一个参数cls（class的缩写，指这个类本身），而实例方法的第一个参数是self，表示该类的一个实例
           3、可以通过类来调用，就像C.f()，相当于java中的静态方法'''
        dbparams = dict(
            host=settings['MYSQL_HOST'],  # 读取settings中的配置
            db=settings['MYSQL_DBNAME'],
            user=settings['MYSQL_USER'],
            passwd=settings['MYSQL_PASSWD'],
            charset='utf8',  # 编码要加上，否则可能出现中文乱码问题
            cursorclass=pymysql.cursors.DictCursor,
            use_unicode=False,
        )
        dbpool = adbapi.ConnectionPool('pymysql', **dbparams)  # **表示将字典扩展为关键字参数,相当于host=xxx,db=yyy....
        return cls(dbpool)  # 相当于dbpool付给了这个类，self中可以得到


project_dir = os.path.abspath(os.path.dirname(__file__))
IMAGES_STORE = os.path.join(project_dir, "books")


class BookPipeline(object):
    def process_item(self, item, spider):
        with open(IMAGES_STORE + "/" + item["title"] + ".txt", "w", encoding='utf-8') as f:
            f.write(item["content"])
