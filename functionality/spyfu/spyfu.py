# -*- coding: utf-8 -*-
import csv
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.common.exceptions import TimeoutException, WebDriverException, NoSuchElementException
import selenium.webdriver.support.expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
import requests
import time
import os
import pandas as pd

input_fields = pd.read_csv("../../input_fields.csv")
websites = input_fields["website"]
codes = input_fields["code_or_ticker"]


my_path = os.path.abspath(os.path.dirname('__file__'))

path_out = my_path + "/../../data/spyfu/"

driver = webdriver.Chrome('/usr/local/Cellar/chromedriver/2.33/bin/chromedriver')

for w, c in zip(websites,codes):

	MAIN_URL = 'https://www.spyfu.com/overview/domain?query=' +w

	driver.get(MAIN_URL)

	monthly_domain_overview = driver.find_element_by_xpath('//span[contains(text(),"Monthly Domain Overview")]/following-sibling::a').get_attribute('href')
	organic_keywords = driver.find_element_by_xpath('//div[text()="Organic Keywords"]/following-sibling::div').text
	est_monthly_seo_click = driver.find_element_by_xpath('//div[text()="Est Monthly SEO Clicks"]/following-sibling::div').text.replace('\n','')
	est_monthly_seo_click_value = driver.find_element_by_xpath('//span[text()="Est Monthly SEO Click Value:"]/following-sibling::span').text
	keywords_their_top_competitors_also_rank_for = driver.find_elements_by_xpath('//div[text()="Keywords their top competitors also rank for"]/preceding-sibling::*')[1].text
	ranking_history = driver.find_element_by_xpath('//div[@class="history"]').text

	paid_keywords = driver.find_element_by_xpath('//div[text()="Paid Keywords"]/following-sibling::div').text
	est_monthly_ppc_click = driver.find_element_by_xpath('//div[text()="Est Monthly PPC Clicks"]/following-sibling::div').text.replace('\n','')
	est_monthly_adwords_budget = driver.find_element_by_xpath('//span[text()="Est Monthly AdWords Budget:"]/following-sibling::span').text
	adwords_their_top_competitors_also_buy = driver.find_elements_by_xpath('//div[text()="AdWords their top competitors also buy"]/preceding-sibling::*')[1].text
	adwords_history = driver.find_elements_by_xpath('//div[@class="history"]')[1].text

	just_made_it_to_the_first_page = driver.find_element_by_xpath('//a[@class="just-made-first"]').text.split('\n')[1]
	just_feel_of_first_page = driver.find_element_by_xpath('//a[@class="fell-off-first"]').text.split('\n')[1]

	organic_competitors = ', '.join(driver.find_element_by_xpath('//div[@class="competitors-chart"]').text.split('\n'))
	paid_competitors = ', '.join(driver.find_elements_by_xpath('//div[@class="competitors-chart"]')[1].text.split('\n'))

	shared_organic_keywords = ', '.join(driver.find_element_by_xpath('//div[@class="sf-kombat-diagram"]').text.split('\n'))
	keyword_universe_organic = driver.find_element_by_xpath('//span[contains(text(),"Keyword Universe")]/following-sibling::span').text
	core_starting_keywords = driver.find_element_by_xpath('//span[contains(text(),"Core Starting Keywords")]/following-sibling::span').text
	weakness_organic = driver.find_element_by_xpath('//span[contains(text(),"Weakness")]/following-sibling::span').text
	organic_exclusive_keywords = driver.find_element_by_xpath('//span[contains(text(),"Exclusive Keywords")]/following-sibling::span').text

	shared_paid_keywords = ', '.join(driver.find_elements_by_xpath('//div[@class="sf-kombat-diagram"]')[1].text.split('\n'))
	keyword_universe_paid = driver.find_elements_by_xpath('//span[contains(text(),"Keyword Universe")]/following-sibling::span')[1].text
	core_niche_paid = driver.find_element_by_xpath('//span[contains(text(),"Core Niche")]/following-sibling::span').text
	buy_recommendations = driver.find_element_by_xpath('//span[contains(text(),"Buy Recommendations")]/following-sibling::span').text
	paid_exclusive_keywords = driver.find_elements_by_xpath('//span[contains(text(),"Exclusive Keywords")]/following-sibling::span')[1].text

	top_keywords_organic = [('Rank = {}'.format(i.text.split('\n')[0]), 'Keyword = {}'.format(i.text.split('\n')[1]), 'Cliks/Mo = {}'.format(i.text.split('\n')[2])) for i in driver.find_elements_by_xpath('//tr[@class="sf-global-component sf-table-row"]')[:5]]
	top_keywords_paid = [('Paid Keywords = {}'.format(i.text.split('\n')[0]), 'Cost Per Click = {}'.format(i.text.split('\n')[1]), 'Monthly Cost = {}'.format(i.text.split('\n')[2])) for i in driver.find_elements_by_xpath('//tr[@class="sf-global-component sf-table-row"]')[5:10]]

	inbound_links = [('Backlink = {}'.format(i.text.split('\n')[0]), 'Domain Organic Clicks = {}'.format(i.text.split('\n')[1]), 'Page Organic Clicks = {}'.format(i.text.split('\n')[2]), 'Domain Strength = {}'.format(i.text.split('\n')[3]), 'Ranked Keywords = {}'.format(i.text.split('\n')[4]), 'Outbound Links = {}'.format(i.text.split('\n')[5])) for i in driver.find_elements_by_xpath('//table[@class="sf-table sf-backlinks-table"]/tr')[1:6]]
	top_keywords_history = [('Rank = {}'.format(i.text.split('\n')[0]), 'Keyword = {}'.format(i.text.split('\n')[1])) for i in driver.find_elements_by_xpath('//div[contains(@class,"legend-entry")]')[:5]]



	data = {'Monthly Domain Overview': monthly_domain_overview, 'Organic Keywords': organic_keywords,
		'Est Monthly Seo Click': est_monthly_seo_click, 'Est Monthly Seo Click Value': est_monthly_seo_click_value,
		'Keywords Their Top Competitors Also Rank For': keywords_their_top_competitors_also_rank_for,
		'Ranking History': ranking_history, 'Paid Keywords': paid_keywords, 'Est Monthly PPC Click': est_monthly_ppc_click,
		'Est Monthly AdWords Budget': est_monthly_adwords_budget,
		'AdWords Their Top Competitors Also Buy': adwords_their_top_competitors_also_buy,
		'AdWords History': adwords_history, 'Just Made It To The First Page': just_made_it_to_the_first_page,
		'Just Feel Of First Page': just_feel_of_first_page, 'Organic Competitors': organic_competitors,
		'Paid Competitors': paid_competitors, 'Shared Organic Keywords': shared_organic_keywords,
		'Keyword Universe Organic': keyword_universe_organic, 'Core Starting Keywords': core_starting_keywords,
		'Weakness Organic': weakness_organic, 'Organic Exclusive Keywords': organic_exclusive_keywords,
		'Shared Paid Keywords': shared_paid_keywords, 'Keyword Universe Paid': keyword_universe_paid,
		'Core Niche Paid': core_niche_paid, 'Buy Recommendations': buy_recommendations,
		'Paid Exclusive Keywords': paid_exclusive_keywords, 'Top Keywords Organic': top_keywords_organic,
		'Top Keywords Paid': top_keywords_paid, 'Inbound Links': inbound_links, 'Top Keywords History': top_keywords_history}

	with open(path_out+c+'_spyfu.csv', 'a', encoding='utf-8', newline='') as f:
		writer = csv.DictWriter(f, fieldnames=data.keys())
		if not os.fstat(f.fileno()).st_size > 0:
			writer.writeheader()
		writer.writerow(data)

	print('Done')
