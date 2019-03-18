import os
import pandas as pd
import _pickle as pickle

my_path = os.path.abspath(os.path.dirname('__file__'))

path_in_ngrams = os.path.join(my_path, "data/cpickle/")

path_in_file = os.path.join(my_path, "input_fields.csv")


input_fields = pd.read_csv(path_in_file)

def dic(coy, bench, location):

    city = location

    figures_dict_c = pickle.load(open(path_in_ngrams + "figures_dict_" + coy + ".p", "rb"))
    figures_dict_b = pickle.load(open(path_in_ngrams + "figures_dict_" + bench + ".p", "rb"))

    from math import cos, asin, sqrt


    def distance(lat1, lon1, lat2, lon2):
        p = 0.017453292519943295
        a = 0.5 - cos((lat2 - lat1) * p) / 2 + cos(lat1 * p) * cos(lat2 * p) * (1 - cos((lon2 - lon1) * p)) / 2
        return 12742 * asin(sqrt(a))


    def closest(data, v):
        return min(data, key=lambda p: distance(v['lat'], v['lon'], p['lat'], p['lon']))


    lat_list = []
    lon_list = []
    name_list = []
    for key, values in figures_dict_b.items():
        location = key[1]
        name_list.append(location)
        lat = values["Response Data"]["coordinates"]["latitude"]
        lon = values["Response Data"]["coordinates"]["longitude"]
        lat_list.append(lat)
        lon_list.append(lon)

    das = [{"lat": lat, "lon": lon, "name": name} for lat, lon, name in zip(lat_list, lon_list, name_list)]

    coy_target = figures_dict_c[coy, city]

    v = {'lat': coy_target["Response Data"]["coordinates"]["latitude"],
         'lon': coy_target["Response Data"]["coordinates"]["longitude"]}
    print(closest(das, v))
    close = closest(das, v)
    return close