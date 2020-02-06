# -*- coding: utf-8 -*-
import scrapy
from scrapy import Selector
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule

from demo3.items import CommonItemLoader, MeiZi


class MeituSpider(CrawlSpider):
    name = 'meitu'
    allowed_domains = ['meitulu.com']
    start_urls = ['https://www.meitulu.com']

    rules = (
        Rule(LinkExtractor(allow=r'item/\d+_\d+.html'), callback='parse_item', follow=True),
        Rule(LinkExtractor(allow=r'item/\d+.html'), callback='parse_item', follow=True),
    )

    def parse_item(self, response):
        selector = Selector(response=response)
        item = MeiZi()
        # meiziItem = CommonItemLoader(item=MeiZi(), response=response)
        css = selector.css(".content center img::attr(src)")
        xpath = selector.xpath("//div[@class='content']/center")
        srcs = []
        for x in xpath.css("img::attr(src)").extract():
            srcs.append(x)
        item['imgUrl'] = srcs
        yield item
