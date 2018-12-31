import scrapy
from scrapy.crawler import CrawlerProcess
from maoyan.spiders.maoyan_spider import MaoyanSpider
from scrapy.utils.project import get_project_settings

import sqlite3



#传入参数用CrawlerProcess运行scrapy
def run_spider(years, route):
    year_list = ','.join(years)
    settings = get_project_settings()
    settings.set('SQLITE_DB_NAME', route)
    process = CrawlerProcess(settings)
    process.crawl(MaoyanSpider, year_list=year_list)
    process.start()
    #print('##################################working##########################################')


run_spider(['12'],'db.sqlite')