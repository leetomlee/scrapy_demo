# -*- coding: utf-8 -*-
from scrapy import Selector
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule
from enum import Enum

from demo3.items import Book

from demo3.items import MeiZi


class BbbSpider(CrawlSpider):
    name = 'bbb'
    allowed_domains = ['m.67as.com']
    start_urls = ['http://m.67as.com/']
    rules = (
        Rule(LinkExtractor(allow=r'html/TXT\d+/\d+.html'), callback='parse_item', follow=True),
        # Rule(LinkExtractor(allow=r'html/PIC\d+/\d+.html'), callback='parse_itempic', follow=True),
    )

    def parse_itempic(self, response):
        selector = Selector(response=response)
        item = MeiZi()
        pics = selector.css(".temp23")
        imgs = []
        for pic in pics.css("a::attr(href)").extract():
            imgs.append(pic)
        item['imgUrl'] = imgs
        yield item

    def parse_item(self, response):
        data = {"乱伦文学": "LLWX",
                "武侠古典": "WXGD",
                "淫色人妻": "YSRQ",
                "激情文学": "JQWX",
                "迷情校园": "MQXY",
                "性爱技巧": "XAJQ",
                "另类小说": "LLXS"}
        item = Book()
        extracts = response.css(".n.link a::text")
        title = extracts.extract()[2]
        category = extracts.extract()[1]
        text = response.css(".temp22::text").extract()
        item['title'] = title
        item['category'] = data.get(category)
        content = ''
        for c in text:
            content = content + c
        if content.strip():
            pass
        item['content'] = content

        yield item
