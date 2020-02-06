# -*- coding: utf-8 -*-
import scrapy
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule


class QisuSpider(CrawlSpider):
    name = 'qisu'
    allowed_domains = ['www.qisuu.com']
    start_urls = ['http://www.qisuu.com']

    rules = (
        Rule(LinkExtractor(allow=r'\d+.html',deny=r'[a-zA-Z].*?'), callback='parse_item', follow=True),
    )

    def parse_item(self, response):
        i = {}
        #i['domain_id'] = response.xpath('//input[@id="sid"]/@value').extract()
        #i['name'] = response.xpath('//div[@id="name"]').extract()
        #i['description'] = response.xpath('//div[@id="description"]').extract()
        return i
