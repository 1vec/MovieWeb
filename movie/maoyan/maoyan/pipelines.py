# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html




class MaoyanPipeline(object):
    def process_item(self, item, spider):
        return item


# 爬取到的数据写入到SQLite数据库
import sqlite3

class SQLitePipeline(object):

    #打开数据库
    def open_spider(self, spider):
        db_name = spider.settings.get('SQLITE_DB_NAME', 'scrapy.db')

        self.db_conn = sqlite3.connect(db_name)
        self.db_cur = self.db_conn.cursor()
        self.create_table()

    #关闭数据库
    def close_spider(self, spider):
        self.db_conn.commit()
        self.db_conn.close()

    #对数据进行处理
    def process_item(self, item, spider):
        self.insert_db(item)
        return item

    #插入数据
    def insert_db(self, item):
        values = (
            item['name'],
            #item['type'],
            #item['actors'],
            #item['director'],
            #item['box_office'],
            item['date'],
            item['score'],
        )

        sql = 'INSERT INTO movies VALUES(?,?,?)'
        self.db_cur.execute(sql, values)

    #创建表
    def create_table(self):
        table = "CREATE TABLE movies('name' TEXT, 'date' TEXT, 'score' TEXT)"
        self.db_cur.execute(table)
