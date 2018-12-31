import scrapy
from scrapy.crawler import CrawlerProcess
from twisted.internet import reactor
from scrapy.crawler import CrawlerRunner
import threading
from maoyan.spiders.maoyan_spider import MaoyanSpider
from scrapy.utils.project import get_project_settings

import sqlite3



#传入参数用CrawlerProcess运行scrapy
def run_spider(years, route):
    year_list = ','.join(years)
    settings = get_project_settings()
    settings.set('SQLITE_DB_NAME', route)
    #runner = CrawlerRunner(settings)
    #runner.crawl(MaoyanSpider, year_list = year_list)
    #reactor.stop()
    #reactor.run()
    process = CrawlerProcess(settings)
    process.crawl(MaoyanSpider, year_list=year_list)
    process.start()
    #print('##################################working##########################################')

#def new_thread(years, route):
#    t = threading.Thread(target=run_spider, args=(['12'],'db.sqlite'))
#    t.start()

#new_thread(['12'],'db.sqlite')   #the template you use the function. 10 for 2015 and so on.
run_spider(['12'],'db.sqlite')