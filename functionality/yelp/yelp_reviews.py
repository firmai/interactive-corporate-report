# -*- coding: utf-8 -*-
import scrapy
import math
import csv
import os


os.makedirs(os.path.dirname("../files_yelp/"), exist_ok=True)

class Yelp(scrapy.Spider):
	name = 'yelp'
	allowed_domains = ['yelp.com']
	csv_files = ['APPB_locations.csv', 'BJRI_locations.csv', 'CAKE_locations.csv',
				'CHIL_locations.csv', 'CPKI_locations.csv', 'RRGB_locations.csv',
				'TGIF_locations.csv']
	

	custom_settings = {
        # 'ROBOTSTXT_OBEY': True,
        'USER_AGENT': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:51.0) Gecko/20100101 Firefox/51.0',
        # 'COOKIES_ENABLED': False,
        # 'DOWNLOADER_MIDDLEWARES': {},
        # 'AUTOTHROTTLE_ENABLED': True,
        # 'AUTOTHROTTLE_START_DELAY': 5,
        # 'AUTOTHROTTLE_MAX_DELAY': 60,
        # 'AUTOTHROTTLE_TARGET_CONCURRENCY': 0.5,
        'DOWNLOAD_DELAY': 1,

    }
	def start_requests(self):
		for csv_file in self.csv_files:
			a = csv.DictReader(open(csv_file, 'r', encoding='utf-8'))
			for row in a:
				url = row['Link']
				yield scrapy.Request(url, callback=self.parse)

	def parse(self, response):
		output_file = response.url.split('/')[-1].replace('?start=20', '') + '.csv'
		reviews = response.xpath('//ul[@class="ylist ylist-bordered reviews"]/li')
		for review in reviews:
			item = {}
			username = review.xpath('.//a[contains(@class,"user-display-name")]/text()').extract_first()
			location = review.xpath('.//li[contains(@class,"user-location")]/b/text()').extract_first()
			friend_count = review.xpath('.//li[contains(@class,"friend-count")]/b/text()').extract_first()
			review_count = review.xpath('.//li[contains(@class,"review-count")]/b/text()').extract_first()
			photo_count = review.xpath('.//li[contains(@class,"photo-count")]/b/text()').extract_first()
			try:
				rating = review.xpath('.//div[contains(@class,"i-stars")]/@title').extract_first().split()[0].strip()
			except AttributeError:
				rating = ''
			try:
				date = review.xpath('.//span[@class="rating-qualifier"]/text()').extract_first().strip()
			except AttributeError:
				date = ''
			review_text = ' '.join(review.xpath('.//div[@class="review-content"]/p/text()').extract())
			item['Username'] = username
			item['location'] = location
			item['friend_count'] = friend_count
			item['review_count'] = review_count
			item['photo_count'] = photo_count
			item['rating'] = rating
			item['date'] = date
			item['review'] = review_text
			if item['Username']:

				my_path = os.path.abspath(os.path.dirname(__file__))
				path_out = os.path.join(my_path, "../../data/yelp/" + output_file)
				print(path_out)

				with open("../files_yelp/"+output_file, 'a', encoding='utf-8', newline='') as f:
					writer = csv.DictWriter(f, fieldnames=item.keys())
					if not os.fstat(f.fileno()).st_size > 0:
						writer.writeheader()
					writer.writerow(item)
		next_page = response.xpath('//a[contains(@class,"next")]/@href').extract_first()
		if next_page:
			url = response.urljoin(next_page)
			yield scrapy.Request(url, callback=self.parse)

