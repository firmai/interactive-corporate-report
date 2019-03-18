from datetime import datetime, timedelta
import os
import pandas as pd
from datetime import datetime, date
from datetime import datetime, timedelta

### This is intrion procesing just for parent firms.

my_path = os.path.abspath(os.path.dirname('__file__'))
path = os.path.join(my_path, "../input_fields.csv")

input_fields = pd.read_csv(path).loc[:, :]

companies = input_fields["code_or_ticker"]

# tick  = [x for x in input_fields[input_fields["ticker"]!="PE"].ticker]

code = [x for x in input_fields[input_fields["parent"] == "Yes"]["code_or_ticker"]]
tick = [x for x in input_fields[input_fields["parent"] == "Yes"]["ticker"]]

year = int(2012)

import intrinio

intrinio.client.username = 'xxxxx'
intrinio.client.password = 'xxxxx'

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