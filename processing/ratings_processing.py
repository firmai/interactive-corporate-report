from __future__ import division


# Library Packages
import regex as re
import itertools as it
import spacy
import numpy as np
import pandas as pd


#### CRC has a better version of this and should be looked at.


# Settings
pd.set_option('display.max_columns', None)
pd.set_option('display.max_rows', None)
seed = 7
np.random.seed(seed)

import warnings

warnings.filterwarnings('ignore')


def front(self, n):
    return self.iloc[:, :n]


def back(self, n):
    return self.iloc[:, -n:]

from sklearn.preprocessing import StandardScaler
np.set_printoptions(threshold=np.nan)

from datetime import datetime
from dateutil.parser import parse
from nltk.sentiment.vader import SentimentIntensityAnalyzer as SIA
import re
from nltk.corpus import stopwords
from nltk.tokenize import wordpunct_tokenize
from sklearn.preprocessing import MinMaxScaler

# Entity Extraction From Review
import itertools as it
import spacy


def Standardisation(df):
    listed = list(df)
    scaler = StandardScaler()
    scaled = scaler.fit_transform(df)
    df = pd.DataFrame(scaled)
    df.columns = listed
    return df



# Like normalization, standardization can be useful, and even required in some
# machine learning algorithms when your time series data has input values with differing scales.


from pandas_datareader.google.daily import GoogleDailyReader
from datetime import datetime, timedelta


class FixedGoogleDailyReader(GoogleDailyReader):
    @property
    def url(self):
        return 'http://finance.google.com/finance/historical'


import os

my_path = os.path.abspath(os.path.dirname(__file__))
path = os.path.join(my_path, "../input_fields.csv")

input_fields = pd.read_csv(path)


companies = input_fields["code_or_ticker"]

#tick  = [x for x in input_fields[input_fields["ticker"]!="PE"].ticker]

tick  = [x for x in input_fields["code_or_ticker"]]
code  = [x for x in input_fields["code_or_ticker"]]

year = int(2008)

for tic, cod in zip(tick, code):


    start = datetime(year, 1, 1)
    end = datetime.now()
    df_tick = pd.DataFrame(
        FixedGoogleDailyReader(tic, start=start, end=end, chunksize=25, retry_count=3, pause=0.001, session=None).read())
    df_tick = df_tick.reset_index()
    df_tick = df_tick.rename(
        columns={'Volume': 'volume', 'Close': 'close', 'High': 'high', 'Low': 'low', 'Open': 'open', 'Date': 'date'})

    # bench = "MENU"

    # df_bench = pd.DataFrame(FixedGoogleDailyReader(bench, start=start, end=end, chunksize=25, retry_count=3, pause=0.001, session=None).read())
    # df_bench = df_bench.reset_index()
    # df_bench = df_bench.rename(columns={'Volume':'volume','Close':'close', 'High':'high', 'Low':'low', 'Open':'open', 'Date':'date'})

    def dala(glassdoor,tam):
        tak = len(glassdoor)
        glassdoor[tam] = glassdoor[tam].fillna(glassdoor[tam].mean())
        glassdoor["roll25"] = pd.rolling_mean(glassdoor[tam],int(tak*0.05)+3)
        glassdoor["roll100"] = pd.rolling_mean(glassdoor[tam],int(tak*0.2))
        glassdoor["roll250"] = pd.rolling_mean(glassdoor[tam],int(tak*0.5))

        glassdoor["roll100"] = glassdoor["roll100"].fillna(glassdoor["roll25"])
        glassdoor["roll250"] = glassdoor["roll250"].fillna(glassdoor["roll100"])
        glassdoor["roll250"] = glassdoor["roll250"].fillna(glassdoor["roll25"])

        glassdoor = glassdoor.sort_values("Review Date", ascending=False)

        glassdoor["special_25"] = pd.rolling_mean(glassdoor[tam],int(tak*0.05)+3)

        glassdoor["special_25"] = glassdoor["special_25"]*.80 + glassdoor[tam]*.10
        # Left 10% out here, that is okay I assume.

        glassdoor["roll100"] = glassdoor["roll100"].fillna(glassdoor["special_25"])
        glassdoor["roll25"] = glassdoor["roll25"].fillna(glassdoor["special_25"])
        glassdoor["roll250"] = glassdoor["roll250"].fillna(glassdoor["special_25"])

        glassdoor = glassdoor.sort_values("Review Date", ascending=True)

        glassdoor["Final_Rating"] = glassdoor["roll25"]*.60 + glassdoor["roll100"] *.30 + glassdoor["roll100"] *.10

        #multiplier = df_tick["close"].tail(1).values[0] / glassdoor["Final_Rating"].tail(1).values[0]

        #glassdoor["Final_Rating"] = glassdoor["Final_Rating"] * multiplier


        return glassdoor["Final_Rating"]
    #
    path = os.path.join(my_path, "../data/glassdoor/")

    glassdoor = pd.read_csv(path +cod +"_review.csv")

    # This is just the glassdoor processing step.


    glassdoor['Review Date'] = glassdoor['Review Date'].apply(lambda x: parse(x))

    # Good
    # Bad
    # Great
    # Severe

    glassdoor["Pros"] = glassdoor["Pros"].apply(lambda x: re.sub('<br\s*?>', '. ', x))
    glassdoor["Cons"] = glassdoor["Cons"].apply(lambda x: re.sub('<br\s*?>', '. ', x))
    glassdoor["Advice to Management"] = glassdoor["Advice to Management"].fillna(value="").apply(
        lambda x: re.sub('<br\s*?>', '. ', x))

    glassdoor["Location"] = glassdoor["Location"].fillna(value="np.nan, np.nan")

    glassdoor["Location"] = glassdoor["Location"].apply(lambda x: x.split(",")[0])


    glassdoor = glassdoor.sort_values("Review Date", ascending=True)

    glassdoor_clean = glassdoor
    for tam in ["Rating", "Work Life Balance", "Culture Values", "Career Opportunities", "Comp Benefits",
                "Senior Management"]:
        glassdoor["Final_" + tam] = dala(glassdoor, tam)


    my_path = os.path.abspath(os.path.dirname(__file__))
    path = os.path.join(my_path, "../data/yelp/"+cod+"/")

    path_out = os.path.join(my_path, "../data/ratings/")

    from os import listdir
    from os.path import isfile, join

    onlyfiles = [f for f in listdir(path) if isfile(join(path, f))]

