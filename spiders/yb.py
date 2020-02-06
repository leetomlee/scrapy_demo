# -*- coding: utf-8 -*-
import scrapy
from pymongo import MongoClient
from scrapy.linkextractors import LinkExtractor
from scrapy.selector import Selector
from scrapy.spiders import CrawlSpider, Rule

from demo3.items import Book, Chapter, CommonItemLoader

conn = MongoClient('120.27.244.128', 27017)
dd = conn.book
my_set = dd.chapters


class MeiziSpider(CrawlSpider):
    name = 'yb'
    allowed_domains = ['m.lewenr.com']
    start_urls = ['http://m.lewenr.com/']

    rules = (
        Rule(LinkExtractor(allow=r'info-\d+/'), callback='parse_mm',follow=True ),
    )
    u_time = scrapy.Field()
    category = scrapy.Field()
    book_name = scrapy.Field()
    author = scrapy.Field()
    book_desc = scrapy.Field()
    status = scrapy.Field()

    def parse_mm(self, response):
        id = str(response.url).split('-')[1].split('/')[0]
        yield scrapy.Request(url=str(response.url).replace('info', 'wapbook'), callback=self.parseChapters,
                             meta={"id": id})
        selector = Selector(response=response)
        book = CommonItemLoader(item=Book(), response=response)
        book.add_value("id", id)
        book.add_value("cover", selector.xpath("//div[@class='block_img2']/img/@src").extract_first())
        book.add_value("hot", 1)
        book.add_xpath('book_name', "//div[@class='block_txt2']/p[1]/a/h2/text()")
        book.add_xpath('author', "//div[@class='block_txt2']/p[2]/a/text()")
        book.add_xpath('category', "//div[@class='block_txt2']/p[3]/a/text()")
        book.add_xpath('status', "//div[@class='block_txt2']/p[4]/text()")
        book.add_value('book_desc', ''.join(selector.xpath("//div[@class='intro_info']/text()").getall()))
        book.add_value("u_time",
                       str(selector.xpath("//div[@class='block_txt2']/p[5]/text()").extract_first()).split('：')[1])
        book.add_xpath('last_chapter', "//div[@class='block_txt2']/p[6]/a/text()")
        item = book.load_item()
        yield item

    def parseContent(self, response):
        selector = Selector(response=response)
        content = ''.join(selector.xpath('//*[@id="nr1"]/text()').getall()
                          )
        ls = str(response.url).split('-')
        bookId = ls[1]
        chapterId = ls[2].replace('/', '')
        my_set.insert_one({"content": content, "_id": chapterId})
        chapter = CommonItemLoader(item=Chapter(), response=response)
        chapter.add_value('book_id', bookId)
        chapter.add_value('chapter_id', chapterId)
        chapter.add_value('chapter_name', response.meta['name'])
        item = chapter.load_item()
        yield item

    def parseChapter(self, response):
        selector = Selector(response=response)
        for li in selector.xpath('//ul[@class="chapter"]/li'):
            chapterName = li.xpath('a/text()').extract_first()
            chapterLink = 'http://m.lewenr.com' + li.xpath('a/@href').extract_first()
            yield scrapy.Request(url=chapterLink, callback=self.parseContent, meta={"name": chapterName})

    def parseChapters(self, response):
        selector = Selector(response=response)
        info = selector.xpath('//div[@class="page"][2]/text()').getall()[2]
        count = str(info)[4]
        for i in range(int(count)):
            url = response.url[:len(response.url) - 1] + '_' + str(i + 1) + '/'
            yield scrapy.Request(url=url, callback=self.parseChapter)
