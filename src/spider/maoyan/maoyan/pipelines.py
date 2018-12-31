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
        db_name = spider.settings.get('SQLITE_DB_NAME')

        self.db_conn = sqlite3.connect(db_name, detect_types=sqlite3.PARSE_DECLTYPES)
        self.db_conn.execute("PRAGMA foreign_keys = ON")
        self.db_conn.row_factory = sqlite3.Row
        self.db_cur = self.db_conn.cursor()
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

        #删除已经存在的数据
        self.db_cur.execute('DELETE FROM movies WHERE id = ?', (item['movie_id'], ))
        #在movie表中插入新数据
        self.db_cur.execute(
            'INSERT INTO movies (id, name, director, box_office, date, score)'
            'VALUES (?, ?, ?, ?, ?, ?)', (item['movie_id'], item['name'], item['director'], item['box_office'], item['date'], item['score'])
        )
        #对演员
        for actor in item['actors']:
            self.init_record('actors', actor)
            actor_id = self.get_id_by_name('actors', actor)
            self.db_cur.execute('INSERT INTO movie_actor (movie_id, actor_id) VALUES (?, ?)', (item['movie_id'], actor_id))

        #对类别
        for tp in item['type']:
            self.init_record('types', tp)
            type_id = self.get_id_by_name('types', tp)
            self.db_cur.execute('INSERT INTO movie_type (movie_id, type_id) VALUES (?, ?)', (item['movie_id'], type_id))

        self.db_conn.commit()

    #创建表
    # def create_table(self):
    #     with open('scrapy.sql') as f:
    #         self.db_conn.executescript(f.read())

    def get_id_by_name(self, table_name, name):
        command = 'SELECT id FROM {} WHERE name = ?'.format(table_name)
        #print(command)
        return self.db_cur.execute(command, (name,)).fetchone()['id']

    def init_record(self, table_name, name):
        command = 'INSERT INTO {0:} (name) SELECT ? WHERE NOT EXISTS(SELECT 1 FROM {0:} WHERE name = ?)'.format(
            table_name)
        return self.db_cur.execute(command, (name, name))
    #创建表
    #def create_table(self):
        #table = """CREATE TABLE flash_movie(
        #'name' TEXT,
        #'type' TEXT,
        #'actors' TEXT,
        #'director' TEXT,
        #'box_office' INTEGER,
        #'date' TEXT,
        #'score' REAL)"""
        #self.db_cur.execute(table)

    # def read_table_data(self, table_name):
    #     order = 'SELECT '+ table_name + ';'
    #     self.db_cur.execute(order)

