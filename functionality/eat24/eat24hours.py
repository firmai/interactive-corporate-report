# -*- coding: utf-8 -*-
import scrapy
import math


class Eat_hours(scrapy.Spider):
	name = 'eat24hours'
	allowed_domains = ['eat24hours.com']
	start_urls = ['https://cupertino.eat24hours.com/bj-s-brewhouse/43327']

	# custom_settings = {
 #        # 'ROBOTSTXT_OBEY': True,
 #        'USER_AGENT': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:51.0) Gecko/20100101 Firefox/51.0',
 #        # 'COOKIES_ENABLED': False,
 #        # 'DOWNLOADER_MIDDLEWARES': {},
 #        # 'AUTOTHROTTLE_ENABLED': True,
 #        # 'AUTOTHROTTLE_START_DELAY': 5,
 #        # 'AUTOTHROTTLE_MAX_DELAY': 60,
 #        # 'AUTOTHROTTLE_TARGET_CONCURRENCY': 0.5,
 #    }

	def parse(self, response):
		tables = response.xpath('//table[contains(@id,"item_")]')
		for row in tables:
			item = {}
			item['Name'] = row.xpath('.//a[@itemprop="name"]/text()').extract_first()
			item['Price'] = row.xpath('.//span[@itemprop="price"]/text()').extract_first()
			item['Description'] = row.xpath('.//div[@class="item_desc"]/text()').extract_first()
			yield item