
import _pickle as pickle
import pandas as pd
from urllib.request import urlopen
import json
import os

my_path = os.path.abspath(os.path.dirname('__file__'))

path_in_ngrams = os.path.join(my_path, "../data/cpickle/")

def getplace(lat, lon):
    url = "http://maps.googleapis.com/maps/api/geocode/json?"
    url += "latlng=%s,%s&sensor=false" % (lat, lon)
    v = urlopen(url).read()
    j = json.loads(v)
    components = j['results'][0]['address_components']
    country = town = None
    for c in components:
        if "country" in c['types']:
            country = c['long_name']
        if "postal_town" in c['types']:
            town = c['long_name']
    return town, country

df = pickle.load(open(path_in_ngrams + "map_dict.p", "rb"))

df["country"] = ""
df["city_long"] = ""
df["city_short"] = ""
df["county"] = ""
df["city"] = ""
df["street"] = ""

df = df.reset_index(drop=True)

# df = df.iloc[:10,:]

r = 0
for lat, lon, ind in zip(df["lat"], df["lon"], df.index):
    r = r + 1
    if r < 1500:
        key = "AIzaSyB2RTyD0EzJFoUKGAejjB5vTea_q6MbMTs"
    if r > 1499:
        key = "AIzaSyAkcyotx1poTVloe-0N3465LOzOLypKHDk"

    url = "https://maps.googleapis.com/maps/api/geocode/json?"
    url += "latlng=%s,%s&sensor=false&key=%s" % (lat, lon, key)
    print(url)
    v = urlopen(url).read()
    j = json.loads(v)
    components = j['results'][0]['address_components']
    country = town = None
    for c in components:
        if "country" in c['types']:
            country = c['long_name']
            df["country"].iloc[ind] = country
        if "administrative_area_level_1" in c['types']:
            city_long = c['long_name']
            city_short = c['short_name']
            df["city_short"].iloc[ind] = city_short
            df["city_long"].iloc[ind] = city_long
        if "administrative_area_level_2" in c['types']:
            county = c['long_name']
            df["county"].iloc[ind] = county
        if "locality" in c['types']:
            city = c['long_name']
            df["city"].iloc[ind] = city
        if "route" in c['types']:
            street = c['long_name']
            df["street"].iloc[ind] = street

df_1 = pickle.load(open(path_in_ngrams + "map_dict.p", "rb"))

df["Average Rating"] = df_1["Average Rating"]
my_path = os.path.abspath(os.path.dirname('__file__'))
path_in_file = os.path.join(my_path, "..data/google/addresses_google.csv")
df.to_csv(path_in_file)