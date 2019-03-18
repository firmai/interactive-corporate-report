# -*- coding: utf-8 -*-
import scrapy
import math
import csv
import os


class GlassDoor(scrapy.Spider):
    name = 'glassdoor'
    allowed_domains = ['glassdoor.com']

    my_path = os.path.abspath(os.path.dirname(__file__))
    path = os.path.join(my_path, "../../input_fields.csv")
    a = csv.DictReader(open(path, 'r', encoding='utf-8'))
    #for row in a:
    #    print(row)

    # a = csv.DictReader(open('input_fields.csv', 'r', encoding='utf-8'))
    start_urls = ['https://www.glassdoor.com/index.htm']

    def parse(self, response):
        for row in self.a:
            request = scrapy.Request(row['glassdoor_url_jobs'], callback=self.parse_first)
            request.meta['Code'] = row['code_or_ticker']
            print(request.meta['Code'])
            yield request

    def parse_first(self, response):
        code_ = response.meta['Code']
        output_file = code_ + '_jobs.csv'
        
        titles = response.xpath('//li[@class="jl"]//a[@class="jobLink"]/text()').extract()
        locations = response.xpath('//span[@class="subtle loc"]/text()').extract()
        dates = response.xpath('//span[@class="hideHH nowrap"]/span[@class="minor"]/text()').extract()
        for title, location, date in zip(titles, locations, dates):
            item = {}
            item['Title'] = title
            item['Location'] = location
            item['Date'] = date

            my_path = os.path.abspath(os.path.dirname(__file__))
            path_out = os.path.join(my_path, "../../data/glassdoor/" + output_file)
            print(path_out)

            with open(path_out, 'a', encoding='utf-8', newline='') as f:
                writer = csv.DictWriter(f, fieldnames=item.keys())
                if not os.fstat(f.fileno()).st_size > 0:
                    writer.writeheader()
                writer.writerow(item)






