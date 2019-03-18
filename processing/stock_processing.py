#####################
"""    Also Run   """
##Figures Processing##
#####################


### I actually replaced this with intrintio.

import pandas as pd
import os
import _pickle as pickle


def db_frame(url):
    url = url.replace("dl=0", "dl=1")  # dl=1 is important

    import urllib.request
    u = urllib.request.urlopen(url)
    data = u.read()
    u.close()

    def find_between_r(s, first, last):
        try:
            start = s.rindex(first) + len(first)
            end = s.rindex(last, start)
            return s[start:end]
        except ValueError:
            return ""

    filename = find_between_r(url, "/", "?")
    print(filename)

    with open(str(filename), "wb") as f:
        f.write(data)

    ff = pd.read_excel(filename)
    return ff


competitors_df = db_frame("https://www.dropbox.com/s/hbsz0uod7w5dsxl/competitors.xlsx?dl=0")



from pandas_datareader.google.daily import GoogleDailyReader
from datetime import datetime, timedelta


class FixedGoogleDailyReader(GoogleDailyReader):
    @property
    def url(self):
        return 'http://finance.google.com/finance/historical'



from pandas_datareader.google.daily import GoogleDailyReader
from datetime import datetime, timedelta


class FixedGoogleDailyReader(GoogleDailyReader):
    @property
    def url(self):
        return 'http://finance.google.com/finance/historical'

def comp_tick(comp_ticks, comp_weight, df_tick):
    df_final = pd.DataFrame(index=df_tick.index)
    df_final["close"] = 0
    df_frame = pd.DataFrame()

    for bench, weight in zip(comp_ticks, comp_weight):
        start = datetime(year, 1, 1)
        end = datetime.now()

        df_bench = pd.DataFrame(
            FixedGoogleDailyReader(bench, start=start, end=end, chunksize=25, retry_count=3, pause=0.001,
                                   session=None).read())
        df_bench = df_bench.reset_index()
        df_bench = df_bench.rename(
            columns={'Volume': 'volume', 'Close': 'close', 'High': 'high', 'Low': 'low', 'Open': 'open',
                     'Date': 'date'})

        df_bench = pd.merge(df_tick[["date", "low"]], df_bench[["date", "close"]], how="left")
        df_bench["close"] = df_bench["close"].fillna(method="bfill")
        df_bench["close"] = df_bench["close"].fillna(method="ffill")
        df_bench["close"] = df_bench["close"].fillna(df_bench["close"].mean())
        df_bench["close"] = df_bench["close"].fillna(value=0)
        df_bench["close"] = df_bench["close"] * 100 / df_bench["close"].iloc[0]

        #     print(bench)
        #     print(df_bench.iloc[276])

        df_final["close"] = df_final["close"] + df_bench["close"] * float(weight)
        df_frame[str(bench)] = df_bench["close"]

    df_final["date"] = df_tick["date"]

    df_final["close"] = df_final["close"] * 100 / df_final["close"].iloc[0]

    df_final["date"] = pd.to_datetime(df_final["date"], format="%Y-%m-%d")


    return df_final, df_frame


tick = "BJRI"
year = int(2012)

my_path = os.path.abspath(os.path.dirname(__file__))
path = os.path.join(my_path, "../input_fields.csv")
input_fields = pd.read_csv("../input_fields.csv")

start = datetime(year, 1, 1)
end = datetime.now()
df_tick = pd.DataFrame(
    FixedGoogleDailyReader(tick, start=start, end=end, chunksize=25, retry_count=3, pause=0.001, session=None).read())
df_tick = df_tick.reset_index()
df_tick = df_tick.rename(
    columns={'Volume': 'volume', 'Close': 'close', 'High': 'high', 'Low': 'low', 'Open': 'open', 'Date': 'date'})
df_tick["close"] = df_tick["close"] * 100 / df_tick["close"].iloc[0]


# Same as above but for any and all firms
df_all = {}