###
    for file  in onlyfiles:

        yelp = pd.read_csv(path + file)

        yelp["date"] = yelp["date"].apply(lambda x: x[:10])
        yelp["date"] = yelp["date"].apply(lambda x: x[:-1] if x[-1]=="\\" else x )
        yelp["date"] = yelp["date"].apply(lambda x: x[:-2] if x[-1]=="n" else x )

        from datetime import datetime
        from dateutil.parser import parse

        yelp['date'] = yelp['date'].apply(lambda x: parse(x))


        yelp = yelp.sort_values("date", ascending=True)

        yelp["roll25"] = pd.rolling_mean(yelp["rating"],25)
        yelp["roll100"] = pd.rolling_mean(yelp["rating"],100)
        yelp["roll250"] = pd.rolling_mean(yelp["rating"],250)

        yelp["roll100"] = yelp["roll100"].fillna(yelp["roll25"])
        yelp["roll250"] = yelp["roll250"].fillna(yelp["roll100"])
        yelp["roll250"] = yelp["roll250"].fillna(yelp["roll25"])

        yelp = yelp.sort_values("date", ascending=False)

        yelp["special_25"] = pd.rolling_mean(yelp["rating"],25)

        yelp["special_25"] = yelp["special_25"]*.80 + yelp["rating"]*.10
        # Left 10% out here, that is okay I assume.

        yelp["roll100"] = yelp["roll100"].fillna(yelp["special_25"])
        yelp["roll25"] = yelp["roll25"].fillna(yelp["special_25"])
        yelp["roll250"] = yelp["roll250"].fillna(yelp["special_25"])

        yelp = yelp.sort_values("date", ascending=True)

        yelp["Final_Rating"] = yelp["roll25"]*.40 + yelp["roll100"] *.40 + yelp["roll100"] *.20

        #multiplier = df_tick["close"].tail(1).values[0]/yelp["Final_Rating"].tail(1).values[0]

        #yelp["Final_Rating"] = yelp["Final_Rating"] * multiplier
        yelp = yelp[yelp["date"] > "2012-01-01"]

        yelp = yelp[yelp["date"] > "2012-01-01"]
        yelp.to_csv(path_out +file[:-4] + "_customer_ratings.csv")


    glassdoor = glassdoor[glassdoor["Review Date"]>"2012-01-01"]
    df_tick = df_tick[df_tick["date"]>"2012-01-01"]



    glassdoor_clean["manager"] = glassdoor_clean["Employee Title"].apply(lambda x:1 if "Manager" in str(x) else 0)

    glassdoor_m = glassdoor_clean[glassdoor_clean["manager"]==1]

    for tam in ["Rating","Work Life Balance","Culture Values","Career Opportunities","Comp Benefits","Senior Management"]:
        glassdoor_m["Final_"+tam] = dala(glassdoor_m,tam)


    glassdoor = glassdoor[glassdoor["Review Date"]>"2012-01-01"]
    glassdoor_m = glassdoor_m[glassdoor_m["Review Date"]>"2012-01-01"]


    # Date processing. ANd M
    glassdoor["Review Date"] = pd.to_datetime(glassdoor["Review Date"])
    glassdoor_m["Review Date"] = pd.to_datetime(glassdoor_m["Review Date"])
    df_tick["date"] = pd.to_datetime(df_tick["date"])

    kas = pd.DataFrame()
    beg = pd.Timestamp('2010-05-15')
    end = pd.Timestamp('2017-12-15')
    idx = pd.DatetimeIndex(start=beg, end=end, freq='D')

    kas["date"] = idx

    glassdoor_m = pd.merge(kas, glassdoor_m, left_on="date", right_on="Review Date", how="left")

    glassdoor_fake = pd.merge(kas, glassdoor, left_on="date", right_on="Review Date", how="left")


    glassdoor_m = pd.merge(glassdoor_fake, glassdoor_m,on="date",how="left")


    glassdoor_m = glassdoor_m[glassdoor_m["date"]>"2012-01-01"]

    glassdoor_m = glassdoor_m[glassdoor_m["date"]<=df_tick["date"].max()]

    glassdoor_m.reset_index(drop=True, inplace=True)

    glassdoor_m.fillna(method="ffill", inplace=True)

    glassdoor_m.fillna(method="bfill", inplace=True)


    glassdoor_m["trace_mse"] = ((((glassdoor_m["Final_Rating_y"]+ glassdoor_m["Final_Senior Management_y"]+glassdoor_m["Final_Work Life Balance_y"]+glassdoor_m["Final_Culture Values_y"]+glassdoor_m["Final_Career Opportunities_y"]+glassdoor_m["Final_Comp Benefits_y"])/6)+glassdoor_m["Final_Rating_x"])/2)

    glassdoor_m["trace_mwlb"] = (glassdoor_m["Final_Work Life Balance_x"]+glassdoor_m["Final_Work Life Balance_y"])/2

    glassdoor_m["trace_mcva"] = (glassdoor_m["Final_Culture Values_x"]+glassdoor_m["Final_Culture Values_y"])/2
    glassdoor_m["trace_mcop"] = (glassdoor_m["Final_Career Opportunities_x"]+glassdoor_m["Final_Career Opportunities_y"])/2
    glassdoor_m["trace_mcbe"] = (glassdoor_m["Final_Comp Benefits_x"]+glassdoor_m["Final_Comp Benefits_y"])/2
    glassdoor_m["trace_msma"] = (glassdoor_m["Final_Senior Management_x"]+glassdoor_m["Final_Senior Management_y"])/2




    df_tick = df_tick[df_tick["date"]>"2012-01-01"]


    glassdoor = glassdoor[glassdoor["Review Date"]<=df_tick["date"].max()]

    glassdoor.to_csv(path_out + cod +"_gdoor_employee_rate.csv")
    glassdoor_m.to_csv(path_out + cod +"_gdoor_mgmt_rate.csv")

    multiplier = (glassdoor_m["trace_mse"].tail(1)).values[0]/df_tick["close"].tail(1).values[0]

    df_tick["close"] = df_tick["close"] * multiplier


    df_tick.to_csv(path_out + cod +"_stock_rate.csv")


