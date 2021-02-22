import scrapy

from scrapy.loader import ItemLoader
from ..items import SparkassemkItem
from itemloaders.processors import TakeFirst


class SparkassemkSpider(scrapy.Spider):
	name = 'sparkassemk'
	start_urls = ['https://sparkasse.mk/Soopshtenija.aspx?IdRoot=1&IdLanguage=1']

	def parse(self, response):
		post_links = response.xpath('//div[@class="box-container__elementsnews"]/a/@href').getall()
		yield from response.follow_all(post_links, self.parse_post)

	def parse_post(self, response):
		title = response.xpath('//span[@class="title"]/text()').get()
		description = response.xpath('//div[@style="width: 100%;"]//text()[normalize-space() and not(ancestor::h2 | ancestor::p[@class="date"] | ancestor::a)]').getall()
		description = [p.strip() for p in description]
		description = ' '.join(description).strip()
		day = response.xpath('//span[@class="day"]//text()').get()
		month = response.xpath('//span[@class="month"]//text()').get()
		year = response.xpath('//span[@class="year"]//text()').get()
		date = day+' '+month+' '+year

		item = ItemLoader(item=SparkassemkItem(), response=response)
		item.default_output_processor = TakeFirst()
		item.add_value('title', title)
		item.add_value('description', description)
		item.add_value('date', date)

		return item.load_item()
