# -*- coding: utf-8 -*-
from bs4 import *
import sqlite3
import re
import string
import json
import Queue
import threading
from xml.dom.minidom import parseString
from bs4 import BeautifulSoup
import time
import requests
import sys
reload(sys)
sys.setdefaultencoding('UTF8')
from requests.packages.urllib3.exceptions import InsecureRequestWarning
requests.packages.urllib3.disable_warnings(InsecureRequestWarning)



class jscraper(object):


	@staticmethod
	def get_soup(url=''):
		headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.102 Safari/537.36'}
		html=requests.get(url, verify=False,headers=headers).text
		soup=BeautifulSoup(html, "html.parser")
		return soup


	@staticmethod
	def get_text_element(soup='',TagName='',AttributeName='',AttributeValue=''):
		text_el=[]
		if AttributeName and AttributeValue !='':
			tag=soup(TagName,{AttributeName:AttributeValue})
			for t in tag:
				el=t.renderContents()
				text_el.append(el)	
		else:
			tag=soup(TagName)
			for t in tag:
				el=t.renderContents()
				text_el.append(el)
		for t in text_el:			
			t=soup.get_text().encode('utf-8-sig').strip()
		return text_el

	@staticmethod
	def get_classes(soup='',TagName='',AttributeName='',AttributeValue=''):
		classes=soup(TagName,{AttributeName:AttributeValue})
		return classes

	@staticmethod
	def get_links(soup='',TagName='a',AttributeName='',AttributeValue='',Prefix='',UniqueCharCheck=''):
		links=list()
		links2=list()
		if AttributeName and AttributeValue !='':
			tag=soup(TagName,{AttributeName:AttributeValue})
			for t in tag:
				links.append(str(t.get('href')))
		else:
			tag=soup(TagName)
			for t in tag:
				links.append(str(t.get('href')))
		if UniqueCharCheck!='':
			for link in links:
				if UniqueCharCheck in str(link):
					links2.append(Prefix+link)
		else:
			for link in links:
				links2.append(Prefix+link)
		return links2

	@staticmethod
	def get_specific(SearchTest='',StartString='',EndString=''):
		if StartString in SearchTest:
			start=SearchTest.find(StartString)
			my_search=SearchTest[start+len(StartString):]
			end=my_search.find(EndString)
			my_search=my_search[:end]
		else:
			return ' '
		return my_search

	@staticmethod
	def get_text(soup=''):
		text_array=[]
		for script in soup(["script", "style"]):
		    script.extract()
		text = soup.get_text()
		lines = (line.strip() for line in text.splitlines())
		chunks = (phrase.strip() for line in lines for phrase in line.split("  "))
		text = '\n'.join(chunk for chunk in chunks if chunk)
		text= text.encode('utf-8','ignore')
		# for t in text.split('\n'):
		# 	text_array.append(t.strip())
		return text


	@staticmethod
	def write_database(db_file,infolist):
		try:
			conn = sqlite3.connect(db_file)
			c = conn.cursor()
			try:
				c.execute('''CREATE TABLE jobs (COMPANY text,URL text, DESCRIPTION text,APPDEADLINE text, DATEGATHERED text)''')
			except:
				pass
			c.executemany('INSERT INTO jobs VALUES (?,?,?,?,?)',[infolist])
			conn.commit()
			conn.close()
		except Exception as e:
			print e

	@staticmethod
	def unique_check(db_file,Company,Url,Description,Deadline,DateGathered):
		try:
			conn = sqlite3.connect(db_file)
			c = conn.cursor()
			try:
				c.execute("SELECT * FROM jobs WHERE DESCRIPTION=?", (Description,))
				data=c.fetchall()
				if len(data)==0:
					return True
				else:
					return False
			except Exception as E:
				pass
		except Exception as E:
			pass
		return True