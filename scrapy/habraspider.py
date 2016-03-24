# -*- coding: utf-8 -*-

import scrapy
from scrapy.loader import ItemLoader
from scrapy.loader.processors import Join, MapCompose, TakeFirst
from scrapy.exceptions import DropItem
from bs4 import BeautifulSoup
import arrow
import datetime

MY_DATE = u'9 марта'

ITEM_PIPELINES = {
    'habraspider.DatePipeline': 1,
}

class MyEncode(object):

    def __call__(self, values):
        res = []
        for value in values:
            soup = BeautifulSoup(value, 'html.parser', from_encoding="utf-8")
            enc_str = soup.get_text()
            res.append(enc_str)
        return res

class InputEncode(object):

    def __call__(self, values):
        res = []
        for value in values:
            enc_str = u''+value
            res.append(enc_str)
        return res


class Post(scrapy.Item):
    post_date = scrapy.Field(
        input_processor=InputEncode(),
        output_processor=MyEncode())

    post_text = scrapy.Field(
        input_processor=InputEncode(),
        output_processor=MyEncode())


class DatePipeline(object):
    def process_item(self, item, spider):
        print item['post_date']
        if MY_DATE not in item['post_date']:
                raise DropItem("Duplicate item found: %s" % item)
        else:
            return item

class BlogSpider(scrapy.Spider):
    name = 'habraspider'
    start_urls = ['https://habrahabr.ru/users/zelenin/']
    custom_settings = {
        'ITEM_PIPELINES': {
            'habraspider.DatePipeline': 1
        }

    def parse(self, response):
        for url in response.css('ul#hubs_data_items.grey li a::attr("href")').re('.*/hub/.*'):
            print url
            yield scrapy.Request(response.urljoin(url), self.parse_hubs)

    def parse_hubs(self, response):
        l = ItemLoader(item=Post(), response=response)
        l.add_css('post_date', 'div.posts_list div.published::text')
        l.add_css('post_text', 'div.content.html_format::text')
        return l.load_item()

    """
    def parse(self, response):
        for sel in response.xpath('//*[@id="archief"]/ul/li'):
            item = NosItem()
            item['name'] = sel.xpath('a/@href').extract()[0]
            item['date'] = sel.xpath('a/div[1]/time/@datetime').extract()[0]
            item['desc'] = sel.xpath('a/div[@class="list-time__title link-hover"]/text()').extract()[0]
            url = response.urljoin(item['name'])
            request = scrapy.Request(url, callback=self.parse_dir_contents)
            request.meta['item'] = item
            yield request
    """


#   local = arrow.get('2015-05-11T21:23:58.970460+00:00')
#   print local.format('DD MMMM YYYY',locale='ru_RU')