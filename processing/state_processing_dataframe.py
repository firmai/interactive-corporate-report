import plotly.plotly as py
import pandas as pd
import numpy as np
import os
import _pickle as pickle

# rd = pd.read_csv('https://raw.githubusercontent.com/plotly/datasets/master/2011_us_ag_exports.csv')


my_path = os.path.abspath(os.path.dirname('__file__'))
path_in_file = os.path.join(my_path, "../data/google/addresses_google.csv")
df_own = pd.read_csv(path_in_file)

path_in_ngrams = os.path.join(my_path, "../data/cpickle/")


df_own = df_own[df_own["country"] == "United States"].reset_index(drop=True)

df_own = df_own.fillna(df_own.mean())

df_own = df_own.rename(columns={"city_long": "state", "city_short": "code", "Female": "Female Rating"
    , "Male": "Male Rating", "Patrons": "Patrons Rating", 'Average Customer Network': 'Connectedness',
                                "Male": "Male Rating", "Patrons": "Patrons Rating",
                                'Food Aestheticist': 'Food Aestheticist Rating',
                                'High Network': 'High Network Rating', 'Low Network': 'Low Network Rating',
                                'Connoisseur': 'Connoisseur Rating'})

df_own.loc[:, ["Total Network", "Number of Reviewers"]] = df_own.loc[:,
                                                          ["Total Network", "Number of Reviewers"]].applymap(np.int32)

df_own.loc[:, ['Male to Female', 'Foreign to Local',
               'Male Rating', 'Female Rating', 'Local', 'Foreign',
               'High Network Rating', 'Low Network Rating', 'Connoisseur Rating',
               'Food Aestheticist Rating', 'Patrons Rating', 'First Visit',
               'Visual Importance', 'Female Importance', 'Foreign Importance',
               'Connectedness', 'Average Rating']] = df_own.loc[:, ['Male to Female', 'Foreign to Local',
                                                                    'Male Rating', 'Female Rating', 'Local', 'Foreign',
                                                                    'High Network Rating', 'Low Network Rating',
                                                                    'Connoisseur Rating',
                                                                    'Food Aestheticist Rating', 'Patrons Rating',
                                                                    'First Visit',
                                                                    'Visual Importance', 'Female Importance',
                                                                    'Foreign Importance',
                                                                    'Connectedness', 'Average Rating']].applymap(
    np.float32).round(3)

df_own.replace({'county': {'Anchorage': 'Anchorage Borough', 'Fairbanks North Star': 'Fairbanks North Star Borough',
                           'Matanuska-Susitna': 'Matanuska-Susitna Borough'}})

df_own["county_state"] = df_own["county"] + ", " + df_own["code"]

us = df_own[df_own["country"] == "United States"].reset_index(drop=True)

sep = us[["Total Network", "Number of Reviewers", "code"]]

us = us.drop(["Total Network", "Number of Reviewers"], axis=1)
all_firms_mean = us.groupby("code").mean().reset_index()
all_firms_sum = sep.groupby("code").sum().reset_index()
all_firms = pd.concat((all_firms_mean, all_firms_sum), axis=1)

all_firms.drop(["Unnamed: 0"], axis=1, inplace=True)
all_firms = all_firms.iloc[:, 1:]

all_dicts = {}
for i in df_own["target_small_name"].unique():
    firm_lvl = df_own[df_own["target_small_name"] == i].reset_index()
    sep_fir = firm_lvl[["Total Network", "Number of Reviewers", "code"]]
    firm_lvl = firm_lvl.drop(["Total Network", "Number of Reviewers"], axis=1)
    firm_lvl = firm_lvl.groupby("code").mean().reset_index()
    sep_fir = sep_fir.groupby("code").sum().reset_index()
    firms = pd.concat((firm_lvl, sep_fir), axis=1)

    firms.drop(["index", "Unnamed: 0"], axis=1, inplace=True)
    firms = firms.iloc[:, 1:]
    all_dicts[i] = firms

all_dicts["All"] = all_firms

pickle.dump(all_dicts, open(path_in_ngrams + "all_dicts_state.p", "wb"))


# go = input_fields["short_name"].tolist()
# go.append("All")
# [dict(args=['z', value["Female"] ], label=key, method='restyle') for key, value in all_dicts.items()]

# updatemenus=list([dict(buttons = [[dict(args=['z', value["Female"] ], label=key, method='update') for key, value in all_dicts.items()]])])