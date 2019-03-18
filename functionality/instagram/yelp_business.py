# We import the requests module which allows us to make the API call
import requests

# Replace [app_id] with the App ID and [app_secret] with the App Secret
app_id = 'xxxxxxxx'
app_secret = 'xxxxxxx'
data = {'grant_type': 'client_credentials',
        'client_id': app_id,
        'client_secret': app_secret}
token = requests.post('https://api.yelp.com/oauth2/token', data=data)
access_token = token.json()['access_token']
headers = {'Authorization': 'bearer %s' % access_token}

# Call Yelp API to pull business data for Kiku Sushi
biz_id = 'kiku-sushi-burnaby'
url = 'https://api.yelp.com/v3/businesses/%s' % biz_id
response = requests.get(url=url, headers=headers)
response_data = response.json()
