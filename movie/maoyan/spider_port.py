import scrapy
from scrapy.crawler import CrawlerProcess
from maoyan import *
from maoyan.spiders.maoyan_spider import MaoyanSpider
from scrapy.utils.project import get_project_settings

import sqlite3




def run_spider(years):
    year_list = ','.join(years)
    process = CrawlerProcess(get_project_settings())
    process.crawl(MaoyanSpider, year_list=year_list)
    process.start()

    db_name = 'scrapy.db'
    db_conn = sqlite3.connect(db_name)
    db_cur = db_conn.cursor()

    delete_old_data(years, db_cur)

    flash_data(db_cur, db_conn)
    db_conn.commit()
    db_conn.close()

def delete_old_data(years, db_cur):

    year_dic = {'10':'2015', '11':'2016', '12':'2017', '13':'2018'}
    real_years = []
    for year in years:
        year = year_dic[year]

        year_ahead = str(int(year)-1)
        year_after = str(int(year)+1)

        db_cur.execute('DELETE FROM movie WHERE ? < substr(date, 1, 4) AND substr(date, 1, 4) < ?', (year_ahead, year_after))
        real_years.append(year)
    print(real_years)
    db_cur.execute("DELETE FROM flash_movie WHERE substr(date, 1,4) NOT IN ( ? )", (real_years))

def flash_data(db_cur, db_conn):
    order_add = 'INSERT INTO movie SELECT * FROM flash_movie'
    db_cur.execute(order_add)
    order_del_table = 'DROP TABLE flash_movie'
    db_cur.execute(order_del_table)




run_spider(['12'])   #the template you use the function. 10 for 2015 and so on.