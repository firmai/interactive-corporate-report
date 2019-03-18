# -*- coding: utf-8 -*-
import os
import csv



a = csv.DictReader(open('TGIF_locations_pages.csv', 'r', encoding='utf-8'))

urls = []

for i in a:
	if i['Page'] == '1':
		old_url = i['Url'].split('?')[0]
		urls.append(old_url)
	else:
		old_url = i['Url'].split('?')[0]
		urls.append(old_url)
		count = 20
		try:
			for num in range(1, int(i['Page'])):
				new_url = old_url + '?start={}'.format(count)
				urls.append(new_url)
				count += 20
		except ValueError:
			continue

print(len(urls))
for r in urls:
	data = {'Url': r}
	with open('TGIF_urls.csv', 'a', encoding='utf-8', newline='') as f:
		writer = csv.DictWriter(f, fieldnames=data.keys())
		if not os.fstat(f.fileno()).st_size > 0:
			writer.writeheader()
		writer.writerow(data)