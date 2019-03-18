import os
import time
from selenium import webdriver
from selenium.common.exceptions import TimeoutException
from selenium.common.exceptions import ElementNotVisibleException
from selenium.common.exceptions import NoSuchElementException
import urllib
import urllib.request
from bs4 import BeautifulSoup
import csv
from itertools import zip_longest
import codecs
import random
import sys

def make_soup(url):
    thepage = urllib.request.urlopen(url)
    soupdata = BeautifulSoup(thepage, "lxml")
    return soupdata


file = open("urls_scraped.txt", "a+")
f = csv.writer(codecs.open("Instagram.csv", "ab+", "utf-8-sig"), lineterminator="\n")
f.writerow(["Name", "Posts", "Followers", "Following", "Category", "Website", "Instagram Url"])
try:
    with open("urls.txt", "r") as inf:
        urls = (line.strip() for line in inf)
        for url in urls:
            print(url)
            url1 = url + "\n"
            file1 = open("urls_scraped.txt", "r")
            double = file1.read()
            file1.close()
            if url not in double:
                def open_browser():
                    file.write(url1)
                    try:
                        fa = open('proxy_file.txt', 'r')
                        proxy_ip = fa.read()
                        fa.close()
                        headers = {'Accept':'*/*',
                            'Accept-Encoding':'gzip, deflate, sdch',
                            'Accept-Language':'en-US,en;q=0.8',
                            'Cache-Control':'max-age=0',
                            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36'}
                        for key, value in enumerate(headers):
                            webdriver.DesiredCapabilities.PHANTOMJS['phantomjs.page.customHeaders.{}'.format(key)] = value
                        if len(proxy_ip) <= 1:
                            print("No Proxy will be used...")
                            driver = webdriver.PhantomJS(executable_path='/Users/dereksnow/anaconda/envs/py36/bin/phantomjs')
                            driver.set_window_size(1024, 768)
                        else:
                            print('Using proxy :' + proxy_ip)
                            service_args = [
                                '--proxy=' + proxy_ip + ':9999',
                                '--proxy-type=socks5'
                            ]
                            driver = webdriver.PhantomJS(executable_path='/Users/dereksnow/anaconda/envs/py36/bin/phantomjs', service_args=service_args)
                            driver.set_window_size(1024, 768)
                    except:
                        os.system("python get_proxy.py")
                        print("REQUEST ERROR...No Proxy will be used...")
                        driver = webdriver.PhantomJS(executable_path='/Users/dereksnow/anaconda/envs/py36/bin/phantomjs')
                        driver.set_window_size(1024, 768)
                    driver.implicitly_wait(5)
                    driver.set_page_load_timeout(300)
                    return driver

                name = []
                posts = []
                following = []
                followers = []
                descr = []
                website = []
                instagram = []
                instagram.append(url)
                try:
                    driver = open_browser()
                    driver.get(url)
                    plt = random.randint(0, 3)
                    time.sleep(plt)
                    try:
                        phon = driver.find_element_by_xpath('//*[@id="react-root"]/section/main/article/header/section/div[2]/h1')
                        tex = phon.text
                        name.append(tex)
                        print(name)
                    except ElementNotVisibleException:
                        phon = driver.find_element_by_xpath('//*[@id="react-root"]/section/main/article/header/section/div[2]/h1')
                        tex = phon.text
                        name.append(tex)
                        print(name)
                except (TimeoutException, NoSuchElementException):
                    print("Name not found")
                    name.append("No name")
                try:
                    try:
                        emai = driver.find_element_by_xpath(
                            '//*[@id="react-root"]/section/main/article/header/section/div[2]/span/span')
                        te = emai.text
                        descr.append(te)
                        print(descr)
                    except ElementNotVisibleException:
                        emai = driver.find_element_by_xpath(
                            '//*[@id="react-root"]/section/main/article/header/section/div[2]/span/span')
                        te = emai.text
                        descr.append(te)
                        print(descr)
                except (TimeoutException, NoSuchElementException):
                    print("Category not found")
                    descr.append("No category")
                try:
                    try:
                        post = driver.find_element_by_xpath(
                            '//*[@id="react-root"]/section/main/article/header/section/ul/li[1]/span/span')
                        te = post.text
                        posts.append(te)
                        print(te)
                    except ElementNotVisibleException:
                        post = driver.find_element_by_xpath(
                            '//*[@id="react-root"]/section/main/article/header/section/ul/li[1]/span/span')
                        te = post.text
                        posts.append(te)
                        print(te)
                except (TimeoutException, NoSuchElementException):
                    print("Posts not found")
                    descr.append("No posts")
                try:
                    try:
                        follower = driver.find_element_by_xpath(
                            '//*[@id="react-root"]/section/main/article/header/section/ul/li[2]/span/span')
                        te = follower.text
                        followers.append(te)
                        print(te)
                    except ElementNotVisibleException:
                        follower = driver.find_element_by_xpath(
                            '//*[@id="react-root"]/section/main/article/header/section/ul/li[2]/span/span')
                        te = follower.text
                        followers.append(te)
                        print(te)
                except (TimeoutException, NoSuchElementException):
                    print("Followers not found")
                    descr.append("No followers")
                try:
                    try:
                        follow = driver.find_element_by_xpath(
                            '//*[@id="react-root"]/section/main/article/header/section/ul/li[3]/span/span')
                        te = follow.text
                        following.append(te)
                        print(te)
                    except ElementNotVisibleException:
                        follow = driver.find_element_by_xpath(
                            '//*[@id="react-root"]/section/main/article/header/section/ul/li[3]/span/span')
                        te = follow.text
                        following.append(te)
                        print(te)
                except (TimeoutException, NoSuchElementException):
                    print("Following not found")
                    descr.append("No following")
                try:

                    try:
                        web = driver.find_element_by_xpath('//*[@id="react-root"]/section/main/article/header/section/div[2]/a')
                        te = web.text
                        website.append(te)
                        print(website)
                    except ElementNotVisibleException:
                        web = driver.find_element_by_xpath('//*[@id="react-root"]/section/main/article/header/section/div[2]/a')
                        te = web.text
                        website.append(te)
                        print(website)
                except (TimeoutException, NoSuchElementException):
                    print(website)
                    website.append("No website")
                for c, z, x, u, i, j, k in zip_longest(name, posts, followers, following, descr, website, instagram):
                    f.writerow((c, z, x, u, i, j, k))
                # os.system("python get_proxy.py")
                driver.quit()

            else:
                pass
except OSError:
    file.close()
    os.execl(sys.executable, sys.executable, *sys.argv)

