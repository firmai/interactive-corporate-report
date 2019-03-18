# -*- coding: utf-8 -*-
import scrapy
import math
import csv
import os
from fake_useragent import UserAgent 


class Yelp(scrapy.Spider):
	name = 'yelp'
	allowed_domains = ['yelp.com']
	csv_files = ['TGIF_locations.csv']
	user_agent = UserAgent().random
	

	custom_settings = {
        # 'ROBOTSTXT_OBEY': True,
        'USER_AGENT': user_agent,
        # 'COOKIES_ENABLED': False,
        # 'DOWNLOADER_MIDDLEWARES': {},
        # 'AUTOTHROTTLE_ENABLED': True,
        # 'AUTOTHROTTLE_START_DELAY': 5,
        # 'AUTOTHROTTLE_MAX_DELAY': 60,
        # 'AUTOTHROTTLE_TARGET_CONCURRENCY': 0.5,
        'DOWNLOAD_DELAY': 1,
        'DOWNLOADER_MIDDLEWARES': {
            'scrapy.downloadermiddlewares.httpproxy.HttpProxyMiddleware': 1,
        }

    }
	def start_requests(self):
		for csv_file in self.csv_files:
			a = csv.DictReader(open(csv_file, 'r', encoding='utf-8'))
			for row in a:
				url = row['Link']
				request = scrapy.Request(url, callback=self.parse)
				request.meta['proxy'] = "103.241.206.252:8081"
				yield request

	def parse(self, response):
		try:
			page_count = response.xpath('//div[contains(@class,"page-of-pages")]/text()').extract_first().strip().split()[-1]
		except AttributeError:
			page_count = 1
		item = {}
		item['Url'] = response.url
		item['Page'] = page_count
		yield item
		