# -*- coding: utf-8 -*-
from demo3.items import CommonItemLoader, PiaoHua
from scrapy import Selector
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule


class PiaohuaSpider(CrawlSpider):
    name = 'piaohua'
    allowed_domains = ['piaohua.com']
    start_urls = ['http://www.piaohua.com/']

    rules = (
        Rule(LinkExtractor(allow=r'html/.*?\d+.html'), callback='parse_item', follow=True),
    )

    def parse_item(self, response):
        selector = Selector(response=response)
        movie = CommonItemLoader(item=PiaoHua(), response=response)
        movie.add_css("title", "#showinfo > div:nth-child(4)::text")
        movie.add_css("cover", "#showinfo > img:nth-child(2)::attr(src)")
        movie.add_css("time", "#showinfo > div:nth-child(6)::text")
        movie.add_css("nation", "#showinfo > div:nth-child(7)::text")
        movie.add_css("type", "#showinfo > div:nth-child(8)::text")
        movie.add_css("language", "#showinfo > div:nth-child(9)::text")
        movie.add_css("releaseDate", "#showinfo > div:nth-child(10)::text")
        movie.add_css("rate", "#showinfo > div:nth-child(11)::text")
        movie.add_css("duration", "#showinfo > div:nth-child(14)::text")
        movie.add_css("actor", "#showinfo > div:nth-child(15)::text")
        movie.add_css("summary", "#showinfo > div:nth-child(34)::text")
        movie.add_css("bit", "#showinfo > table:nth-child(38) > tbody > tr > td > a::attr(href)")
        movie.add_css("thunder", "#showinfo > table:nth-child(39) > tbody > tr > td > anchor > a::text")

        item = movie.load_item()

        yield item
