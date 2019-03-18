# -*- coding: utf-8 -*-
import scrapy
import math
import os
import csv

class GlassDoor(scrapy.Spider):
    name = 'glassdoor'
    allowed_domains = ['glassdoor.com']

    my_path = os.path.abspath(os.path.dirname(__file__))
    path = os.path.join(my_path, "../../input_fields.csv")
    a = csv.DictReader(open(path, 'r', encoding='utf-8'))
    #for row in a:
    #    print(row)
    print(a)
    start_urls = ['https://www.glassdoor.com/index.htm']

    def parse(self, response):
        for row in self.a:
            request = scrapy.Request(row['glassdoor_ben'], callback=self.parse_first)
            request.meta['Code'] = row['code_or_ticker']
            print(request.meta['Code'])
            yield request

    def parse_first(self, response):
        code_ = response.meta['Code']
        output_file = code_ + '_benefits.csv'
        ratings = [response.xpath('//li[contains(@class,"benefitReview")][{}]//span[@class="rating"]/span/@title'.format(i)).extract() for i in range(1, 11)]
        review_dates = response.xpath('//div[@class="dtreviewed minor date"]/text()').extract()
        employees = [' '.join(response.xpath('//li[contains(@class,"benefitReview")][{}]//span[@class="authorInfo minor cell middle"]//text()'.format(i)).extract()) for i in range(1, 11)]
        descriptions = [response.xpath('//li[contains(@class,"benefitReview")][{}]//p[contains(@class,"description")]//text()'.format(i)).extract() for i in range(1, 11)]

        for rating, review_date, employee, description in zip(ratings, review_dates, employees, descriptions):
            item = {}
            item['Rating'] = rating[0]
            item['Review Date'] = review_date.strip()
            item['Employee'] = employee.strip()
            item['Description'] = description

            my_path = os.path.abspath(os.path.dirname(__file__))
            path_out = os.path.join(my_path, "../../data/glassdoor/"+ output_file)
            print(path_out)

            with open(path_out, 'a', encoding='utf-8', newline='') as f:
                writer = csv.DictWriter(f, fieldnames=item.keys())
                if not os.fstat(f.fileno()).st_size > 0:
                    writer.writeheader()
                writer.writerow(item)

        next_page = response.xpath('//li[@class="next"]//@href').extract_first()
        if next_page is not None:
            next_page = response.urljoin(next_page)
            request = scrapy.Request(next_page, callback=self.parse_first)
            request.meta['Code'] = code_
            yield request





