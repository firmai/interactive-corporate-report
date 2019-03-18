import pandas as pd
import numpy as np
import json
import os
from datetime import *

my_path = os.path.abspath(os.path.dirname('__file__'))
path_in_ngrams = os.path.join(my_path, "../data/cpickle/")
my_path = os.path.abspath(os.path.dirname('__file__'))
path = os.path.join(my_path, "../input_fields.csv")

input_fields = pd.read_csv(path)

code = input_fields["code_or_ticker"]

from os import listdir
from os.path import isfile, join

code = input_fields["code_or_ticker"]
full_dict = {}

# code = code.iloc[0]
for coy in code:
    full_dict[coy] = {}

    my_path = os.path.abspath(os.path.dirname('__file__'))
    path = os.path.join(my_path, "../data/yelp_extra_info/" + coy + "/")

    path_out = os.path.join(my_path, "../data/extra_info/")

    onlyfiles = [f for f in listdir(path) if isfile(join(path, f))]

    names_final = []
    for li in onlyfiles:
        if len(li) > 15:
            li = li[:-4]
            names_final.append(li)

    rat = ""
    for li in onlyfiles:
        rat = rat + li + "-"

    from collections import Counter
    import re

    coun = Counter(rat.split("-"))

    ad = pd.DataFrame()

    ad["word"] = list(coun.keys())
    ad["number"] = list(coun.values())

    ad = ad.sort_values("number", ascending=False)

    ad = ad[~(np.abs(ad.number - ad.number.mean()) <= (3.2 * ad.number.std()))]

    ad.reset_index(inplace=True, drop=True)
    ad["word_1"] = "-" + ad["word"] + "-"
    ad["word_2"] = ad["word"] + "-"
    ad["word_3"] = "-" + ad["word"]

    ad["final"] = ad["word_1"]

    words = list(ad["final"].append(ad["word_2"]).append(ad["word_3"]).values)

    full_names = []
    small_names = []
    for i in range(len(onlyfiles)):
        my_string = onlyfiles[i]
        full_names.append(my_string)
        li = my_string
        if len(li) > 4:
            li = re.sub(r'|'.join(map(re.escape, list(words))), '', li)
            small_names.append(li[:-4])

    for big, small in zip(full_names, small_names):

        path = my_path + "/../data/yelp_extra_info/" + coy + "/" + big

        extra = pd.read_csv(path)

        extra_dict = {}

        extra_dict["hours_open"] = {}

        for i, h in zip(extra["Day"], extra["Hours Opened"]):
            try:
                if len(i) > 1:
                    extra_dict["hours_open"][i] = h
            except:
                continue

        extra_dict["business_info"] = {}

        for i, h in zip(extra["Business Info"], extra["Detail"]):
            try:
                if len(i) > 1:
                    extra_dict["business_info"][i] = h
            except:
                continue

        extra_dict["also_considered"] = {}

        for i, h in zip(extra["Also-Considered"], extra["Considered Link"]):
            try:
                if len(i) > 1:
                    extra_dict["also_considered"][i] = h
            except:
                continue

        extra_dict["also_viewed"] = {}

        for i, h in zip(extra["Also-Viewed"], extra["Viewed Link"]):
            try:
                if len(i) > 1:
                    extra_dict["also_viewed"][i] = h
            except:
                continue
        extra_dict["small_name"] = small

        full_dict[coy][big] = extra_dict

info_dict = {}
for i in full_dict.keys():
    info_dict[i] = {}
    for r in full_dict[i].keys():
        ext = full_dict[i][r]
        info_dict[i][r] = {}
        total_hours = 0
        for g, hours in ext["hours_open"].items():
            hours = hours.replace(' Open now', "")
            if hours == "Closed":
                continue
            if len(hours.split("-")) > 2:

                ga = hours.split("-")
                ra = ga[1].split(ga[1][6:9].replace(" ", ""))

                str_dict = {}
                a = -1
                for w in ra[:2]:
                    a = a + 1
                    if ga[1][6:9].replace(" ", "") not in w:
                        str_dict[a] = w + ga[1][6:9].replace(" ", "")

                time_1 = str_dict[0][1:]
                time_2 = str_dict[0][1:]

                t1 = datetime.strptime(time_1, '%I:%M %p')
                t2 = datetime.strptime(time_2, '%I:%M %p')
                diffy_dat = t2 - t1

                time_1 = hours.split("-")[0][:-1]

                time_2 = hours.split("-")[2][1:]

                t1 = datetime.strptime(time_1, '%I:%M %p')
                t2 = datetime.strptime(time_2, '%I:%M %p')
                tdiff = t2 - t1
                tdiff = tdiff - diffy_dat
            else:
                time_1 = hours.split("-")[0][:-1]

                time_2 = hours.split("-")[1][1:]

                t1 = datetime.strptime(time_1, '%I:%M %p')
                t2 = datetime.strptime(time_2, '%I:%M %p')
                tdiff = t2 - t1
            hours = tdiff.seconds / (60 * 60)
            total_hours = total_hours + hours
        info_dict[i][r]["total_hours"] = total_hours

list_infos = []
for i in full_dict.keys():
    for r in full_dict[i].keys():
        ext = full_dict[i][r]
        list_infos.extend(list(ext["business_info"].keys()))

list_infos.append("Small Name")
list_infos.append("Target Name")
list_infos.append("Hours Open")

new_frame = pd.DataFrame(index=list(set(list_infos)))

for i in full_dict.keys():
    for r in full_dict[i].keys():
        ext = full_dict[i][r]
        ext["business_info"]["Small Name"] = ext["small_name"]
        ext["business_info"]["Target Name"] = i
        ext["business_info"]["Hours Open"] = info_dict[i][r]["total_hours"]
        fa = pd.DataFrame.from_dict(ext["business_info"], orient='index', dtype=None)
        fa.columns = [r]
        new_frame = new_frame.join(fa, how="outer")

frame_t = new_frame.T
frame_t_2 = frame_t.fillna(frame_t.mode().T[0])

frame_t_2["Wi-Fi"] = frame_t_2["Wi-Fi"].replace(['Paid', 'Paid'], 'No')

frame_t_2["Noisy"] = frame_t_2['Noise Level'].replace(['Average', 'Quiet'], 'No')

frame_t_2["Noisy"] = frame_t_2["Noisy"].replace(['Loud', 'Very Loud'], 'Yes')

final_df = frame_t_2[
    ['Wi-Fi', 'Target Name', 'Hours Open', 'Takes Reservations', 'Outdoor Seating', 'Delivery', 'Caters',
     'Bike Parking', 'Accepts Apple Pay', 'Accepts Android Pay', 'Noisy']]

i_dict = {}

for ra in list(final_df["Target Name"].unique()):
    i_dict[ra] = {}
    for col in final_df.drop(['Target Name', 'Hours Open'], axis=1).columns:
        i_dict[ra][col] = final_df[final_df["Target Name"] == ra][col].value_counts(normalize=True).to_dict()
    i_dict[ra]["Average Hours"] = final_df[final_df["Target Name"] == ra][final_df["Hours Open"] > 10][
        "Hours Open"].mean()

import _pickle as pickle

path_out = os.path.join(my_path, "../data/yelp_extra_info/")
path_in_ngrams = os.path.join(my_path, "../data/cpickle/")

final_df.to_csv(path_out + "extra_info.csv")

pickle.dump(i_dict, open(path_in_ngrams+"i_dict.p", "wb"))

## Send to dictionary

path_in_file = os.path.join(my_path, "../input_fields.csv")

input_fields = pd.read_csv(path_in_file)