### Fixer which allows you to delete some of the above, but you are too lazy:

my_path = os.path.abspath(os.path.dirname('__file__'))
path = os.path.join(my_path, "../input_fields.csv")
path_in = os.path.join(my_path, "../data/ratings/")

input_fields = pd.read_csv(path)

code = input_fields["code_or_ticker"]

#df_tick_1= pd.read_csv(path_in +c + "_stock_rate.csv")

path_sto = os.path.join(my_path, "../data/stock/")
path_out = os.path.join(my_path, "../data/ratings/")
for c in code:
    df_tick = pd.read_csv(path_sto + c + "_tick_df.csv")

    ## This is normalised, but I don't see why I shouldn't
    df_tick = df_tick.fillna(method="bfill").fillna(method="ffill")

    df_tick["date"] = pd.to_datetime(df_tick["date"], infer_datetime_format=True)

    df_tick = df_tick[["close", "date"]]

    df_tick = df_tick[df_tick["date"]>"2012-01-01"]

    glassdoor_m= pd.read_csv(path_in +c + "_gdoor_mgmt_rate.csv")

    multiplier = (glassdoor_m["trace_mse"].tail(1)).values[0]/df_tick["close"].tail(1).values[0]

    df_tick["close"] = df_tick["close"] * multiplier

    df_tick.to_csv(path_out + c +"_stock_rate.csv")