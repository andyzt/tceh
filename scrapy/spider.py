import scrapy
from scrapy.loader import ItemLoader
from scrapy.loader.processors import Join, MapCompose, TakeFirst

def parse_category(my_str):
    return my_str[0].split(' ')[3]

class Article(scrapy.Item):
    category = scrapy.Field(

        output_processor=TakeFirst()
    )
    title2 = scrapy.Field()



class BlogSpider(scrapy.Spider):
    name = 'blogspider'
    start_urls = ['https://blog.scrapinghub.com']

    def parse(self, response):
        for url in response.css('ul li a::attr("href")').re('.*/category/.*'):
            yield scrapy.Request(response.urljoin(url), self.parse_titles)

    def parse_titles(self, response):
        l = ItemLoader(item=Article(), response=response)
        l.add_css('category', 'h1.pagetitle::text', parse_category)
        l.add_css('title2', 'div.entries > ul > li a::text')
        return l.load_item()
