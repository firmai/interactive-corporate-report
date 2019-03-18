# -*- coding: utf-8 -*-
import scrapy
import math
import csv
import os
from fake_useragent import UserAgent
from random import choice
from scrapy.spidermiddlewares.httperror import HttpError
from twisted.internet.error import TimeoutError 


class Yelp(scrapy.Spider):
	name = 'yelp'
	allowed_domains = ['yelp.com']
	csv_files = ['BJRI_locations.csv']
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
        'DOWNLOAD_DELAY': 2,
        'DOWNLOAD_TIMEOUT': '30',
        # 'DOWNLOADER_MIDDLEWARES': {
        #     'scrapy.downloadermiddlewares.httpproxy.HttpProxyMiddleware': 1,}

    }

	def start_requests(self):
		for csv_file in self.csv_files:
			my_path = os.path.abspath(os.path.dirname('__file__'))
			path_out = my_path + "/functionality/yelp/"
			a = csv.DictReader(open(path_out + csv_file, 'r', encoding='utf-8'))
			for row in a:
				link = row['Link'].split('/')[-1]
				urls = ['https://nz.yelp.com/search?cflt=newamerican&find_near=', 'https://nz.yelp.com/search?cflt=breweries&find_near=', 'https://nz.yelp.com/search?cflt=pizza&find_near=']
				for url in urls:
					url = url + link
					user_agent = UserAgent().random
					headers = {'User-Agent': user_agent}
					request = scrapy.Request(url, callback=self.parse, headers=headers)
					request.meta['proxy'] = "192.241.138.179:8080"
					yield request

	def parse(self, response):
		output_file = response.url.split('=')[-1].split('?start=')[0] + '.csv'
		companies = response.xpath('//li[@class="regular-search-result"]//div[@class="main-attributes"]//div[@class="media-story"]')
		for comp in companies:
			name = comp.xpath('.//a[contains(@class,"biz-name")]//text()').extract_first()
			try:
				rating = comp.xpath('.//div[contains(@class,"i-stars i-stars")]/@title').extract_first().split()[0]
			except AttributeError:
				rating = ''
			try:
				reviews = comp.xpath('.//span[contains(@class,"review-count")]/text()').extract_first().strip().split()[0]
			except AttributeError:
				reviews = ''
			comp_link = response.urljoin(comp.xpath('.//a[contains(@class,"biz-name")]/@href').extract_first())
			try:
				distance = [i.strip() for i in comp.xpath('.//li[@class="tag-18x18_marker-error"]/small/text()').extract() if i.strip()][0]
			except IndexError:
				distance = ''
			descr = [i.strip() for i in comp.xpath('.//span[@class="category-str-list"]//text()').extract() if i.strip() != ',' and i.strip()]
			data = {'Name': name, 'Rating': rating, 'Reviews': reviews, 'Link': comp_link, 'Distance': distance, 'Description': descr}
			with open(output_file, 'a', encoding='utf-8', newline='') as f:
				writer = csv.DictWriter(f, fieldnames=data.keys())
				if not os.fstat(f.fileno()).st_size > 0:
					writer.writeheader()
				writer.writerow(data)


