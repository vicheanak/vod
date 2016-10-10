# -*- coding: utf-8 -*-
import scrapy
from scrapy.spiders import CrawlSpider, Rule
from freshnews.items import FreshnewsItem
from scrapy.linkextractors import LinkExtractor
import time


class TestSpider(CrawlSpider):
    name = "freshnews"
    allowed_domains = ["freshnewsasia.com"]
    start_urls = [
    'http://www.freshnewsasia.com/index.php/en/',
    ]

    def parse(self, response):
        now = time.strftime('%Y-%m-%d %H:%M:%S')
        hxs = scrapy.Selector(response)

        articles = hxs.xpath('//td[@headers="categorylist_header_title"]')

        for article in articles:
            item = FreshnewsItem()
            item['categoryId'] = '1'

            name = article.xpath('a/text()')
            if not name:
                print('FreshNews => [' + now + '] No title')
            else:
                item['name'] = name.extract_first()

            url = article.xpath("a/@href")
            if not url:
                print('FreshNews => [' + now + '] No url')
            else:
                item['url'] = 'http://www.freshnewsasia.com/' + url.extract_first()

            request = scrapy.Request(item['url'], callback=self.parse_detail)
            request.meta['item'] = item
            yield request

    def parse_detail(self, response):
        item = response.meta['item']
        hxs = scrapy.Selector(response)
        now = time.strftime('%Y-%m-%d %H:%M:%S')

        item_page = hxs.css('div.item-page')
        description = item_page.xpath('p[1]/text()')
        if not description:
            print('FreshNews => [' + now + '] No description')
        else:
            item['description'] = item_page.xpath('p[1]/strong/text()').extract_first() + ' ' + description.extract_first()

        imageUrl = item_page.xpath('p[last()]/img/@src')
        if not imageUrl:
            print('FreshNews => [' + now + '] No imageUrl')
        else:
            item['imageUrl'] = imageUrl.extract_first()


        yield item
