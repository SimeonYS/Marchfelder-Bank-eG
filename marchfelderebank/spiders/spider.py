import scrapy
import re
from scrapy.loader import ItemLoader
from scrapy.loader.processors import TakeFirst
from ..items import MarchfelderebankItem

pattern = r'(\r)?(\n)?(\t)?(\xa0)?'

class SpiderSpider(scrapy.Spider):
    name = 'spider'

    start_urls = ['https://www.marchfelderbank.at/private/news']

    def parse(self, response):
        links = response.xpath('//h3/a/@href').getall()
        yield from response.follow_all(links, self.parse_article)

    def parse_article(self, response):
        item = ItemLoader(MarchfelderebankItem())
        item.default_output_processor = TakeFirst()

        title = response.xpath('//h1//text()').get()
        content = response.xpath('//ul[@class="block_list"]//text()').getall()
        content = ' '.join([text.strip() for text in content if text.strip()][:-1])


        item.add_value('title', title)
        item.add_value('link', response.url)
        item.add_value('content', content)
        return item.load_item()
