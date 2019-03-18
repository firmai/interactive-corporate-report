import urllib, bs4, re, sys
import requests
import json
import unicodedata
from difflib import SequenceMatcher
import time
import requests
from bs4 import BeautifulSoup
from itertools import groupby

client = requests.Session()

HOMEPAGE_URL = 'https://www.linkedin.com'
LOGIN_URL = 'https://www.linkedin.com/uas/login-submit'

html = client.get(HOMEPAGE_URL).content
soup = BeautifulSoup(html)
csrf = soup.find(id="loginCsrfParam-login")['value']

login_information = {
    'session_key': sys.argv[1],
    'session_password': sys.argv[2],
    'loginCsrfParam': csrf,
}

client.post(LOGIN_URL, data=login_information)
time.sleep(5)
cookie = client.cookies.get_dict()
bcookie = cookie.get('bcookie')
bscookie = cookie.get('bscookie')
lidc = cookie.get('lidc')
visit = cookie.get('visit')
leo_auth = cookie.get('leo_auth_token')
lang = cookie.get('lang')
JSESSIONID = cookie.get('JSESSIONID')
li_at = cookie.get('li_at')
liap = cookie.get('liap')
sl = cookie.get('sl')
JSESSIONID = JSESSIONID[1:-1]

headers = {
    'accept-encoding': 'gzip, deflate, br',
    'x-li-lang': 'en_US',
    'accept-language': 'en-IN,en-GB;q=0.9,en-US;q=0.8,en;q=0.7',
    'x-requested-with': 'XMLHttpRequest',
    'cookie': 'bcookie=' + bcookie +'; bscookie='+bscookie+'; _ga=GA1.2.2031948949.1505287936; join_wall=v=3&AQHD97456159aAAAAWDPGQ3M3Aq3_rLnrrKVlLylSXdBQfIey_uaWr_eJdf_Iv3pXIXRasL3MnYYxBNzU4JT110ze90bP7cnpwR2RT-gyw3TzY4m8lDwwg8zN7b_1IA8E_4opY5OI_WHYkujFFxolT9dpJ7FqB53bo9v49gNLxjVqdLyfzxwr1_uPLQrjIPZLt2-l8DYqxIjiTltSKo5dBlsiYDR5g; visit='+visit+'; JSESSIONID="'+JSESSIONID+'"; lang='+lang+'; leo_auth_token='+leo_auth+'; sl=' + sl + '; li_at=' + li_at +'; liap='+ liap+ '; _gat=1; _lipt=CwEAAAFg0JRRaEURBUySp_H7rUHhlKUvxHByf26SW8DjXFfJLqDfaJ2Ur45U2McgAnKXEkrZ3p7HcB7nIM48TDnstalQUSxh8KVxod9RCLP2cm1uHtJDyEPpa9nFqNOMnq44ccWIRfdGpMqOp9L8cvZf-PYMQLpUpMGqtDlVx1sm; lidc='+lidc,
    'x-restli-protocol-version': '2.0.0',
    'user-agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.132 Safari/537.36',
    'x-li-page-instance': 'urn:li:page:d_flagship3_company;Q+QlHYpyQm2iHdKt1Z2TRQ==',
    'accept': 'application/vnd.linkedin.normalized+json',
    'csrf-token': JSESSIONID,
    'x-li-track': '{"clientVersion":"1.1.*","osName":"web","timezoneOffset":5.5,"deviceFormFactor":"DESKTOP","mpName":"voyager-web"}',
    'authority': 'www.linkedin.com',
    'referer': 'https://www.linkedin.com/feed/',
}
print ('login done')

if len(sys.argv)==4:
	rest_list = sys.argv[3].split(',')
else:
	print ('fetching restaurants list')
	pages = bs4.BeautifulSoup(urllib.request.urlopen('https://www.thebalance.com/publicly-traded-us-restaurant-chains-2892798').read())
	strong = pages('strong')
	rest_list = [unicodedata.normalize('NFKD',res.contents[0]).encode('ascii','ignore').strip().decode('utf-8') for res in strong if res.contents and type(res.contents[0]) == bs4.element.NavigableString]
	print (rest_list)

rest_id_list = {}
for restaurant in rest_list:
	params = (
		('keywords', restaurant),
		('origin', 'GLOBAL_SEARCH_HEADER'),
		('q', 'blended'),
	)

	response = requests.get('https://www.linkedin.com/voyager/api/typeahead/hitsV2', headers=headers, params=params)
	com_id = json.loads(response.text)
	com_list = json.loads(response.text)
	if com_list.get('included',None):
		com_list = com_list['included']
	else:
		continue

	matching_ratio = []
	for com in com_list:
		if com.get('name',None):
			matching_ratio.append(SequenceMatcher(None, restaurant.lower(), com['name'].lower()).ratio())
			print (com['name'] + ' is matched with' + str(matching_ratio[-1]))

	com_list = [com for com in com_list if com.get('name',None)]
	com = com_list[matching_ratio.index(max(matching_ratio))]
	#print com
	urn = com.get('entityUrn',None)
	if not urn:
		urn = com.get('objectUrn',None)
	if urn:
		rest_id_list[restaurant] = int(re.search(r'\d+', urn).group())

