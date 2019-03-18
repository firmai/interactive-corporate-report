# -*- coding: utf-8 -*-
from selenium import webdriver
import os
import csv
import selenium
from lxml import html
import pandas as pd
import os
driver = webdriver.Chrome('/usr/local/Cellar/chromedriver/2.33/bin/chromedriver')


input_fields = pd.read_csv("input_fields.csv")
short = input_fields["short_name"]
codes = input_fields["code_or_ticker"]
all_codes = list(codes)
all_codes.remove("APPB")
all_codes.remove("BJRI")
all_codes.remove("CHIL")
all_codes.remove("CAKE")
for coy in all_codes:
	my_path = os.path.abspath(os.path.dirname('__file__'))
	path_in_door = os.path.join(my_path, "../../data/doordash/")

	d_frame = pd.read_csv(path_in_door +coy+"_locations.csv")
	print(my_path + "/../../data/doordash/"+coy+"/")
	import pathlib
	pathlib.Path(my_path + "/../../data/doordash/"+coy+"/").mkdir(parents=True, exist_ok=True)

	path_out_door = os.path.join(my_path, "../../data/doordash/"+coy+"/")

	for r in d_frame["Link"]:
		print(r)
		url = r
		driver.get(url)

		t = ""
		for l in url.split('/')[4:]:
			t = t + l
		output_file = path_out_door +t + '.csv'

		items = driver.find_elements_by_xpath('//div[contains(@class,"Category_itemContainer")]')

		print(len(items))
		try:
			rating = driver.find_element_by_xpath('//em[contains(@class,"StoreDetails_scoresEm")]').text
		except:
			continue
		number_of_ratings = driver.find_element_by_xpath('//span[contains(@class,"StoreDetails_ratings")]').text
		address = driver.find_element_by_xpath('//span[contains(@class,"MenuPage_address")]').text
		data = {'Rating': rating, 'Number Of Ratings': number_of_ratings, 'Address': address}
		with open(output_file, 'a', encoding='utf-8', newline='') as f:
			writer = csv.DictWriter(f, fieldnames=data.keys())
			if not os.fstat(f.fileno()).st_size > 0:
				writer.writeheader()
			writer.writerow(data)
		names = driver.find_elements_by_xpath('//span[contains(@class,"Item_name")]')
		prices = driver.find_elements_by_xpath('//span[contains(@class,"Item_price")]')
		descriptions = driver.find_elements_by_xpath('//div[contains(@class,"Item_description")]')

		tree = html.fromstring(driver.page_source)
		categories = tree.xpath('//div[contains(@class,"Category_root")]')
		for cat in categories:
			type_ = cat.xpath('.//h2[contains(@class,"Category_name")]/text()')[0]
			names = cat.xpath('.//span[contains(@class,"Item_name")]/text()')
			prices = cat.xpath('.//span[contains(@class,"Item_price")]/text()')
			descriptions = cat.xpath('.//div[contains(@class,"Item_description")]/text()')
			for name, price, descr in zip(names, prices, descriptions):
				name = name.replace('®', '').replace('*', '').replace('’', "'")
				print(name)
				data = {'Name': name, 'Price': price, 'Type': type_, 'Description': descr}
				try:
					with open(output_file, 'a', newline='') as f:
						writer = csv.DictWriter(f, fieldnames=data.keys())
						if not os.fstat(f.fileno()).st_size > 0:
							writer.writeheader()
						writer.writerow(data)
				except UnicodeEncodeError:
					with open(output_file, 'a', encoding='utf-8', newline='') as f:
						writer = csv.DictWriter(f, fieldnames=data.keys())
						if not os.fstat(f.fileno()).st_size > 0:
							writer.writeheader()
						writer.writerow(data)



		# for name, price, descr in zip(names, prices, descriptions):
		# 	print(name.text)
		# 	data = {'Name': name.text, 'Price': price.text, 'Description': descr.text}
		# 	try:
		# 		with open('doordash.csv', 'a', newline='') as f:
		# 			writer = csv.DictWriter(f, fieldnames=data.keys())
		# 			if not os.fstat(f.fileno()).st_size > 0:
		# 				writer.writeheader()
		# 			writer.writerow(data)
		# 	except UnicodeEncodeError:
		# 		with open('doordash.csv', 'a', encoding='utf-8', newline='') as f:
		# 			writer = csv.DictWriter(f, fieldnames=data.keys())
		# 			if not os.fstat(f.fileno()).st_size > 0:
		# 				writer.writeheader()
		# 			writer.writerow(data)