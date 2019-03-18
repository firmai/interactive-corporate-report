import dash_html_components as html
import os
import pandas as pd
import processing.frames as fm
from os import listdir
from os.path import isfile, join
import numpy as np
import _pickle as pickle



# After this you have to run first page_execution - can actually combine the two
### NB App_processing.py is inextricably linked with frames without which no output can be obtained.

my_path = os.path.abspath(os.path.dirname(__file__))
path = os.path.join(my_path, "../input_fields.csv")

input_fields = pd.read_csv(path)

short_codes  = input_fields["code_or_ticker"]

all_dict = {}
dict_all_coll = {}
for target_code in short_codes:

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

    def load_dict(filename_):
        with open(filename_, 'rb') as f:
            ret_di = pd.read_pickle(f)
        return ret_di


    my_path = os.path.abspath(os.path.dirname(__file__))
    path = os.path.join(my_path, "../data/financial/")
    dict_frames = load_dict(path + 'data.pkl')


    import datetime


    s = ["'" + str(int(str(datetime.datetime.now().year)[-2:]) - 5 + i) for i in range(5)]
    s2 = [str(int(str(datetime.datetime.now().year)) - 5 + i) for i in range(5)]

    #go
   # s_metrics_df = fm.s_metrics_df
    #c_metrics_df = fm.c_metrics_df

    my_path = os.path.abspath(os.path.dirname('__file__'))
    path = os.path.join(my_path, "../data/closure/")
    new_frame = pd.read_csv(path + "stakeholder_metrics.csv")
    new_frame = new_frame.set_index("Unnamed: 0")
    print(new_frame)

    print(target_code)

    pcaframe = dict_frames[target_code, 'calculations', 'Principal Component']

    for col in pcaframe.columns:
        pcaframe[col + "_direction"] = pcaframe[col] > pcaframe[col].shift()

    for col in pcaframe.iloc[:, :3].columns:
        pcaframe[col + "_direction"] = pcaframe[col + "_direction"].apply(lambda x: "↓" if x == False else "↑")

    s_metrics_df = pd.DataFrame([["Type", "E", "C", "S", "M", "A", "BA"],
                                 ["Sentiment", new_frame[new_frame.index==target_code].round(1)["Employees"].values[0],
                                  new_frame[new_frame.index==target_code].round(1)["Customers"].values[0],
                                  new_frame[new_frame.index==target_code].round(1)["Valuation Part"].values[0],
                                  new_frame[new_frame.index==target_code].round(1)["Management"].values[0],
                                  new_frame[new_frame.index==target_code].round(1)["Mean"].values[0],
                                  round(new_frame["Mean"].mean(),1)] ])

    not_listed = input_fields[input_fields["listed"] == "No"].reset_index(drop=True)["code_or_ticker"]

    if target_code in list(not_listed):

        c_metrics_df = pd.DataFrame([["Year", s[0], s[1], s[2], s[3], s[4]],
                                     ["Solvency", "N", "N", "N", "N", "N"],
                                     ["Efficiency", "N", "N", "N", "N", "N"],
                                     ["Profitability", "N", "N", "N", "N", "N"],
                                     ["Liquidity", "N", "N", "N", "N", "N"]])
    else:

        c_metrics_df = pd.DataFrame([["Year", s[0], s[1], s[2], s[3], s[4]],
                                     ["Solvency",
                                      pcaframe[pcaframe["year"]==int(s2[0])]["solvency_direction"].values[0],
                                      pcaframe[pcaframe["year"] == int(s2[1])]["solvency_direction"].values[0],
                                      pcaframe[pcaframe["year"] == int(s2[2])]["solvency_direction"].values[0],
                                      pcaframe[pcaframe["year"] == int(s2[3])]["solvency_direction"].values[0],
                                      pcaframe[pcaframe["year"] == int(s2[4])]["solvency_direction"].values[0]],
                                     ["Efficiency",
                                      pcaframe[pcaframe["year"]==int(s2[0])]["efficiency_direction"].values[0],
                                      pcaframe[pcaframe["year"] == int(s2[1])]["efficiency_direction"].values[0],
                                      pcaframe[pcaframe["year"] == int(s2[2])]["efficiency_direction"].values[0],
                                      pcaframe[pcaframe["year"] == int(s2[3])]["efficiency_direction"].values[0],
                                      pcaframe[pcaframe["year"] == int(s2[4])]["efficiency_direction"].values[0]],
                                     ["Profitability",
                                      pcaframe[pcaframe["year"]==int(s2[0])]["profitability_direction"].values[0],
                                      pcaframe[pcaframe["year"] == int(s2[1])]["profitability_direction"].values[0],
                                      pcaframe[pcaframe["year"] == int(s2[2])]["profitability_direction"].values[0],
                                      pcaframe[pcaframe["year"] == int(s2[3])]["profitability_direction"].values[0],
                                      pcaframe[pcaframe["year"] == int(s2[4])]["profitability_direction"].values[0]],
                                     ["Liquidity",
                                      pcaframe[pcaframe["year"]==int(s2[0])]["liquidity_direction"].values[0],
                                      pcaframe[pcaframe["year"] == int(s2[1])]["liquidity_direction"].values[0],
                                      pcaframe[pcaframe["year"] == int(s2[2])]["liquidity_direction"].values[0],
                                      pcaframe[pcaframe["year"] == int(s2[3])]["liquidity_direction"].values[0],
                                      pcaframe[pcaframe["year"] == int(s2[4])]["liquidity_direction"].values[0]]])

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
    path = os.path.join(my_path, "../data/yelp/" + target_code + "/")

    path_out = os.path.join(my_path, "../data/ratings/")

    all_target_location_file_names_1 = [f for f in listdir(path) if isfile(join(path, f))]

    path_in_ngrams = os.path.join(my_path, "../data/cpickle/")

    figures_dict = pickle.load(open(path_in_ngrams + "figures_dict_"+target_code+".p", "rb"))

    all_target_location_file_names = [key[1] for key in figures_dict.keys()]

    new_list = []
    for of in all_target_location_file_names:
        address = figures_dict[target_code, of]["Response Data"]["location"]["display_address"]
        ak = ""
        for a in address:
            if ak == "":
                ak = ak + a
            else:
                ak = ak + ", " + a
        new_list.append(ak)

    rat = ""
    for li in all_target_location_file_names:
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
    all_target_location_small_names = []
    for i in range(len(all_target_location_file_names)):
        my_string = all_target_location_file_names[i]
        full_names.append(my_string)
        li = my_string
        if len(li) > 4:
            li = re.sub(r'|'.join(map(re.escape, list(words))), '', li)
            small_names.append(li)

            ga  = li.title()
            all_target_location_small_names.append(ga)

    codes_df = pd.DataFrame()
    codes_df["file"]=all_target_location_file_names
    codes_df["address"] = new_list
    codes_df["small"] = all_target_location_small_names
    #print(codes_df[codes_df["small"]=="Glendale"]["address"].reset_index(drop=True)[0])

    all_target_location_full_addresses = new_list

    location_start = new_list[0]

    small_loc = all_target_location_small_names[0]
    ###############


    my_path = os.path.abspath(os.path.dirname('__file__'))
    path = os.path.join(my_path, "../input_fields.csv")

    input_fields = pd.read_csv(path)
    input_fields = pd.read_csv(path)


    all_benchmark_codes = list(input_fields["code_or_ticker"].values)

    all_benchmark_codes.remove(target_code)

    all_benchmark_small_names =  list(input_fields[input_fields["code_or_ticker"].isin(all_benchmark_codes)]["short_name"].reset_index(drop=True).values)

    tickers_loca = {}
    tickers_loca["All"] = target_code
    for i in all_target_location_full_addresses:
        tickers_loca[i] = target_code

    """
    codes_bench = {}
    for i, t in zip(all_benchmark_codes, code_bench):
        codes_bench[i] = t
    """

    dict_collect = {}

    dict_collect["All Benchmark Codes"] = all_benchmark_codes
    dict_collect["All Benchmark Small Names"]= all_benchmark_small_names
    dict_collect["All Target Location File Names"] = all_target_location_file_names
    dict_collect["All Target Location Small Names"] = all_target_location_small_names
    dict_collect["All Target Location Full Addresses"] = all_target_location_full_addresses

    dict_collect["Stakeholder Metrics"] = s_metrics_df
    dict_collect["Company Metrics"] = c_metrics_df
    dict_collect["Sentiment Dictionary"] = dict
    dict_collect["Stock Dictionary"] = dict_frames
    dict_collect["Figures Dictionary"] = figures_dict

    dict_all_coll[target_code]  =   dict_collect

my_path = os.path.abspath(os.path.dirname(__file__))

path = os.path.join(my_path, "../data/cpickle/")

pickle.dump(dict_all_coll, open(path + "ext_info_dict.p", "wb"))