rest_rem_list = [rest for rest in rest_list if rest not in rest_id_list.keys()]
for restaurant in rest_rem_list:
	url = 'https://www.linkedin.com/voyager/api/search/cluster?count=10&guides=List(v-%3ECOMPANIES)&keywords=' + restaurant + '&origin=SWITCH_SEARCH_VERTICAL&q=guided&start=0'
	response = requests.get(url, headers=headers)
	 
	com_list = json.loads(response.text)
	if com_list.get('included',None):
		com_list = com_list['included']
	else:
		continue
	 
	matching_ratio = []
	 
	for com in com_list:
		if 'name' in com.keys():
			matching_ratio.append(SequenceMatcher(None, restaurant.lower(), com['name'].lower()).ratio())
	
	com_list = [com for com in com_list if 'name' in com.keys()]
	com = com_list[matching_ratio.index(max(matching_ratio))]
	#print com
	urn = com.get('entityUrn',None)
	if not urn:
		urn = com.get('objectUrn',None)
	if urn:
		rest_id_list[restaurant] = int(re.search(r'\d+', urn).group())

print (rest_id_list)
sim_com_dict = {}
for key, value in rest_id_list.items():
	params = (
		('decoration', '(name,industries,logo,staffCountRange,url,universalName,entityUrn~(~relevanceReason(company,details(com.linkedin.voyager.jobs.shared.InNetworkRelevanceReasonDetails(inNetworkPeopleSearchUrl,totalNumberOfConnections,topConnections*~(profilePicture,firstName,lastName,entityUrn)),com.linkedin.voyager.jobs.shared.CompanyRecruitRelevanceReasonDetails(currentCompany~(entityUrn,logo,name,industries,followingInfo,url,paidCompany,universalName),totalNumberOfPastCoworkers,sharedPastCompanyPeopleSearchUrl),com.linkedin.voyager.jobs.shared.SchoolRecruitRelevanceReasonDetails(mostRecentSchool~(entityUrn,logo,name,description,coverPhoto),totalNumberOfAlumni,sharedSchoolPeopleSearchUrl))),entityUrn))'),
		('companyUniversalName', value),
		('count', '6'),
		('q', 'similarCompanies'),
		('start', '0'),
	)

	response = requests.get('https://www.linkedin.com/voyager/api/organization/companies', headers=headers, params=params)
	sim_com_json = json.loads(response.text)
	sim_com = []

	for com in sim_com_json['included']:
		if com.get('name',None):
			sim_com.append(com['name'])
	sim_com_dict[key] = sim_com
print ('found the list of similiar companies')

com_details_dict = {}
for key,value in rest_id_list.items():
	params = (
		('decoration', '(adsRule,affiliatedCompaniesWithEmployeesRollup,affiliatedCompaniesWithJobsRollup,articlePermalinkForTopCompanies,autoGenerated,backgroundCoverImage,claimable,claimableByViewer,companyEmployeesSearchPageUrl,companyPageUrl,coverPhoto,dataVersion,description,entityUrn,followingInfo,foundedOn,headquarter,jobSearchPageUrl,lcpTreatment,logo,name,type,overviewPhoto,paidCompany,partnerCompanyUrl,partnerLogo,permissions,pysmAvailable,rankForTopCompanies,recentNewsAvailable,salesNavigatorCompanyUrl,school,showcase,staffCount,staffCountRange,staffingCompany,topCompaniesListName,universalName,url,viewerConnectedToAdministrator,viewerEmployee,viewerPendingAdministrator,companyIndustries*,industries,specialities,acquirerCompany~(entityUrn,logo,name,industries,followingInfo,url,paidCompany,universalName),affiliatedCompanies*~(entityUrn,logo,name,industries,followingInfo,url,paidCompany,universalName),groups*~(entityUrn,largeLogo,groupName,memberCount,websiteUrl,url),showcasePages*~(entityUrn,logo,name,industries,followingInfo,url,description,universalName),ratingQuestions*~(entityUrn,description,ratingType,rating,aggregateRatingCount,aggregateRatingAverage,aggregateRatingDescription))'),
		('q', 'universalName'),
		('universalName', value),
	)

	response = requests.get('https://www.linkedin.com/voyager/api/organization/companies', headers=headers, params=params)
	com_det_json = json.loads(response.text)
	com_det_json = com_det_json['included']
	for com in com_det_json:
		if type(com) == dict and (com.get('staffcount',None) or com.get('description',None)):
			com_details_dict[key] = com
			break
			
