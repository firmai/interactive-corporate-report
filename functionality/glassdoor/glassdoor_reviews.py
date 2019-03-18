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

    #a = csv.DictReader(open('input_fields.csv', 'r', encoding='utf-8'))
    start_urls = ['https://www.glassdoor.com/index.htm']


    def parse(self, response):
        for row in self.a:
            request = scrapy.Request(row['glassdoor_url_review'], callback=self.parse_first)
            request.meta['Code'] = row['code_or_ticker']
            yield request

    def parse_first(self, response):
        # output_file = response.url.split('/')[-1].split('.')[0].split('_P')[0] + '.csv'
        code_ = response.meta['Code']
        output_file = code_ + '_review.csv'
        item = {}
        titles = response.xpath('//h2[@class=" h2 summary strong tightTop margBotXs"]//span/text()').extract()
        ratings = response.xpath('//div[@id="EmployerReviews"]//span[@class="value-title"]/@title').extract()
        review_dates = response.xpath('//time[@class="date subtle small"]/text()').extract()
        current_past_employees = []
        for i in response.xpath('//span[@class="authorJobTitle middle reviewer"]/text()').extract():
            if i.startswith('Current'):
                cur_past = 'Current'
            elif i.startswith('Former'):
                cur_past = 'Past'
            else:
                cur_past = ''
            current_past_employees.append(cur_past)
        employee_titles = [i.split('-')[-1].strip() for i in response.xpath('//span[@class="authorJobTitle middle reviewer"]/text()').extract()]
        # locations = response.xpath('//span[@class="authorLocation middle"]/text()').extract()
        locations = []
        employees = response.xpath('//span[@class="authorInfo tbl hideHH"]').extract()
        for i in employees:
            if len(i.split('</span>')) == 3:
                location = ''
            else:
                location = i.split('Location middle">')[-1].split('</span')[0]
            locations.append(location)
        recommends_list = []
        outlooks_list = []
        approves_list = []
        recommends = response.xpath('//div[@class="flex-grid recommends"]').extract()
        for i in recommends:
            if 'Recommends' in i:
                rec1 = 'Yes'
            elif "Doesn't Recommend" in i:
                rec1 = 'No'
            else:
                rec1 = 'Neutral'
            recommends_list.append(rec1)
        for i in recommends:
            if 'Positive Outlook' in i:
                rec2 = 'Yes'
            elif 'Negative Outlook' in i:
                rec2 = 'No'
            else:
                rec2 = 'Neutral'
            outlooks_list.append(rec2)
        for i in recommends:
            if 'Approves of' in i:
                rec3 = 'Yes'
            elif 'Disapproves of CEO' in i:
                rec3 = 'No'
            else:
                rec3 = 'Neutral'
            approves_list.append(rec3)
        full_part_time_list = []
        for i in response.xpath('//p[@class=" tightBot mainText"]/text()').extract():
            if 'part-time' in i:
                full_part_time = 'Part-time'
            elif 'full-time' in i:
                full_part_time = 'Full-time'
            else:
                full_part_time = ''
            full_part_time_list.append(full_part_time)
        time_employeed_list = []
        for i in response.xpath('//p[@class=" tightBot mainText"]/text()').extract():
            if '(' in i:
                time_employeed = i.split('(')[-1].split(')')[0].strip()
            else:
                time_employeed = ''
            time_employeed_list.append(time_employeed)
        pros_list = []
        # for i in response.xpath('//p[@class=" pros mainText truncateThis wrapToggleStr"]').extract():
        #     pros_list.append(i.split('">')[-1].split('</p>')[0])
        cons_list = []
        # for i in response.xpath('//p[@class=" cons mainText truncateThis wrapToggleStr"]').extract():
        #     cons_list.append(i.split('">')[-1].split('</p>')[0])
        advice_list = []
        # for i in response.xpath('//p[@class=" adviceMgmt mainText truncateThis wrapToggleStr"]').extract():
        #     advice_list.append(i.split('">')[-1].split('</p>')[0])
        pros_cons_advice = response.xpath('//div[@class=" tbl fill prosConsAdvice truncateData"]').extract()
        for i in pros_cons_advice:
            if '>Pros<' in i:
                pros = i.split('pros mainText truncateThis wrapToggleStr">')[-1].split('</p>')[0]
            else:
                pros = ''
            pros_list.append(pros)
        for i in pros_cons_advice:
            if '>Cons<' in i:
                cons = i.split('cons mainText truncateThis wrapToggleStr">')[-1].split('</p>')[0]
            else:
                cons = ''
            cons_list.append(cons)
        for i in pros_cons_advice:
            if '>Advice to Management<' in i:
                advice = i.split('adviceMgmt mainText truncateThis wrapToggleStr">')[-1].split('</p>')[0]
            else:
                advice = ''
            advice_list.append(advice)
        work_life_balances = [response.xpath('//li[contains(@class,"empReview")][{}]//ul[@class="undecorated"]/li[1]/span/@title'.format(i)).extract_first() for i in range(1, 11)]
        culture_values = [response.xpath('//li[contains(@class,"empReview")][{}]//ul[@class="undecorated"]/li[2]/span/@title'.format(i)).extract_first() for i in range(1, 11)]
        career_opportunities = [response.xpath('//li[contains(@class,"empReview")][{}]//ul[@class="undecorated"]/li[3]/span/@title'.format(i)).extract_first() for i in range(1, 11)]
        comp_benefits = [response.xpath('//li[contains(@class,"empReview")][{}]//ul[@class="undecorated"]/li[4]/span/@title'.format(i)).extract_first() for i in range(1, 11)]
        senior_managements = [response.xpath('//li[contains(@class,"empReview")][{}]//ul[@class="undecorated"]/li[5]/span/@title'.format(i)).extract_first() for i in range(1, 11)]
        
        for title, rating, work_life_balance, culture_value, career_opportunity, comp_benefit, senior_management, review_date, current_past_employee, employee_title, location, recommends_, outlook, approve, full_part_time_, time_employeed_, pros_, cons_, advice_ in zip(titles, ratings, work_life_balances, culture_values, career_opportunities, comp_benefits, senior_managements, review_dates, current_past_employees, employee_titles, locations, recommends_list, outlooks_list, approves_list, full_part_time_list, time_employeed_list, pros_list, cons_list, advice_list):
            item['Title'] = title
            item['Rating'] = rating
            item['Work Life Balance'] = work_life_balance
            item['Culture Values'] = culture_value
            item['Career Opportunities'] = career_opportunity
            item['Comp Benefits'] = comp_benefit
            item['Senior Management'] = senior_management
            item['Review Date'] = review_date
            item['Current or Past Employee'] = current_past_employee
            item['Employee Title'] = employee_title
            item['Location'] = location
            item['Recommends'] = recommends_
            item['Outlook'] = outlook
            item['Approves of CEO'] = approve
            item['Full-Time or Part-Time'] = full_part_time_
            item['Time Employeed']= time_employeed_
            item['Pros'] = pros_
            item['Cons'] = cons_
            item['Advice to Management'] = advice_
            with open("../../data/glassdoor" + output_file, 'a', encoding='utf-8', newline='') as f:
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







