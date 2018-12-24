import scrapy
from scrapy.crawler import CrawlerProcess
from maoyan import *
from maoyan.spiders.maoyan_spider import MaoyanSpider
from scrapy.utils.project import get_project_settings

import sqlite3




def run_spider(years, route):
    year_list = ','.join(years)
    settings = get_project_settings()
    settings.set('SQLITE_DB_NAME', route)
    process = CrawlerProcess(settings)
    process.crawl(MaoyanSpider, year_list=year_list)
    process.start()



run_spider(['12'],'db.sqlite')   #the template you use the function. 10 for 2015 and so on.