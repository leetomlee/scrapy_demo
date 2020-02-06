# -*- coding: utf-8 -*-
import scrapy
from scrapy import Request
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule


class VideoSpider(CrawlSpider):
    name = 'video'
    allowed_domains = ['email.v2dizhi.at.gmail.com.p2tv.space']
    start_urls = ['http://email.v2dizhi.at.gmail.com.p2tv.space/']

    rules = (
        Rule(LinkExtractor(allow=r'v/.*?'), callback='parse_item', follow=True),
    )

    def parse_item(self, response):
        css = response.css("#h5player_html5_api::attr(src)")

        # i['domain_id'] = response.xpath('//input[@id="sid"]/@value').extract()
        # i['name'] = response.xpath('//div[@id="name"]').extract()
        # i['description'] = response.xpath('//div[@id="description"]').extract()
        print(css)

    def start_requests(self):
        for url in self.start_urls:
            yield Request(url, callback=self.parse, meta={'proxy':'https://144.123.46.106:8118'})
