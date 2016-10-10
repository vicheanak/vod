# -*- coding: utf-8 -*-
import scrapy
from scrapy.spiders import CrawlSpider, Rule
from kohsantepheap.items import KohsantepheapItem
from scrapy.linkextractors import LinkExtractor
import time


class TestSpider(CrawlSpider):
    name = "kohsantepheap"
    allowed_domains = ["kohsantepheapdaily.com.kh"]
    start_urls = ['https://kohsantepheapdaily.com.kh/category/local-news/']

    def parse(self, response):
        now = time.strftime('%Y-%m-%d %H:%M:%S')
        hxs = scrapy.Selector(response)
        articles = hxs.xpath('//div[@class="articleItem"]')
        for article in articles:
            item = KohsantepheapItem()

            text = article.xpath('div[@class="articleText"]')
            if not text:
                print('KSP => [' + now + '] No Text Container')

            image = article.xpath('div[@class="articleImage"]')
            if not image:
                print('KSP => [' + now + '] No Image Container')

            name = text.xpath('h4/a/text()')
            if not name:
                print('KSP => [' + now + '] No title')
            else:
                item['name'] = name.extract()[0]

            description = text.xpath('p/text()')
            if not description:
                print('KSP => [' + now + '] No description')
            else:
                item['description'] = description[1].extract()

            url = text.xpath("h4/a/@href")
            if not url:
                print('KSP => [' + now + '] No url')
            else:
                item['url'] = 'https://kohsantepheapdaily.com.kh' + url.extract()[0]

            imageUrl = image.xpath('a/img/@src')
            if not imageUrl:
                print('KSP => [' + now + '] No imageUrl')
            else:
                item['imageUrl'] = imageUrl.extract()[0]

            yield item

    def parse_detail(self, response):
        item = response.meta['item']
        hxs = scrapy.Selector(response)
        description = hxs.xpath('//div[@id="fullArticle"]/p/text()').extract()
        new_description = '';
        for node in description:
            new_description += node
        item['description'] = new_description
        image_urls = hxs.xpath('//a[@data-fancybox-group="gallery"]/img/@src').extract()
        item['imageUrl'] = image_urls
        yield item
