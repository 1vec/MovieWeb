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
        try:
            self.create_table()
        except:
            print("Table exists.Continuing to add data.")

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
            item['type'],
            item['actors'],
            item['director'],
            item['box_office'],
            item['date'],
            item['score'],
        )

        sql = 'INSERT INTO movies (name, type, actors, director, box_office, date, score) VALUES (?,?,?,?,?,?,?)'
        self.db_cur.execute(sql, values)
        self.db_conn.commit()

    #创建表
    def create_table(self):
        table = """CREATE TABLE movies(
        'id' INTEGER PRIMARY KEY AUTOINCREMENT,
        'name' TEXT,
        'type' TEXT,
        'actors' TEXT,
        'director' TEXT,
        'box_office' INTEGER,
        'date' TEXT,
        'score' REAL)"""
        self.db_cur.execute(table)

    def read_table_data(self, table_name):
        order = 'SELECT '+ table_name + ';'
        self.db_cur.execute(order)

