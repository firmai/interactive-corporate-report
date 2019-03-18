# -*- coding: utf-8 -*-
from selenium import webdriver
import os
import csv
import selenium
import time
import pandas as pd

input_fields = pd.read_csv("../../input_fields.csv")
websites = input_fields["website"]
codes = input_fields["code_or_ticker"]

websites =["https://www.tgifridays.com/"]

codes =[
"TGIF"]

my_path = os.path.abspath(os.path.dirname('__file__'))

path_out = my_path + "/../../data/similarweb/"

for w, c in zip(websites,codes):

	driver = webdriver.Chrome('/usr/local/Cellar/chromedriver/2.33/bin/chromedriver')
	driver.get('https://www.similarweb.com/website/' +w)
	for i in range(0, 20000, 100):
		driver.execute_script("window.scrollTo(0, {});".format(i))
		time.sleep(1)


	headline = driver.find_element_by_xpath('//span[@itemprop="headline"]').text
	overview_date = driver.find_element_by_xpath('//span[@class="websiteHeader-dateFull"]').text
	global_rank = driver.find_element_by_xpath('//li[contains(@class,"globalRank")]/div[contains(@class,"valueContainer")]').text
	country_rank = driver.find_element_by_xpath('//li[contains(@class,"countryRank")]/div[contains(@class,"valueContainer")]').text
	category_rank = driver.find_element_by_xpath('//li[contains(@class,"categoryRank")]/div[contains(@class,"valueContainer")]').text
	total_visits = driver.find_element_by_xpath('//div[@data-type="visits"]//span[contains(@class,"countValue")]').text
	avg_visit_duration = driver.find_element_by_xpath('//span[@data-type="time"]/span').text
	pages_per_visit = driver.find_element_by_xpath('//span[@data-type="ppv"]/span').text
	bounce_rate = driver.find_element_by_xpath('//span[@data-type="bounce"]/span').text
	traffic_by_countries_names = [i.text for i in driver.find_elements_by_xpath('//span[contains(@class,"country-container")]/a')]
	traffic_by_countries_values = [i.text for i in driver.find_elements_by_xpath('//span[contains(@class,"traffic-share-value")]/span')]
	traffic_by_countries = list(zip(traffic_by_countries_names, traffic_by_countries_values))

	traffic_sources_texts = [i.text for i in driver.find_elements_by_xpath('//span[@class="trafficSourcesChart-text"] | //a[@class="trafficSourcesChart-reference js-goToSection"]')]
	traffic_sources_values = [i.text for i in driver.find_elements_by_xpath('//div[@class="trafficSourcesChart-value"]')]
	traffic_sources = list(zip(traffic_sources_texts, traffic_sources_values))
	lastamt = driver.find_element_by_xpath('//g[@class="highcharts-tooltip"]/text/tspan[3]').text
	referrals_percent = driver.find_element_by_xpath('//span[@class="subheading-value referrals"]').text
	top_referring_sites_names = [i.text for i in driver.find_elements_by_xpath('//div[@class="referralsSites referring"]//ul[@class="websitePage-list"]//div[@class="websitePage-listItemTitle"]/a')]
	top_referring_sites_values = [i.text for i in driver.find_elements_by_xpath('//div[@class="referralsSites referring"]//ul[@class="websitePage-list"]//span[@class="websitePage-trafficShare"]')]
	top_referring_sites = list(zip(top_referring_sites_names, top_referring_sites_values))
	top_destination_sites_names = [i.text for i in driver.find_elements_by_xpath('//div[@class="referralsSites destination"]//ul[@class="websitePage-list"]//div[@class="websitePage-listItemTitle"]/a')]
	top_destination_sites_values = [i.text for i in driver.find_elements_by_xpath('//div[@class="referralsSites destination"]//ul[@class="websitePage-list"]//span[@class="websitePage-trafficShare"]')]
	top_destination_sites = list(zip(top_destination_sites_names, top_destination_sites_values))

	search_percent = driver.find_element_by_xpath('//span[@class="subheading-value searchText"]').text
	organic_keywords_percent = driver.find_element_by_xpath('//div[@class="searchPie-text searchPie-text--left  "]/span[@class="searchPie-number"]').text
	paid_keywords_percent = driver.find_element_by_xpath('//div[@class="searchPie-text searchPie-text--right  "]/span[@class="searchPie-number"]').text

	top_5_organic_keywords_words = [i.text for i in driver.find_elements_by_xpath('//div[contains(@class,"searchKeywords-text searchKeywords-text--left")]//span[@class="searchKeywords-words"]')]
	top_5_organic_keywords_values = [i.text for i in driver.find_elements_by_xpath('//div[contains(@class,"searchKeywords-text searchKeywords-text--left")]//span[@class="searchKeywords-trafficShare"]')]
	top_5_organic_keywords = list(zip(top_5_organic_keywords_words, top_5_organic_keywords_values))
	top_5_paid_keywords_words = [i.text for i in driver.find_elements_by_xpath('//div[contains(@class,"searchKeywords-text searchKeywords-text--right")]//span[@class="searchKeywords-words"]')]
	top_5_paid_keywords_values = [i.text for i in driver.find_elements_by_xpath('//div[contains(@class,"searchKeywords-text searchKeywords-text--right")]//span[@class="searchKeywords-trafficShare"]')]
	top_5_paid_keywords = list(zip(top_5_paid_keywords_words, top_5_paid_keywords_values))

	social_percent = driver.find_element_by_xpath('//span[@class="subheading-value social"]').text
	social_items_names = [i.text for i in driver.find_elements_by_xpath('//ul[@class="socialList"]//a[@class="socialItem-title name link"]')]
	social_items_values = [i.text for i in driver.find_elements_by_xpath('//ul[@class="socialList"]//div[@class="socialItem-value"]')]
	social_items = list(zip(social_items_names, social_items_values))
	try:
		display_advertising_percent = driver.find_element_by_xpath('//span[@class="subheading-value display"]').text
	except:
		display_advertising_percent = None
	top_publishers = [i.text for i in driver.find_elements_by_xpath('//div[@class="websitePage-engagementInfo"]//a[@class="js-tooltipTarget websitePage-listItemLink"]')]

	website_contents_subdomains_texts = [i.text for i in driver.find_elements_by_xpath('//div[@class="websiteContent-tableLine"]//span[@class="websiteContent-itemText"]')]
	website_contents_subdomains_values = [i.text for i in driver.find_elements_by_xpath('//div[@class="websiteContent-tableLine"]//span[@class="websiteContent-itemPercentage js-value"]')]
	website_contents_subdomains = list(zip(website_contents_subdomains_texts, website_contents_subdomains_values))

	also_visited_websites = [i.text for i in driver.find_elements_by_xpath('//section[contains(@class,"alsoVisitedSection")]//a[@class="js-tooltipTarget websitePage-listItemLink"]')]
	similarity_sites = [i.get_attribute('data-site') for i in driver.find_elements_by_xpath('//li[@class="similarSitesList-item"]')]

	data = {'Headline': headline,'ffff': lastamt, 'Overview Date': overview_date, 'Global Rank': global_rank,
		'Country Rank': country_rank, 'Category Rank': category_rank, 'Total Visits': total_visits,
		'Avg Visit Duration': avg_visit_duration, 'Pages Per Visit': pages_per_visit, 'Bounce Rate': bounce_rate,
		'Traffic By Countries': traffic_by_countries, 'Traffic Sources': traffic_sources, 'Referrals Percent': referrals_percent, 'Top Referring Sites': top_referring_sites,
		'Top Destination Sites': top_destination_sites, 'Search Percent': search_percent, 'Organic Keywords Percent': organic_keywords_percent,
		'Paid Keywords Percent': paid_keywords_percent, 'Top 5 Organic Keywords': top_5_organic_keywords,
		'Top 5 Paid Keywords': top_5_paid_keywords, 'Social Percent': social_percent, 'Social Items': social_items,
		'Display Advertising Percent': display_advertising_percent, 'Top Publishers': top_publishers,
		'Website Contents Subdomains': website_contents_subdomains, 'Also Visited Websites': also_visited_websites,
		'Similarity Sites': similarity_sites}
	with open(path_out + c +'_similarweb.csv', 'a', encoding='utf-8', newline='') as f:
		writer = csv.DictWriter(f, fieldnames=data.keys())
		if not os.fstat(f.fileno()).st_size > 0:
			writer.writeheader()
		writer.writerow(data)

	print('done')