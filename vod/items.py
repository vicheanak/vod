# -*- coding: utf-8 -*-


import scrapy


class VodItem(scrapy.Item):
    name = scrapy.Field()
    description = scrapy.Field()
    url = scrapy.Field()
    imageUrl = scrapy.Field()
    htmlcontent = scrapy.Field()
    categoryId = scrapy.Field()
