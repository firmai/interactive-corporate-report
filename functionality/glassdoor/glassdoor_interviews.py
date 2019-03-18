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
            request = scrapy.Request(row['glassdoor_url_interview'], callback=self.parse_first)
            request.meta['Code'] = row['code_or_ticker']
            print(request.meta['Code'])
            yield request


    def parse_first(self, response):
        code_ = response.meta['Code']
        output_file = code_ + '_interview.csv'
        item = {}
        titles = response.xpath('//h2[@class="summary strong noMargTop tightTop margBotXs"]//span/text()').extract()
        interview_dates = response.xpath('//time[@class="date subtle small"]/text()').extract()
        employees = [' '.join(response.xpath('//li[contains(@class,"empReview")][{}]//div[@class="author minor"]//text()'.format(i)).extract()) for i in range(1, 11)]
        offers = [response.xpath('//li[contains(@class,"empReview")][{}]//div[@class="tightLt col span-1-3"][1]//text()'.format(i)).extract() for i in range(1, 11)]
        experiences = [response.xpath('//li[contains(@class,"empReview")][{}]//div[@class="tightLt col span-1-3"][2]//text()'.format(i)).extract() for i in range(1, 11)]
        interview_types = [response.xpath('//li[contains(@class,"empReview")][{}]//div[@class="tightLt col span-1-3"][3]//text()'.format(i)).extract() for i in range(1, 11)]
        applications = [response.xpath('//li[contains(@class,"empReview")][{}]//p[@class="applicationDetails mainText truncateThis wrapToggleStr "]//text()'.format(i)).extract() for i in range(1, 11)]
        interviews = [response.xpath('//li[contains(@class,"empReview")][{}]//p[@class="interviewDetails mainText truncateThis wrapToggleStr "]//text()'.format(i)).extract() for i in range(1, 11)]
        questions = [response.xpath('//li[contains(@class,"empReview")][{}]//span[@class="interviewQuestion noPadVert truncateThis wrapToggleStr "]//text()'.format(i)).extract() for i in range(1, 11)]

        for title, interview_date, employee, offer, experience, interview_type, application, interview, question in zip(titles, interview_dates, employees, offers, experiences, interview_types, applications, interviews, questions):
            item['Title'] = title
            item['Interview Date'] = interview_date
            item['Employee Type'] = employee
            item['Offer'] = offer
            item['Experience'] = experience
            item['Interview Type'] = interview_type
            item['Application'] = application
            item['Interview'] = interview
            item['Question'] = question

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







