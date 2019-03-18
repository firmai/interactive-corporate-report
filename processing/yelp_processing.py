
import pandas as pd
import numpy as np
import os

#companies = ["BJRI", "TGIF", "CPKI", "RRGB", "CAKE", "CHIL", "APPB"]

my_path = os.path.abspath(os.path.dirname('__file__'))
path = os.path.join(my_path, "../input_fields.csv")

input_fields = pd.read_csv(path)

from os import listdir
from os.path import isfile, join


code = input_fields["code_or_ticker"]

for coy in code:

    my_path = os.path.abspath(os.path.dirname('__file__'))
    path = os.path.join(my_path, "../data/yelp/" + coy + "/")

    path_out = os.path.join(my_path, "../data/ratings/")

    onlyfiles = [f for f in listdir(path) if isfile(join(path, f))]

    if '.DS_Store' in onlyfiles:
        onlyfiles.remove('.DS_Store')

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

    def yelp_final(yelp):
        tak = len(yelp)

        yelp = yelp.sort_values("date", ascending=True)

        yelp["roll25"] = pd.rolling_mean(yelp["rating"], int(tak * 0.05) + 3)
        yelp["roll100"] = pd.rolling_mean(yelp["rating"], int(tak * 0.2))
        yelp["roll250"] = pd.rolling_mean(yelp["rating"], int(tak * 0.5))

        yelp["roll100"] = yelp["roll100"].fillna(yelp["roll25"])
        yelp["roll250"] = yelp["roll250"].fillna(yelp["roll100"])
        yelp["roll250"] = yelp["roll250"].fillna(yelp["roll25"])

        yelp = yelp.sort_values("date", ascending=False)

        yelp["special_25"] = pd.rolling_mean(yelp["rating"], int(tak * 0.05) + 3)

        yelp["special_25"] = yelp["special_25"] * .80 + yelp["rating"] * .10
        # Left 10% out here, that is okay I assume.

        yelp["roll100"] = yelp["roll100"].fillna(yelp["special_25"])
        yelp["roll25"] = yelp["roll25"].fillna(yelp["special_25"])
        yelp["roll250"] = yelp["roll250"].fillna(yelp["special_25"])

        yelp = yelp.sort_values("date", ascending=True)

        yelp["Final_Rating"] = yelp["roll25"] * .40 + yelp["roll100"] * .40 + yelp["roll100"] * .20

        # multiplier = df_tick["close"].tail(1).values[0]/yelp["Final_Rating"].tail(1).values[0]

        # yelp["Final_Rating"] = yelp["Final_Rating"] * multiplier
        # print(yelp["Final_Rating"].head())
        return yelp[["Final_Rating","date"]]


    from datetime import datetime
    from dateutil.parser import parse

    df_tick = pd.read_csv(path_out +coy+"_stock_rate.csv")

    # Range input and related index
    ras = pd.DataFrame()
    beg = pd.Timestamp('2010-05-15')
    end = pd.Timestamp('2017-12-15')
    idx = pd.DatetimeIndex(start=beg, end=end, freq='D')

    ras["date"] = idx

    df_tick["date"] = pd.to_datetime(df_tick["date"])
    r = -1
    for i in full_names:
        r = r + 1
        yp = pd.read_csv(path + i)
        small = small_names[r]
        yp["date"] = yp["date"].apply(lambda x: x[:10])
        yp["date"] = yp["date"].apply(lambda x: x[:-1] if x[-1] == "\\" else x)
        yp["date"] = yp["date"].apply(lambda x: x[:-2] if x[-1] == "n" else x)

        yp['date'] = yp['date'].apply(lambda x: parse(x))

        #yp["date"] = pd.to_datetime(yp["date"]) ### I uncommented this beast

        rp = yelp_final(yp)
        rp[small] = rp["Final_Rating"]
        ras = pd.merge(ras, rp[[small, "date"]], on="date", how="left")
        ras = ras.drop_duplicates("date")

    ras = ras.fillna(method="ffill")
    ras = ras.fillna(method="bfill")
    ras = ras.fillna(value=0)

    ras["date"] = pd.to_datetime(ras["date"])
    ras = ras[ras["date"] <= df_tick["date"].max()]
    ras = ras[ras["date"] > "2012-06-01"]

    ras["all"] = 0
    fas = ras
    fas["all"] = fas[fas.drop("date", axis=1).columns].sum(axis=1)
    fas["all"] = fas["all"] / len(fas.drop("date", axis=1).columns)

    fas.to_csv(path_out +"all_yelps_rates_"+coy+".csv", index=False)