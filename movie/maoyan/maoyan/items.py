# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class MaoyanItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    #电影id
    movie_id = scrapy.Field()
    #电影名称
    name = scrapy.Field()
    #电影题材
    type = scrapy.Field()
    #电影演员
    actors = scrapy.Field()
    #导演
    director = scrapy.Field()
    #累计票房
    box_office = scrapy.Field()
    #上映日期
    date = scrapy.Field()
    #观众评分
    score = scrapy.Field()

    pass
