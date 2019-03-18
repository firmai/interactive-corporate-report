import csv
import requests
from bs4 import BeautifulSoup 
from urllib.parse import urljoin
import os
import errno

csv_files = ['APPB_locations.csv', 'BJRI_locations.csv', 'CAKE_locations.csv',
				'CHIL_locations.csv', 'CPKI_locations.csv', 'RRGB_locations.csv',
				'TGIF_locations.csv']

codes = [a.split('_')[0] for a in csv_files]

os.makedirs(os.path.dirname("../files_yelp/"), exist_ok=True)

url_biz = 'https://nz.yelp.com/biz/bjs-restaurant-and-brewhouse-huntington-beach'

for csv_file, namer in zip(csv_files, codes):
    a = csv.DictReader(open(csv_file, 'r', encoding='utf-8'))
    for row in a:
        url_biz = row['Link']
        output_file = url_biz.split('/')[-1].split('?start=')[0] + '.csv'


        def custom_zip(*iterables):
            """
            A re-implementation of the default zip function
            Author: toby
            """
            count = 0
            max_ = max(len(i) for i in iterables)
            iterators = [iter(it) for it in iterables]

            while count < max_:
                result = []
                for it in iterators:
                    elem = next(it, ['', ''])
                    result.extend(elem)
                count += 1
                yield tuple(result)


        def _extract_hours_opened(url):
            """
            Extract opening hours of a business on YELP !
            """
            print(f">>Sending a request to {url}...")
            response = requests.get(url, headers={'user-agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) \
                AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.108 Safari/537.36'})

            soup = BeautifulSoup(response.content, 'html.parser')

            # sidebar
            sidebar = soup.find('div', class_='sidebar')

            # task 1
            # opening hours
            biz_hours = soup.select('table.hours-table tr')
            day_time = [ [hr.find('th').text, hr.find('td').text.strip()] for hr in biz_hours ]

            # task 2
            # all the business info; more-info
            more_info_dl = soup.select('div.ywidget ul.ylist dl')
            info_cond = [ [m.find('dt').text.strip(), m.find('dd').text.strip()] for m in more_info_dl ]

            # task 3
            # people might also consider
            ads_business = sidebar.select('div.you-might-also-consider a.biz-name')
            ads_name_url = [ [a.text.strip(), urljoin(response.url, a.get('href'))] for a in ads_business]

            # task 4
            # people also viewed
            related_business = sidebar.select('div.js-related-businesses a.biz-name')
            related_name_url = [ [a.text.strip(), urljoin(response.url, a.get('href'))] for a in related_business]

            # couple all results and write to csv
            title = soup.find('h1', class_='biz-page-title').text.strip()
            csv_file_name = output_file

            my_path = os.path.abspath(os.path.dirname(__file__))
            path_out = os.path.join(my_path, "../../data/yelp_info/"+str(namer)+'/' + csv_file_name)

            if not os.path.exists(os.path.dirname(path_out)):
                try:
                    os.makedirs(os.path.dirname(path_out))
                except OSError as exc:  # Guard against race condition
                    if exc.errno != errno.EEXIST:
                        raise

            headers = ['Day', 'Hours Opened', 'Business Info', 'Detail', 'Also-Considered', 'Link', 'Also-Viewed', 'Link']
            results = custom_zip(day_time, info_cond, ads_name_url, related_name_url)
            with open(path_out, 'w', newline='') as f:
                csvfile = csv.writer(f)
                csvfile.writerow(headers)
                csvfile.writerows(results)

            # done !!
            print(f'\n\ncsv file saved as {csv_file_name}')


        if __name__ == '__main__':
            import sys
            if len(url_biz) < 2:
                print('Script accept 1 additional argument <business-url>')
                sys.exit(0)

            url = url_biz
            # call the function
            _extract_hours_opened(url)
