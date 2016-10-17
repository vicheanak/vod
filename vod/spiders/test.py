# -*- coding: utf-8 -*-
import scrapy
from scrapy.spiders import CrawlSpider, Rule
from vod.items import VodItem
from scrapy.linkextractors import LinkExtractor
import time


class TestSpider(CrawlSpider):
    name = "vod"
    allowed_domains = ["vodhotnews.com/"]
    start_urls = [
    'http://vodhotnews.com/category/politics/',
    ]

    def parse(self, response):
        now = time.strftime('%Y-%m-%d %H:%M:%S')
        hxs = scrapy.Selector(response)

        articles = hxs.xpath('//section[@class="clearfix news-by-category"]/article[@class="clearfix"]')

        for article in articles:
            item = VodItem()
            item['categoryId'] = '1'
            name = article.xpath('h3[1]/a[1]/text()')
            if not name:
                print('Vod => [' + now + '] No title')
            else:
                item['name'] = name.extract_first()

            url = article.xpath('h3[1]/a[1]/@href')
            if not url:
                print('Vod => [' + now + '] No url')
            else:
                item['url'] = url.extract_first()

            description = article.xpath('p/text()')
            if not description:
                print('Vod => [' + now + '] No description')
            else:
                item['description'] = description.extract_first()

            imageUrl = article.xpath("""
                img[1]/@src
                """)
            item['imageUrl'] = ''
            if not imageUrl:
                print('Vod => [' + now + '] No imageUrl')
            else:
                item['imageUrl'] = imageUrl.extract_first()

            yield item

        articles = hxs.xpath('//div[@class="popular-articles"][1]/ul[@class="clearfix"][1]/li')

        for article in articles:
            item = VodItem()
            item['categoryId'] = '1'
            name = article.xpath('article[1]/h4[1]/a[1]/text()')
            if not name:
                print('Vod => [' + now + '] No title')
            else:
                item['name'] = name.extract_first()

            url = article.xpath('article[1]/h4[1]/a[1]/@href')
            if not url:
                print('Vod Popular => [' + now + '] No url')
            else:
                item['url'] = url.extract_first()

            description = article.xpath('article[1]/p/text()')
            if not description:
                print('Vod Popular => [' + now + '] No description')
            else:
                item['description'] = description.extract_first()

            imageUrl = article.xpath("""
                article[1]/img[1]/@src
                """)
            if not imageUrl:
                print('Vod Popular => [' + now + '] No imageUrl')
            else:
                item['imageUrl'] = imageUrl.extract_first()

            yield item

    def parse_detail(self, response):
        item = response.meta['item']
        hxs = scrapy.Selector(response)
        now = time.strftime('%Y-%m-%d %H:%M:%S')

        item_page = hxs.css('div.item-page')
        description = item_page.xpath('p[1]/text()')
        if not description:
            print('Vod => [' + now + '] No description')
        else:
            item['description'] = item_page.xpath('p[1]/strong/text()').extract_first() + ' ' + description.extract_first()

        imageUrl = item_page.xpath('p[last()]/img/@src')
        if not imageUrl:
            print('Vod => [' + now + '] No imageUrl')
        else:
            item['imageUrl'] = imageUrl.extract_first()


        yield item
