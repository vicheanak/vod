# -*- coding: utf-8 -*-
import scrapy
from scrapy.spiders import CrawlSpider, Rule
from kohsantepheap.items import KohsantepheapItem
from scrapy.linkextractors import LinkExtractor


class TestSpider(CrawlSpider):
    name = "kohsantepheap"
    allowed_domains = ["kohsantepheapdaily.com.kh"]
    start_urls = ['https://kohsantepheapdaily.com.kh/category/local-news/']

    def parse(self, response):
        hxs = scrapy.Selector(response)
        articles = hxs.xpath('//div[@class="articleItem"]')
        for article in articles:
            text = article.xpath('div[@class="articleText"]')
            image = article.xpath('div[@class="articleImage"]')
            item = KohsantepheapItem()
            item['name'] = text.xpath('h4/a/text()').extract()[0]
            item['description'] = text.xpath('p/text()').extract()[1]
            item['url'] = 'https://kohsantepheapdaily.com.kh' + text.xpath("h4/a/@href").extract()[0]
            item['imageUrl'] = image.xpath('a/img/@src').extract()[0]
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
