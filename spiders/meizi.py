# -*- coding: utf-8 -*-
import scrapy
from scrapy import Request
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule
from scrapy.selector import Selector
from demo3.items import MeiZi, CommonItemLoader


class MeiziSpider(CrawlSpider):
    name = 'meizi'
    allowed_domains = ['mmjpg.com']
    start_urls = ['http://www.mmjpg.com']

    rules = (
        Rule(LinkExtractor(allow=r'mm/\d+/\d+', deny_domains='m.mmjpg.com'), callback='parse_mm', follow=True, ),
    )

    def parse_mm(self, response):
        selector = Selector(response=response)
        meiziItem = CommonItemLoader(item=MeiZi(), response=response)
        meiziItem.add_css("imgUrl", "#content a img::attr(src)")
        item = meiziItem.load_item()
        item['imgrl'] = [item.get("imgUrl", "")]

        yield item
