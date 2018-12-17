# -*- coding: utf-8 -*-
import scrapy
import re
import sys
sys.path.append('..\\')
from maoyan.items import MaoyanItem
import time, random
from maoyan.num_decode import getNumber
import pandas as pd
import sqlite3
import json

year_flag = 1
page = 0
movie_scraped = []
try:
    with sqlite3.connect('scrapy.db') as con:
        df = pd.read_sql(sql='SELECT name FROM flash_movie', con=con)
        movie_scraped = df['name'].tolist()

except:
    movie_scraped = []


class MaoyanSpider(scrapy.Spider):
    global year_flag
    global page
    global movie_scraped
    name = 'maoyan_spider'
    allowed_domains = ['maoyan.com/films']

    def __init__(self, year_list='10,11,12,13', *args, **kwargs):
        super(MaoyanSpider, self).__init__(*args, **kwargs)
        self.year_list = year_list.split(',')
        self.start_urls = ['https://maoyan.com/films?showType=3&yearId='+self.year_list[0]+'&sortId=3']

    def parse(self, response):
        global year_flag
        global page

        movie_list = []
        movie_list = response.xpath("//div[@class='channel-detail movie-item-title']/a/@href").extract()
        name_list = response.xpath("//div[@class='channel-detail movie-item-title']/a/text()").extract()
        print(movie_list)
        if len(movie_list)==0:
            yield scrapy.Request(response.url, meta={'useSelenium':True, 'noRedirect':True}, callback=self.parse, dont_filter=True)
            return
        for i in range(0, len(movie_list)):

            next_link = movie_list[i]
            movie_scrapping = name_list[i]
            if next_link and movie_scrapping not in movie_scraped:
                yield scrapy.Request("https://maoyan.com" + next_link, meta={'useSelenium':True, 'noRedirect':True}, callback=self.sub_page, dont_filter=True)
        next_page = response.xpath("//div[@class='movies-pager']/ul/li/a[contains(text(),'下一页')]/@href").extract_first()

        print('page='+ str(page), next_page)

        if next_page and page < 15:
            yield scrapy.Request("https://maoyan.com/films" + next_page,meta={'useSelenium':True, 'noRedirect':True},  callback=self.parse, dont_filter=True)
            page = page + 1
        elif year_flag < len(self.year_list):
            yield scrapy.Request("https://maoyan.com/films?showType=3&yearId=" + self.year_list[year_flag] + '&sortId=3',meta={'useSelenium':True, 'noRedirect':True},  callback=self.parse, dont_filter=True)
            page = 0
            year_flag += 1
        pass

    def sub_page(self, response):
        time.sleep(random.random()*3)
        #print(re.search(r"url\('(?P<font>.+?woff)'", response.text).group('font'))
        movie_item = MaoyanItem()
        #电影名称
        if not response.xpath("//h3[@class='name']/text()").extract_first():
            yield scrapy.Request(response.url, meta={'useSelenium':True, 'noRedirect':True}, callback= self.sub_page, dont_filter=True)
            return
        movie_item['name'] = response.xpath("//h3[@class='name']/text()").extract_first()
        #上映日期
        movie_item['date'] = str(response.xpath("//ul/li[@class='ellipsis'][contains(text(),'上映')]/text()").extract_first()).replace('大陆上映','')
        #导演与演员
        director_path = "//div[@class='celebrity-group']/div[@class='celebrity-type'][contains(text(),'导演')][not(contains(text(),'副导演'))]/../ul/li/div[@class='info']/a[1]/text()"
        movie_item['director'] = str(response.xpath(director_path).extract_first()).replace(' ','').replace('\n','').replace('\\n','')
        actor_path = "//div[@class='celebrity-group']/div[@class='celebrity-type'][contains(text(),'演员')]/../ul/li/div[@class='info']/a[1]/text()"
        items = response.xpath(actor_path).extract()
        actors = []
        flag = 0
        for item in items:
            if flag > 15:
                break
            item = str(item).replace('\\n','').replace(' ','').replace('\n','')
            if item not in actors and item != ',':
                actors.append(item)
                flag = flag + 1
        movie_item['actors'] = json.dumps(actors, ensure_ascii=False)

        #电影类型
        movie_type = response.xpath("//div[@class='movie-brief-container']/ul/li[1]/text()").extract_first()
        if movie_type and '分钟' not in str(movie_type):
            movie_item['type'] = json.dumps(str(movie_type).split(','), ensure_ascii=False)
        else:
            movie_item['type'] = None

        #字符解码文件url
        if(re.search(r"url\('(?P<font>.+?woff)'", response.text)):
            url = re.search(r"url\('(?P<font>.+?woff)'", response.text).group('font')
        #评分数据
        score = response.xpath("//div[@class='movie-index-content score normal-score']/span/span[@class='stonefont']/text()").extract_first()
        #票房数据
        money = response.xpath("//div[@class='movie-index-content box']/span[@class='stonefont']/text()").extract_first()
        unit = response.xpath("//div[@class='movie-index-content box']/span[@class='unit']/text()").extract_first()

        if score and money:
            decode = getNumber(url, [score, money])
            score_decode = decode[0]
            money_decode = decode[1]
        elif score:
            score_decode = getNumber(url, [score])[0]
        elif money:
            money_decode = getNumber(url, [money])[0]


        if score:
            movie_item['score'] = float(score_decode)
        else:
            movie_item['score'] = None

        if money:
            if unit == '亿':
                money = float(money_decode) * 100000000
            elif unit == '万':
                money = float(money_decode) * 10000
            try:
                movie_item['box_office'] = round(money)
            except TypeError:
                print('[ERRRRRRR]', money)
                movie_item['box_office'] = None
        else:
            movie_item['box_office'] = None
        yield movie_item

        pass


