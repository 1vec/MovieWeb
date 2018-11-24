# -*- coding: utf-8 -*-
import scrapy
from maoyan.items import MaoyanItem

year_list = ['11','12','13','14']
year_flag = 0


class MaoyanSpiderSpider(scrapy.Spider):
    global year_flag
    global year_list
    name = 'maoyan_spider'
    allowed_domains = ['maoyan.com/films']
    start_urls = ['http://maoyan.com/films?showType=3&yearId=10']

    def parse(self, response):
        global year_flag
        movie_list = response.xpath("//div[@class='channel-detail movie-item-title']/a/@href").extract()
        for url_item in movie_list:
            next_link = url_item
            if next_link:
                yield scrapy.Request("http://maoyan.com"+next_link,callback = self.sub_page, dont_filter = True)
        next_page = response.xpath("//div[@class='movies-pager']/ul/li/a[contains(text(),'下一页')]/@href").extract_first()
        if next_page:
            yield scrapy.Request("https://maoyan.com/films" + next_page, callback = self.parse, dont_filter=True)
        elif year_flag < 3:
            yield scrapy.Request("https://maoyan.com/films?showType=3&yearId=" + year_list[year_flag],callback = self.parse, dont_filter = True)
            year_flag += 1
        pass

    def sub_page(self, response):
        movie_item = MaoyanItem()
        movie_item['name'] = response.xpath("//h3[@class='name']/text()").extract_first()
        movie_item['date'] = str(response.xpath("//ul/li[@class='ellipsis'][contains(text(),'上映')]/text()").extract_first()).replace('国内上映','')

        score = response.xpath("//div[@class='movie-index-content score normal-score']/span/span[@class='stonefont']/text()").extract_first()
        if score:
            movie_item['score'] = score
        else:
            movie_item = '无’'

        #money = int(response.xpath("//div[@class='movie-index-content box']/span[@class='stonefont']/text()").extract_first())
        unit = response.xpath("//div[@class='movie-index-content box']/span[@class='unit']/text()").extract_first()
        """
        if money:
            if unit == '亿':
                money = money * 100000000
            elif unit == '万':
                money = money * 10000
            movie_item['box_office'] = money
        else:
            movie_item['box_office'] = '无'
        """
        yield movie_item
        #people_part = response.xpath("//div[@class='mod-title']/a[@class='more']/@href")
        pass