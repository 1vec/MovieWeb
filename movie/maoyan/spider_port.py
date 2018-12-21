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



run_spider(['12'])   #the template you use the function. 10 for 2015 and so on.