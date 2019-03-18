# -*- coding: utf-8 -*-
from selenium import webdriver
import os
import csv
from lxml import html
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.common.exceptions import TimeoutException, WebDriverException, NoSuchElementException, ElementNotVisibleException
import selenium.webdriver.support.expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.chrome.options import Options

driver = webdriver.Chrome('/usr/local/Cellar/chromedriver/2.33/bin/chromedriver')

driver.get('https://angel.co/restaurants-1')

while True:
	WebDriverWait(driver, 10).until(EC.visibility_of_element_located((By.XPATH, '//div[@class="more hidden"]')))
	more = driver.find_element_by_xpath('//div[@class="more hidden"]')
	more.click()
tree = html.fromstring(driver.page_source)

names = tree.xpath('//a[@class="startup-link"]/text()')
cities = tree.xpath('//div[@class="tags"]/a[1]/text()')
types = [i.xpath('./a[2]/text()') for i in tree.xpath('//div[@class="tags"]')]
descriptions = [i.strip() for i in tree.xpath('//div[@class="blurb"]/text()')]
joins = [i.strip() for i in tree.xpath('//div[@class="column joined"]/div[@class="value"]/text()')]
followers = [i.strip() for i in tree.xpath('//div[@class="column followers"]/div[@class="value"]/text()')]

for name, city, type_, desc, join, fol in zip(names, cities, types, descriptions, joins, followers):
	try:
		t = type_[0]
	except IndexError:
		t = ''
	data = {'name':name, 'city':city, 'type':t, 'description': desc, 'joined':join, 'followers': fol}

	with open('angel.csv', 'a', encoding='utf-8', newline='') as f:
		writer = csv.DictWriter(f, fieldnames=data.keys())
		if not os.fstat(f.fileno()).st_size > 0:
			writer.writeheader()
		writer.writerow(data)
