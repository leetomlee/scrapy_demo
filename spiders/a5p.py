# -*- coding: utf-8 -*-
import scrapy
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule

from demo3.items import Book


class A5pSpider(CrawlSpider):
    name = '5p'
    allowed_domains = ['y1gp.5p33.date']
    start_urls = ['http://y1gp.5p33.date/']

    rules = (
        Rule(LinkExtractor(allow=r'xiaoshuozhuanqu/[a-zA-Z]+/\d+.html'), callback='parse_item', follow=True),
    )

    def parse_item(self, response):
        item = Book()
        extracts = response.css("#breadcrumb a::text")
        category = extracts.extract()[2]

        title = response.css(".post-title::text").extract()
        item['title'] = title[0]
        item['category'] = category
        temp = response.css("#post-3466 .entry::text").extract()
        content = ""
        for t in temp:
            content = content + t
        item['content'] = content

        yield item
