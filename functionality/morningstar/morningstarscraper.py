# -*- coding: utf-8 -*-
from jscraper import *
import Queue
import threading
from bs4 import BeautifulSoup
import re
import json
import gc
import time
#for coy, tick_coy in zip(["bjri"],["XNAS:bjri"]):
from pathlib import Path
import os

my_path = os.path.abspath(os.path.dirname('__file__'))

path_out = my_path + "/../../data/morningstar/"


#for coy, tick_coy in zip(["BJRI","RRGB","CAKE"], ["XNAS:bjri","XNAS:rrgb","XNAS:cake"]):
for coy, tick_coy in zip(["APPB","CHIL"], ["XNYS:din","eat"]):

	my_file = Path(coy +'_sample.json')

	statinfo = os.stat("empty_keep.txt")
	while (not my_file.is_file()) or (statinfo.st_size<15000):

		text=open(coy +'_sample.json','w')
		my_file = Path(coy + '_sample.json')
		writelist=[]
		count=0
		#time.sleep(10)


		def get_from_bank(link,stock):
			soup=jscraper.get_soup(url=link['Profile'][0].replace('&t='+stock+':','&t='))
			Classes=jscraper.get_classes(soup=soup,TagName='tr',AttributeName='class',AttributeValue='text3')
			DayAvgVol=jscraper.get_text_element(soup=Classes[0],TagName='td')[0]
			MarketCap=jscraper.get_text_element(soup=Classes[0],TagName='td')[2]
			NetIncome=jscraper.get_text_element(soup=Classes[0],TagName='td')[4]
			Sales=jscraper.get_text_element(soup=Classes[1],TagName='td')[0]
			Sector=jscraper.get_text_element(soup=Classes[1],TagName='td')[2]
			Industry=jscraper.get_text_element(soup=Classes[1],TagName='td')[4]
			StockSale=cleanhtml(jscraper.get_text_element(soup=Classes[2],TagName='td')[0])
			DirInvestment=cleanhtml(jscraper.get_text_element(soup=Classes[2],TagName='td')[2])
			DivInvestment=cleanhtml(jscraper.get_text_element(soup=Classes[2],TagName='td')[4])
			soup2=jscraper.get_soup(url=link['Profile'][1].replace('&t='+stock+':','&t='))
			AllText2=jscraper.get_text_element(soup=soup2,TagName='td')
			NAICS=AllText2[0]
			SIC= ' '.join(cleanhtml(AllText2[2]).split())
			ISIC= ' '.join(cleanhtml(AllText2[4]).split())
			soup3=jscraper.get_soup(url=link['Profile'][2].replace('&t='+stock+':','&t='))
			Executives=' '.join(jscraper.get_text_element(soup=soup3,TagName='a'))
			soup4=jscraper.get_soup(url=link['Profile'][3].replace('&t='+stock+':','&t='))
			AllText4=jscraper.get_text_element(soup=soup4,TagName='td')
			FiscalYearEnds=' '.join(cleanhtml(AllText4[0]).split())
			CIK=' '.join(cleanhtml(AllText4[2]).split())
			YearEstablished=' '.join(cleanhtml(AllText4[4]).split())
			Employees=' '.join(cleanhtml(AllText4[6]).split())
			FullTime=' '.join(cleanhtml(AllText4[8]).split())
			PartTime=' '.join(cleanhtml(AllText4[10]).split())
			Auditor=' '.join(cleanhtml(AllText4[12]).split())
			LegalAdvisor=' '.join(cleanhtml(AllText4[14]).split())
			soup5=jscraper.get_soup(url=link['Stocks'][0].replace('&t='+stock+':','&t='))
			Keystats=cleanhtml(' '.join(jscraper.get_text_element(soup=soup5,TagName='tbody'))).strip().lstrip()
			Keystats=' '.join(Keystats.split())
			soup6=jscraper.get_soup(url=link['Stocks'][1].replace('&t='+stock+':','&t='))
			Financrow=jscraper.get_classes(soup=soup6,TagName='tr',AttributeName='align',AttributeValue='right')
			Cfinancials=table_to_dict(Financrow)
			soup7=jscraper.get_soup(url=link['Competitors'][0].replace('&t='+stock+':','&t='))
			CompRow=jscraper.get_classes(soup=soup7,TagName='tr')
			Competitors=table_to_dict2(CompRow)
			soup8=jscraper.get_soup(url=link['Analyst'][0])
			AnnualEarningEstRow=jscraper.get_classes(soup=soup8,TagName='tr')
			AnnualEarningEst=table_to_dict(AnnualEarningEstRow)
			soup9=jscraper.get_soup(url=link['Analyst'][1].replace('&t='+stock+':','&t='))
			AnalystRating=cleanhtml(' '.join(jscraper.get_text_element(soup=soup9,TagName='tbody'))).strip().lstrip().rstrip().strip('\xc2\xa0')
			AnalystRating=' '.join(AnalystRating.split())
			soup10=jscraper.get_soup(url=link['Valuation'][0].replace('&t='+stock+':','&t='))
			ForwardCalculation=cleanhtml(' '.join(jscraper.get_text_element(soup=soup10,TagName='tbody'))).strip().lstrip().rstrip().strip('\xc2\xa0')
			ForwardCalculation=' '.join(ForwardCalculation.split())
			soup11=jscraper.get_soup(url=link['Valuation'][1].replace('&t='+stock+':','&t='))
			CurrentCalculation=cleanhtml(' '.join(jscraper.get_text_element(soup=soup11,TagName='tbody'))).strip().lstrip().rstrip().strip('\xc2\xa0')
			CurrentCalculation=' '.join(CurrentCalculation.split())
			soup12=jscraper.get_soup(url=link['Insiders'][0].replace('&t='+stock+':','&t='))
			BoardDirectors=cleanhtml(jscraper.get_text(soup=soup12)).strip().lstrip().rstrip().strip('\xc2\xa0')
			# BoardDirectors=' '.join(BoardDirectors.split())
			soup13=jscraper.get_soup(url=link['Committees'][0].replace('&t='+stock+':','&t='))
			Committees=cleanhtml(jscraper.get_text(soup=soup13)).strip().lstrip().rstrip().strip('\xc2\xa0')

			# soup14=jscraper.get_soup(url=link['EqOwner'][0].replace('&t=XNAS:','&t='+stock+':'))
			# EquitityOwnership=jscraper.get_classes(soup=soup14,TagName='table',AttributeName='id',AttributeValue='equitycacheTable')
			# EquitityOwnership=table_to_dict(EquitityOwnership)
			# print EquitityOwnership
			jsondata={'DayAvgVol':DayAvgVol,'MarketCap':MarketCap,'NetIncome':NetIncome,'Sales':Sales,'Sector':Sector,'Industry':Industry,'StockSale':StockSale,'DirInvestment':DirInvestment,'NAICS':NAICS,'SIC':SIC,'ISIC':ISIC,'Executives':Executives,
			'FiscalYearEnds':FiscalYearEnds,'CIK':CIK,'YearEstablished':YearEstablished,'Employees':Employees,'FullTime':FullTime,'PartTime':PartTime,'Auditor':Auditor,'LegalAdvisor':LegalAdvisor,'Keystats':Keystats,
			'Cfinancials':Cfinancials,'Competitors':Competitors,'AnnualEarningEst':AnnualEarningEst,'AnalystRating':AnalystRating,'ForwardCalculation':ForwardCalculation,'CurrentCalculation':CurrentCalculation,'BoardDirectors':BoardDirectors,'Committees':Committees}
			return jsondata

		def table_to_dict(rows):
			DictList=[]
			for row in rows:
				try:
					DictField={}
					columns=jscraper.get_text_element(soup=row,TagName='td')
					if columns[0]:
						DictField[' '.join(columns[0].split())]=columns[1:]
						DictList.append(DictField)
				except:
					pass
			return DictList


		def table_to_dict2(rows):
			DictList=[]
			for row in rows:
				try:
					DictField={}
					columns=jscraper.get_text_element(soup=row,TagName='td')
					Header=jscraper.get_text_element(soup=row,TagName='th')
					mykey=cleanhtml(Header[0]).replace('\n','')
					if len(columns)>1:
						DictField[' '.join(mykey.split())]='|'.join(columns[1:]).strip().strip('\n').lstrip().rstrip().replace('\n','').replace(' ','').split('|')
						DictList.append(DictField)
				except Exception as E:
					print E
					pass
			return DictList


		def get_links(Name,LinkList):
			global LinksDict
			LinksDict[Name]=LinkList


		def cleanhtml(raw_html):
			cleanr = re.compile('<.*?>')
			cleantext = re.sub(cleanr, '', raw_html)
			return cleantext

		def get_info(queue,CompanyName):
			global text,writelist
			queue_full = True
			while queue_full:
				try:
					link= queue.get(False)
					try:
						jsondata={}
						jsondata[CompanyName]=get_from_bank(link,'XNAS')
					except Exception as E:
						print E
						try:
							jsondata={}
							jsondata[CompanyName]=get_from_bank(link,'XNYS')
						except Exception as E:
							print E
							pass
					try:
						writelist.append(jsondata)
					except:
						pass
					q.task_done()
				except Queue.Empty:
					queue_full = False


		def get_companies():
			company =[tick_coy]
			return company



		Companies=get_companies()
		for CompanyName in Companies:
			AllLinks=[]
			LinksDict={}
			LinkList=[]
			LinkList.append('http://financials.morningstar.com/cmpind/company-profile/component.action?component=BasicData&t={COMPANYNAME}&region=usa&culture=en-US&cur=&_=1515378517614'.replace('{COMPANYNAME}',CompanyName))
			LinkList.append('http://financials.morningstar.com/cmpind/company-profile/component.action?component=IndustryClassification&t={COMPANYNAME}&region=usa&culture=en-US&cur=&_=1515378517615'.replace('{COMPANYNAME}',CompanyName))
			LinkList.append('http://financials.morningstar.com/cmpind/company-profile/component.action?component=insidersList&t={COMPANYNAME}&region=usa&culture=en-US&cur=&_=1515460795632'.replace('{COMPANYNAME}',CompanyName))
			LinkList.append('http://financials.morningstar.com/cmpind/company-profile/component.action?component=OperationDetails&t={COMPANYNAME}&region=usa&culture=en-US&cur=&_=1515460795329'.replace('{COMPANYNAME}',CompanyName))

			get_links('Profile',LinkList)

			LinkList=[]
			LinkList.append('http://investors.morningstar.com/ownership/shareholders-overview.html?t={COMPANYNAME}&region=usa&culture=en-US'.replace('{COMPANYNAME}',CompanyName))
			get_links('EqOwner',LinkList)

			LinkList=[]
			LinkList.append('http://quotes.morningstar.com/stockq/c-keystats?&t={COMPANYNAME}&region=usa&culture=en-US&version=RET&cur=&test=QuoteiFrame&e=eyJlbmMiOiJBMTI4R0NNIiwiYWxnIjoiUlNBLU9BRVAifQ.mZ0BqTbgOqIwt1TUz1mKPDSjnp1D1FTk-Eb_ZvK50D6m-21Ht_4o6gGG-rU6awWPFqxaXNMuNr81o4hRFuRIwAsvf3dE6ZEq4-w2kOlz2roTM5agvSFgJqy1XWUGowcxjEw4BiWcRLXFSXQuJhvjLtiWzeS6SyTiE6LC9vrViNs.MLt5SKViMzMw5ryZ.m41PyUJJfxMO-o7c07Gpmkwma-LZbqN-9pudLwe-dxtE7HYSMnQx-KRADOJ9-ixiJV-Aawq0gFts3yt0p66mHTFmfQMhPqldYx_iL2DjK9SUIpCPAKRV9m58uSF4QeXM5ML2xQvrsW-0kUS_U2Z9R1m6dRONSBTCnIEtJ9oyaVDVTXCcofiFi9kYLhg_GMIHWmk2UxODtE8yTDYiaH2PAxEoRZf3Tn1Ud8Ekqnw.1Fr0hfYfD7_LbIIo9kPXQQ'.replace('{COMPANYNAME}',CompanyName))
			LinkList.append('http://quotes.morningstar.com/stockq/c-financials?&t={COMPANYNAME}&region=usa&culture=en-US&version=RET&cur=&test=QuoteiFrame&e=eyJlbmMiOiJBMTI4R0NNIiwiYWxnIjoiUlNBLU9BRVAifQ.mZ0BqTbgOqIwt1TUz1mKPDSjnp1D1FTk-Eb_ZvK50D6m-21Ht_4o6gGG-rU6awWPFqxaXNMuNr81o4hRFuRIwAsvf3dE6ZEq4-w2kOlz2roTM5agvSFgJqy1XWUGowcxjEw4BiWcRLXFSXQuJhvjLtiWzeS6SyTiE6LC9vrViNs.MLt5SKViMzMw5ryZ.m41PyUJJfxMO-o7c07Gpmkwma-LZbqN-9pudLwe-dxtE7HYSMnQx-KRADOJ9-ixiJV-Aawq0gFts3yt0p66mHTFmfQMhPqldYx_iL2DjK9SUIpCPAKRV9m58uSF4QeXM5ML2xQvrsW-0kUS_U2Z9R1m6dRONSBTCnIEtJ9oyaVDVTXCcofiFi9kYLhg_GMIHWmk2UxODtE8yTDYiaH2PAxEoRZf3Tn1Ud8Ekqnw.1Fr0hfYfD7_LbIIo9kPXQQ'.replace('{COMPANYNAME}',CompanyName))
			get_links('Stocks',LinkList)

			LinkList=[]
			LinkList.append('http://financials.morningstar.com/cmpind/competitors/industry-peer-data.action?type=com&t={COMPANYNAME}&region=usa&culture=en-US&cur=&_=1515645286506&pageIndex=1&sortBy=MARKET-CAP&order=DESC'.replace('{COMPANYNAME}',CompanyName))
			get_links('Competitors',LinkList)


			LinkList=[]
			LinkList.append('http://financials.morningstar.com/valuate/annual-estimate-list.action?&t={COMPANYNAME}&region=usa&culture=en-US&cur=&r=1515646052335.632&_=1515646052336'.replace('{COMPANYNAME}',CompanyName))
			LinkList.append('http://financials.morningstar.com/valuate/analyst-opinion-list.action?&t={COMPANYNAME}&region=usa&culture=en-US&cur=&r=1515646052338.1562&_=1515646052338'.replace('{COMPANYNAME}',CompanyName))
			get_links('Analyst',LinkList)



			LinkList=[]
			LinkList.append('http://financials.morningstar.com/valuate/forward-valuation-list.action?&t={COMPANYNAME}&region=usa&culture=en-US&cur=&adsFlag=true&_=1515726839712'.replace('{COMPANYNAME}',CompanyName))
			LinkList.append('http://financials.morningstar.com/valuate/current-valuation-list.action?&t={COMPANYNAME}&region=usa&culture=en-US&cur=&adsFlag=true&_=1515726839708'.replace('{COMPANYNAME}',CompanyName))
			get_links('Valuation',LinkList)



			LinkList=[]
			LinkList.append('http://insiders.morningstar.com/insiders/trading/current-insiders-list.action?&t={COMPANYNAME}&region=usa&culture=en-US&cur=&type=Director&_=1515729966952'.replace('{COMPANYNAME}',CompanyName))
			get_links('Insiders',LinkList)

			LinkList=[]
			LinkList.append('http://insiders.morningstar.com/insiders/trading/insider-committees-data.action?&t={COMPANYNAME}&region=usa&culture=en-US&cur=&_=1515730672811'.replace('{COMPANYNAME}',CompanyName))
			get_links('Committees',LinkList)




			AllLinks.append(LinksDict)





			q = Queue.Queue()
			for link in AllLinks:
				q.put(link)
			thread_count = 12
			for i in range(thread_count):
				t = threading.Thread(target=get_info, args = (q,CompanyName,))
				t.start()

			q.join()

			print 'DONE'
		text=open(coy +'_sample.json','w')
		Towrite=json.dump(writelist, text, indent=4,ensure_ascii=True,encoding='utf8',sort_keys=True)

		text.close()

		print 'DONE'
		statinfo = os.stat(coy + "_sample.json")
		#gc.collect()