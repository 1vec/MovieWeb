import scrapy
from scrapy.crawler import CrawlerProcess
from maoyan import *
from maoyan.spiders.maoyan_spider import MaoyanSpider
from scrapy.settings import Settings
from scrapy.utils.project import get_project_settings


settings = Settings()
process = CrawlerProcess(get_project_settings())
process.crawl(MaoyanSpider, year_list='12')
process.start()