# -*- coding: utf-8 -*-
import scrapy
from scrapy.spiders import CrawlSpider, Rule
from vod.items import VodItem
from scrapy.linkextractors import LinkExtractor
import time
import lxml.etree
import lxml.html
from lxml.html import builder as E
from stripogram import html2text, html2safehtml

class TestSpider(CrawlSpider):
    name = "vod"
    allowed_domains = ["vodhotnews.com"]
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

            request = scrapy.Request(item['url'], callback=self.parse_detail)
            request.meta['item'] = item

            yield request

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

            request = scrapy.Request(item['url'], callback=self.parse_detail)
            request.meta['item'] = item
            yield request

    def parse_detail(self, response):

        item = response.meta['item']
        hxs = scrapy.Selector(response)
        now = time.strftime('%Y-%m-%d %H:%M:%S')

        htmlcontent = ''
        imageUrl = hxs.xpath('//article[contains(@class, "post type-post status-publish")][1]/a[1]/img[1]/@src')
        if imageUrl:
            imageEle = E.IMG(src=imageUrl.extract_first())
            imageEle = lxml.html.tostring(imageEle, encoding=unicode)
            htmlcontent = imageEle


        root = lxml.html.fromstring(response.body)
        lxml.etree.strip_elements(root, lxml.etree.Comment, "script", "head")
        content = root.xpath('//p[text() and not(contains(@class, "write_author")) and not(contains(@class, "copy")) and not(contains(@class, "text-right"))]')
        for c in content:
            htmlcontent += lxml.html.tostring(c, encoding=unicode)
        item['htmlcontent'] = htmlcontent
        print item['htmlcontent']


        yield item
