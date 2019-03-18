import sys
import urllib.request
import json
import datetime
import csv
import time
encode_filter = lambda x: ord(x)<128

start_date = datetime.date(2004,1,1)
end_date = datetime.date.today()
diff_days = ((end_date + datetime.timedelta(1)) - (start_date - datetime.timedelta(1))).days


import pandas as pd
import os

input_fields = pd.read_csv("../../input_fields.csv")
names = input_fields["yelp_name"]
codes = input_fields["code_or_ticker"]

names =["BJsRestaurants","applebees","thecheesecakefactory","Chilis","californiapizzakitchen","RedRobin","TGIFridays"]
"""
codes =[
"TGIF"]
"""

my_path = os.path.abspath(os.path.dirname('__file__'))

path_out = my_path + "/../../data/facebook/"




def FacebookPageData(page_id, access_token):
    # construct the URL string
    base = "https://graph.facebook.com/v2.4"
    node = "/" + page_id
    parameters = "/?access_token=%s" % access_token
    url = base + node + parameters

    # retrieve data
    req = urllib.request.Request(url)
    response = urllib.request.urlopen(req)
    data = json.loads(response.read())
    print(json.dumps(data, indent=4, sort_keys=True))


# testFacebookPageData(page_id, access_token)

def request_until_succeed(url):
    req = urllib.request.Request(url)
    success = False
    while success is False:
        try:
            response = urllib.request.urlopen(req)
            if response.getcode() == 200:
                success = True
        except Exception as e:
            print(e)
            time.sleep(5)

            print("Error for URL %s: %s" % (url, datetime.datetime.now()))

    return response.read().decode('utf-8')


def FacebookPageFeedData(page_id, access_token):
    # construct the URL string
    base = "https://graph.facebook.com/v2.4"
    node = "/" + page_id + "/feed"  # changed
    parameters = "/?access_token=%s" % access_token
    url = base + node + parameters

    # retrieve data
    data = json.loads(request_until_succeed(url))

    print(json.dumps(data, indent=4, sort_keys=True))


# testFacebookPageFeedData(page_id, access_token)

def getFacebookPageFeedData(page_id, access_token, num_statuses):
    # construct the URL string
    base = "https://graph.facebook.com"
    node = "/" + page_id + "/feed"
    parameters = "/?since=%s&until=%s&fields=message,link,created_time,type,name,id,reactions.limit(1).summary(true),comments.limit(1).summary(true),shares&limit=%s&access_token=%s" % (
    start_date, end_date, num_statuses, access_token)  # changed
    url = base + node + parameters

    # retrieve data
    data = json.loads(request_until_succeed(url))

    return data


# test_status = getFacebookPageFeedData(page_id, access_token, 1)["data"][0]
# print json.dumps(test_status, indent=4, sort_keys=True)

def processFacebookPageFeedStatus(status):
    # The status is now a Python dictionary, so for top-level items,
    # we can simply call the key.

    # Additionally, some items may not always exist,
    # so must check for existence first

    status_id = status['id']
    status_message = '' if 'message' not in status.keys() else ''.join(list(filter(encode_filter, status['message'])))
    link_name = '' if 'name' not in status.keys() else ''.join(list(filter(encode_filter, status['name'])))
    status_type = status['type']
    status_link = '' if 'link' not in status.keys() else status['link']

    # Time needs special care since a) it's in UTC and
    # b) it's not easy to use in statistical programs.

    status_published = datetime.datetime.strptime(status['created_time'], '%Y-%m-%dT%H:%M:%S+0000')
    status_published = status_published + datetime.timedelta(hours=-5)  # EST
    status_published = status_published.strftime('%Y-%m-%d %H:%M:%S')  # best time format for spreadsheet programs

    # Nested items require chaining dictionary keys.

    num_reactions = 0 if 'reactions' not in status.keys() else status['reactions']['summary']['total_count']
    num_comments = 0 if 'comments' not in status.keys() else status['comments']['summary']['total_count']
    num_shares = 0 if 'shares' not in status.keys() else status['shares']['count']

    # return a tuple of all processed data
    return (status_id, status_message, link_name, status_type, status_link,
            status_published, num_reactions, num_comments, num_shares)


# processed_test_status = processFacebookPageFeedStatus(test_status)
# print processed_test_status

def scrapeFacebookPageFeedStatus(page_id, access_token, file):
    w = csv.writer(file)
    w.writerow(["status_id", "status_message", "link_name",
                "status_type", "status_link",
                "status_published", "num_reactions", "num_comments", "num_shares"])

    has_next_page = True
    num_processed = 0  # keep a count on how many we've processed
    scrape_starttime = datetime.datetime.now()

    print("Scraping %s Facebook Page: %s\n" % (page_id, scrape_starttime))

    statuses = getFacebookPageFeedData(page_id, access_token, 100)

    while has_next_page:
        for status in statuses['data']:
            w.writerow(processFacebookPageFeedStatus(status))

            # output progress occasionally to make sure code is not stalling
            num_processed += 1
            if num_processed % 1000 == 0:
                print("%s Statuses Processed: %s" % (num_processed, datetime.datetime.now()))

        # if there is no next page, we're done.
        if 'paging' in statuses.keys() and 'next' in statuses['paging']:
            statuses = json.loads(request_until_succeed(statuses['paging']['next']))
        else:
            has_next_page = False

    print("\nDone!\n%s Statuses Processed in %s" % (num_processed, datetime.datetime.now() - scrape_starttime))


for page_id, c in zip(names,codes):

    fd = open(path_out + c +'_facebook.csv','w')
    page_id = page_id.split('/')[-1]
    app_id = "xxxxxx"
    app_secret = "xxxxxx"  # DO NOT SHARE WITH ANYONE!

    access_token = app_id + "|" + app_secret
    scrapeFacebookPageFeedStatus(page_id, access_token, fd)
    fd.close()
