import scrapy
from scrapy.crawler import CrawlerProcess
from maoyan import *
from maoyan.spiders.maoyan_spider import MaoyanSpider
from scrapy.settings import Settings
from scrapy.utils.project import get_project_settings

def run_spider(years):
    year_list = ','.join(years)
    process = CrawlerProcess(get_project_settings())
    process.crawl(MaoyanSpider, year_list='12')
    process.start()

run_spider(['12','13'])   #the template you use the function.