code = input_fields["code_or_ticker"]


for tick, code in zip(input_fields[input_fields["ticker"]!="PE"].ticker,code):

    start = datetime(year, 1, 1)
    end = datetime.now()
    df_tick = pd.DataFrame(
        FixedGoogleDailyReader(tick, start=start, end=end, chunksize=25, retry_count=3, pause=0.001, session=None).read())
    df_tick = df_tick.reset_index()
    df_tick = df_tick.rename(
        columns={'Volume': 'volume', 'Close': 'close', 'High': 'high', 'Low': 'low', 'Open': 'open', 'Date': 'date'})
    df_tick["close"] = df_tick["close"] * 100 / df_tick["close"].iloc[0]

    df_all[tick] = df_tick


    # bench = "MENU"

    # df_bench = pd.DataFrame(FixedGoogleDailyReader(bench, start=start, end=end, chunksize=25, retry_count=3, pause=0.001, session=None).read())
    # df_bench = df_bench.reset_index()
    # df_bench = df_bench.rename(columns={'Volume':'volume','Close':'close', 'High':'high', 'Low':'low', 'Open':'open', 'Date':'date'})


    df_final, df_frame = comp_tick(competitors_df["Ticker"], competitors_df["Weight"], df_tick)

    df_frame[tick] = df_final["close"]
    corrs = df_frame.corr()[tick].sort_values(ascending=False)
    five = corrs.ix[1:6].index.values

    df_final_filt, _ = comp_tick(five, [1 / five.shape[0] for i in list(range(five.shape[0]))], df_tick)

    import numpy as np

    hack = np.array([five[0], five[0]])

    # All Menu Firms
    df_final_one, _ = comp_tick(hack, [1 / hack.shape[0] for i in list(range(hack.shape[0]))], df_tick)

    my_path = os.path.abspath(os.path.dirname(__file__))
    path_out = os.path.join(my_path, "../data/stock/")
    print(path_out)

    pickle.dump(df_all, open(path_out + "_all_stocks_df.p", "wb"))

    # Correlated Five
    df_final_filt.to_csv(path_out + code + "_comp_f_df.csv")

    # Most Correlated
    df_final_one.to_csv(path_out +  code + "_comp_o_df.csv")

    # All Competitor Firms
    df_final.to_csv(path_out +  code + "_comp_df.csv")

    # Selected Firm
    df_tick.to_csv(path_out + code + "_tick_df.csv")

    print("done")

from datetime import datetime, timedelta
import os
import pandas as pd
from datetime import datetime, date
from datetime import datetime, timedelta

my_path = os.path.abspath(os.path.dirname('__file__'))
path = os.path.join(my_path, "../input_fields.csv")

input_fields = pd.read_csv(path).loc[:, :]

companies = input_fields["code_or_ticker"]

# tick  = [x for x in input_fields[input_fields["ticker"]!="PE"].ticker]

code = [x for x in input_fields[input_fields["parent"] == "Yes"]["code_or_ticker"]]
tick = [x for x in input_fields[input_fields["parent"] == "Yes"]["ticker"]]

year = int(2007)

import intrinio

intrinio.client.username = 'xxxxx'
intrinio.client.password = 'xxxx'

for tic, cod in zip(tick, code):
    # for tic, code in zip(["BKC"],["BKC"]):
    start = datetime(year, 1, 1)
    end = datetime.now()
    r = intrinio.prices(tic, start_date=str(year) + '-01-01')
    df_tick = r.rename(columns={'adj_volume': 'volume'})
    df_tick = df_tick.reset_index()
    df_tick = df_tick.rename(
        columns={'Volume': 'volume', 'Close': 'close', 'High': 'high', 'Low': 'low', 'Open': 'open', 'Date': 'date'})
    my_path = os.path.abspath(os.path.dirname('__file__'))
    path = os.path.join(my_path, "../data/stock/")

    df_tick.to_csv(path + cod + "_parent_tick_df.csv")