for key,value in com_details_dict.items():
    a = dict((b,c) for b, c in value.items() if b in ['staffCount','description','industries','companyPageUrl','jobSearchPageUrl','universalName'])
    com_details_dict[key] = a
print ('found company details')

print ('now fetching employee details for each company.\
		This may take time because linked has created service such that you can fetch the details of 10 employees at a time.')
emp_details_dict = {}
emp_details_dict1 = {}
for key,value in rest_id_list.items():
	if key in emp_details_dict:
		continue
	employees = []
	for i in range(0,100000,10):
		print ('got employees for ' + key + ': ' + str(i))
		url = 'https://www.linkedin.com/voyager/api/search/cluster?count=10&guides=List(v-%3EPEOPLE,facetCurrentCompany-%3E'+str(value)+')&origin=OTHER&q=guided&start=' + str(i)
		response = requests.get(url, headers=headers)
		emp_list = json.loads(response.text)
		emp_list = emp_list['included']
		if len(emp_list) == 0:
			break
		else:
			for emp in emp_list:
				if 'firstName' in emp.keys():
					emp['urn'] = emp['entityUrn'].split(':')[-1]
					employees.append(emp)
				elif 'location' in emp.keys():
					emp['urn'] = emp['miniProfile'].split(':')[-1]
					employees.append(emp)
	
	lst = sorted(employees, key=lambda x:x['urn'])
	emp_details_dict[key] = employees
	list_c = []
	for k,v in groupby(lst, key=lambda x:x['urn']):
		d = {}
		for dct in v:
			d.update(dct)
		list_c.append(d)

	print('length of all the employees at ' + key + ': ' + str(len(list_c)))
	emp_details_dict1[key] = list_c

for key,value in emp_details_dict1.items():
	emp_list = []
	for val in value:
		if val['headless']:
			emp_list.append(dict([(b,c) for b, c in val.items() if b in ['firstName','lastName','occupation','location','industry','schools','companies']]))
			continue
		response = requests.get('https://www.linkedin.com/voyager/api/identity/profiles/' + val['publicIdentifier'] + '/profileView', headers=headers)
		a = json.loads(response.text)
		a = a['included']
		coms = [b for b in a if b.get('companyName',None)]

		for com in coms:
		    tp = com.get('timePeriod',None)
		    if tp:
		        st = tp + ',startDate'
		        st = [b for b in a if b.get('$id',None) == st]
		        et = tp + ',endDate'
		        et = [b for b in a if b.get('$id',None) == et]
		        if len(st) >0 :   
		        	com['joining'] = dict([(b,c) for b, c in st[0].items() if b in ['day','month','year']])
		        if len(et) > 0:
		        	com['lwd'] = dict([(b,c) for b, c in et[0].items() if b in ['day','month','year']])
		coms = [dict([(b,c) for b, c in com.items() if b in ['companyName','title','joining','lwd']]) for com in coms]
		val['companies'] = coms

		schools = [b for b in a if b.get('schoolName',None)]
		for com in schools:
		    tp = com.get('timePeriod',None)
		    if tp:
		        st = tp + ',startDate'
		        st = [b for b in a if b.get('$id',None) == st]
		        et = tp + ',endDate'
		        et = [b for b in a if b.get('$id',None) == et]
		        if len(st) >0 :   
		        	com['joining'] = dict([(b,c) for b, c in st[0].items() if b in ['day','month','year']])
		        if len(et) > 0:
		        	com['lwd'] = dict([(b,c) for b, c in et[0].items() if b in ['day','month','year']])

		schools = [dict([(b,c) for b, c in school.items() if b in ['fieldOfStudy','schoolName','joining','lwd']]) for school in schools]
		lst = sorted(schools, key=lambda x:x['schoolName'])
		list_c = []
		for k,v in groupby(lst, key=lambda x:x['schoolName']):
			d = {}
			for dct in v:
				d.update(dct)
			list_c.append(d)
		schools = list_c
		val['schools'] = schools
		emp_list.append(dict([(b,c) for b, c in val.items() if b in ['firstName','lastName','occupation','location','industry','schools','companies']]))
	emp_details_dict1[key] = emp_list


final_list = []
for key,value in rest_id_list.items():
    final_dict = {}
    final_dict['company'] = key
    final_dict['company_id'] = value
    final_dict['similiar_companies'] = sim_com_dict.get(key,None)
    final_dict['company_info'] = com_details_dict.get(key,None)
    final_dict['employees'] = emp_details_dict1.get(key,None)
    final_list.append(final_dict)

final_dict = {}
final_dict['companies'] = final_list


#with open('final_linkedin.json' , 'w') as fd:
with open('wes_linkedin.json' , 'w') as fd:
	json.dump(final_dict,fd)
