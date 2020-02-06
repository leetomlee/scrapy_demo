# -*- coding: utf-8 -*-
import scrapy
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule


class ImgSpider(CrawlSpider):
    name = 'img'
    allowed_domains = ['img.vquite.space']
    start_urls = ['http://img.vquite.space/']

    rules = (
        Rule(LinkExtractor(allow=r'thumb/\d+-\d+-\d+/.*?_thumb_\d.jpg'), callback='parse_item', follow=True),
    )

    def parse_item(self, response):
        i = {}
        #i['domain_id'] = response.xpath('//input[@id="sid"]/@value').extract()
        #i['name'] = response.xpath('//div[@id="name"]').extract()
        #i['description'] = response.xpath('//div[@id="description"]').extract()
        return i
