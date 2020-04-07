# -*- coding: utf-8 -*-
import scrapy
from douban_book.items import DoubanBookItem

class DoubanSpider(scrapy.Spider):
    name = 'douban'
    allowed_domains = ['douban.com']
    start_urls = ['http://book.douban.com/top250']

    def parse_url(self, response):
        yield scrapy.Request(response.url, callback=self.parse)

        for page in response.xpath('//div[@class="paginator"]/a'):
            link = page.xpath('@href').extract()[0]
            yield scrapy.Request(link, callback=self.parse)

    def parse(self, response):
        for item in response.xpath('//tr[@class="item"]'):
            book = DoubanBookItem()
            book['name'] = item.xpath('td[2]/div[1]/a/@title').extract()[0]
            book['ratings'] = item.xpath('td[2]/div[2]/span[@class="rating_nums"]/text()').extract()[0]
            # book['ratings'] = item.xpath('td[2]/div[2]/span[2]/text()').extract()[0]
            book_info = item.xpath('td[2]/p[1]/text()').extract()[0]
            book_info_contents = book_info.strip().split(' / ')
            book['author'] = book_info_contents[0]
            book['publisher'] = book_info_contents[1]
            book['edition_year'] = book_info_contents[2]
            book['price'] = book_info_contents[3]
            yield book
