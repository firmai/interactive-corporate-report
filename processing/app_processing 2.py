import dash_html_components as html
import os
import pandas as pd
import processing.frames as fm
from os import listdir
from os.path import isfile, join
import numpy as np
import _pickle as pickle


my_path = os.path.abspath(os.path.dirname(__file__))
path = os.path.join(my_path, "../input_fields.csv")

input_fields = pd.read_csv(path)

short_codes  = input_fields["code_or_ticker"]

all_dict = {}
dict_all_coll = {}
for code_start in short_codes:

    ## Starting here

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

        with open(filename, "wb") as f:
            f.write(data)

        ff = pd.read_excel(filename)
        return ff

    #go
    s_metrics_df = fm.s_metrics_df
    c_metrics_df = fm.c_metrics_df


    r = 5
    if r>4:
        employee_sentiment = "happy"
    else:
        employee_sentiment = "unhappy"

    dict = {

        "title":"BJ’s Restaurant & Brewhouse",
        "location":"Jacksonville",
        "employees":"Employees are " + employee_sentiment + "." + "The company then bought 26.",
        "customers":"Customers are happy. The company then bought 26.",
        "shareholders":"Shareholders are happy. The company then bought 26.",
        "management":"Management is performing well. The company then bought 26."

    }
    #


    from datetime import datetime, timedelta

    now = datetime.now()

    #stock_price_desc = describe


    def make_dash_table(df):
        ''' Return a dash definitio of an HTML table for a Pandas dataframe '''
        table = []
        for index, row in df.iterrows():
            html_row = []
            for i in range(len(row)):
                html_row.append(html.Td([row[i]]))
            table.append(html.Tr(html_row))
        return table

    ##
    #df_perf_summary = pd.read_csv("17530.csv")

    # Function To Import Dictionary and Open IT.
    def load_dict(filename_):
        with open(filename_, 'rb') as f:
            ret_di = pd.read_pickle(f)
        return ret_di

    my_path = os.path.abspath(os.path.dirname(__file__))
    path = os.path.join(my_path, "../data/financial/")

    # And the specification of this table
    dict_frames = load_dict(path + 'data.pkl') # Much rather use this one


    df_fund_info = pd.read_csv('https://plot.ly/~jackp/17544.csv')
    df_fund_characteristics = pd.read_csv('https://plot.ly/~jackp/17542.csv')
    df_fund_facts = pd.read_csv('https://plot.ly/~jackp/17540.csv')
    df_bond_allocation = pd.read_csv('https://plot.ly/~jackp/17538.csv')

    ##### Addition One

    my_path = os.path.abspath(os.path.dirname('__file__'))
    path = os.path.join(my_path, "../data/yelp/" + code_start + "/")

    path_out = os.path.join(my_path, "../data/ratings/")

    onlyfiles_1 = [f for f in listdir(path) if isfile(join(path, f))]

    path_in_ngrams = os.path.join(my_path, "../data/cpickle/")

    figures_dict = pickle.load(open(path_in_ngrams + "figures_dict_"+code_start+".p", "rb"))

    onlyfiles = [key[1] for key in figures_dict.keys()]

    new_list = []
    for of in onlyfiles:
        address = figures_dict[code_start, of]["Response Data"]["location"]["display_address"]
        ak = ""
        for a in address:
            if ak == "":
                ak = ak + a
            else:
                ak = ak + ", " + a
        new_list.append(ak)

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
    a_small_names = []
    for i in range(len(onlyfiles)):
        my_string = onlyfiles[i]
        full_names.append(my_string)
        li = my_string
        if len(li) > 4:
            li = re.sub(r'|'.join(map(re.escape, list(words))), '', li)
            small_names.append(li)

            ga  = li.title()
            a_small_names.append(ga)

    codes_df = pd.DataFrame()
    codes_df["file"]=onlyfiles
    codes_df["address"] = new_list
    codes_df["small"] = a_small_names
    #print(codes_df[codes_df["small"]=="Glendale"]["address"].reset_index(drop=True)[0])

    available_locations = new_list

    location_start = new_list[0]

    small_loc = a_small_names[0]
    ###############


    my_path = os.path.abspath(os.path.dirname('__file__'))
    path = os.path.join(my_path, "../input_fields.csv")

    input_fields = pd.read_csv(path)
    input_fields = pd.read_csv(path)


    available_benchmarks = list(input_fields["code_or_ticker"].values)

    available_benchmarks.remove(code_start)

    available_benchmarks_small_names =  list(input_fields[input_fields["code_or_ticker"].isin(available_benchmarks)]["short_name"].reset_index(drop=True).values)

    tickers_loca = {}
    tickers_loca["All"] = code_start
    for i in available_locations:
        tickers_loca[i] = code_start


    """
    codes_bench = {}
    for i, t in zip(available_benchmarks, code_bench):
        codes_bench[i] = t
    """

    dict_collect = {}

    dict_collect["Available Benchmark"] = available_benchmarks
    dict_collect["Available Benchmark Small Name"]= available_benchmarks_small_names
    dict_collect["Full Location Name"] = location_start
    dict_collect["Small Presentable Name"] = small_loc
    dict_collect["File Name"] = onlyfiles
    dict_collect["Adapted Small Name"] = a_small_names
    dict_collect["Full Address"] = available_locations
    dict_collect["Location Dictionary With Ticker"] = tickers_loca




    #####dict_collect["Stakeholder Metrics"] = s_metrics_df
    #####dict_collect["Company Metrics"] = c_metrics_df
    #dict_collect["Sentiment Dictionary"] = dict
    #####dict_collect["Stock Dictionary"] = dict_frames
    #dict_collect["Extra_1"] = df_fund_info
    #dict_collect["Extra_2"] = df_fund_characteristics

    #dict_collect["Extra_3"] = df_fund_facts
    #dict_collect["Extra_4"] = df_bond_allocation

    #dict_collect["Figures Dictionary"] = figures_dict


    dict_all_coll[code_start]  =   dict_collect

my_path = os.path.abspath(os.path.dirname(__file__))

path = os.path.join(my_path, "../data/cpickle/")

pickle.dump(dict_all_coll, open(path + "dict_all_coll.p", "wb"))