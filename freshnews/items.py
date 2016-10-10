# -*- coding: utf-8 -*-


import scrapy


class FreshnewsItem(scrapy.Item):
    name = scrapy.Field()
    description = scrapy.Field()
    url = scrapy.Field()
    imageUrl = scrapy.Field()
    categoryId = scrapy.Field()
