# -*- coding: utf-8 -*-
import time
from demo3.items import Book
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule


class BookSpider(CrawlSpider):
    name = 'book'
    allowed_domains = ['book3k.com']
    start_urls = ['https://book3k.com/']
    rules = (
        Rule(LinkExtractor(allow=r'archives/\d+'), callback='parse_item', follow=True),
    )

    def parse_item(self, response):
        # bookItem = CommonItemLoader(item=Book(), response=response)
        # css = bookItem.add_css("content", ".entry-content.clearfix p")
        item = Book()
        divs = response.xpath('//div[@id="content"]')
        body = ""
        title = response.css(".entry-title::text").extract()[0]
        category = response.css(".meta-category a::text").extract()[0]
        publishTime = response.css(".meta-date a time::text").extract()[0]
        timeArray = time.strptime(publishTime, "%d/%m/%Y")
        publishTime = time.strftime("%Y/%m/%d", timeArray)
        for p in divs.xpath('.//p/text()'):
            body = body + p.extract().strip() + "\r\n"
        # i['domain_id'] = response.xpath('//input[@id="sid"]/@value').extract()
        # i['name'] = response.xpath('//div[@id="name"]').extract()
        # i['description'] = response.xpath('//div[@id="description"]').extract()
        # item['content'] = body
        item["title"] = title
        item["content"] = body
        item["category"] = category
        # item["publishTime"] = publishTime
        yield item
