# df.to_csv("bla.csv")

import plotly.plotly as py
import pandas as pd
import numpy as np
import os

# rd = pd.read_csv('https://raw.githubusercontent.com/plotly/datasets/master/2011_us_ag_exports.csv')


my_path = os.path.abspath(os.path.dirname('__file__'))
path_in_file = os.path.join(my_path, "../data/google/addresses_google.csv")
df_own = pd.read_csv(path_in_file)

path_in_ngrams = os.path.join(my_path, "../data/cpickle/")

all_dicts_county = {}

for i in df_own["target_small_name"].unique():
    df_own = pd.read_csv(path_in_file)

    df_own = df_own[df_own["country"] == "United States"].reset_index(drop=True)

    df_own = df_own[df_own["target_small_name"] == i].reset_index(drop=True)

    df_own = df_own.fillna(df_own.mean())

    df_own = df_own.rename(columns={"city_long": "state", "city_short": "code", "Female": "Female Rating"
        , "Male": "Male Rating", "Patrons": "Patrons Rating", 'Average Customer Network': 'Connectedness',
                                    "Male": "Male Rating", "Patrons": "Patrons Rating",
                                    'Food Aestheticist': 'Food Aestheticist Rating',
                                    'High Network': 'High Network Rating', 'Low Network': 'Low Network Rating',
                                    'Connoisseur': 'Connoisseur Rating'})

    df_own.loc[:, ["Total Network", "Number of Reviewers"]] = df_own.loc[:,
                                                              ["Total Network", "Number of Reviewers"]].applymap(
        np.int32)

    df_own.loc[:, ['Male to Female', 'Foreign to Local',
                   'Male Rating', 'Female Rating', 'Local', 'Foreign',
                   'High Network Rating', 'Low Network Rating', 'Connoisseur Rating',
                   'Food Aestheticist Rating', 'Patrons Rating', 'First Visit',
                   'Visual Importance', 'Female Importance', 'Foreign Importance',
                   'Connectedness', 'Average Rating']] = df_own.loc[:, ['Male to Female', 'Foreign to Local',
                                                                        'Male Rating', 'Female Rating', 'Local',
                                                                        'Foreign',
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

    temp = df_own[["Total Network", "Number of Reviewers", "county_state"]]

    df_1 = df_own.drop(["Total Network", "Number of Reviewers"], axis=1)
    all_firms_mean_count = df_1.groupby("county_state").mean().reset_index()
    all_firms_sum_count = temp.groupby("county_state").sum().reset_index()

    all_firms_count = pd.concat((all_firms_mean_count, all_firms_sum_count), axis=1)

    all_firms_count.drop(["Unnamed: 0", "Unnamed: 0.1"], axis=1, inplace=True)
    all_firms_count = all_firms_count.iloc[:, 1:]

    cols = list(all_firms_count.columns)
    cols.remove("county_state")
    temp_reconst = df_own.drop(cols, axis=1)
    temp_reconst = temp_reconst.drop_duplicates(["county_state"]).reset_index(drop=True)

    # df_county = df

    all_firms_count_2 = pd.merge(all_firms_count, temp_reconst, on="county_state", how="left")

    all_firms_count_2.drop(["Unnamed: 0"], axis=1, inplace=True)

    # all_firms_count['county'].apply(lambda x: x.split(" ")[0] if x.split(" ")==2 else x )

    df2 = pd.read_csv('https://data.cdc.gov/api/views/pbkm-d27e/rows.csv?accessType=DOWNLOAD')

    df2 = df2.drop_duplicates("County").reset_index(drop=True)

    # all_firms_count_2.drop(["Unnamed: 0"],axis=1, inplace = True)

    # https://plot.ly/~jackp/18292.embed
    import geopandas as gp

    df_geo = gp.read_file("../data/county/cb_2016_us_county_500k.shp")

    all_f_second = pd.merge(all_firms_count_2, df2, left_on="county_state", right_on="County", left_index=True,
                            how="left")

    all_f_second = all_f_second.reset_index(drop=True)

    df_geo['FIPS'] = df_geo['STATEFP'] + df_geo['COUNTYFP']
    df_geo['FIPS'] = df_geo['FIPS'].astype(float)
    all_f_third = pd.merge(all_f_second, df_geo, on="FIPS", how="left").reset_index(drop=True)
    all_dicts_county[i] = all_f_third

# df.to_csv("bla.csv")

import plotly.plotly as py
import pandas as pd
import numpy as np

# rd = pd.read_csv('https://raw.githubusercontent.com/plotly/datasets/master/2011_us_ag_exports.csv')

my_path = os.path.abspath(os.path.dirname('__file__'))
path_in_file = os.path.join(my_path, "../data/google/addresses_google.csv")
df_own = pd.read_csv(path_in_file)

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

temp = df_own[["Total Network", "Number of Reviewers", "county_state"]]

df_1 = df_own.drop(["Total Network", "Number of Reviewers"], axis=1)
all_firms_mean_count = df_1.groupby("county_state").mean().reset_index()
all_firms_sum_count = temp.groupby("county_state").sum().reset_index()

all_firms_count = pd.concat((all_firms_mean_count, all_firms_sum_count), axis=1)

all_firms_count.drop(["Unnamed: 0", "Unnamed: 0.1"], axis=1, inplace=True)
all_firms_count = all_firms_count.iloc[:, 1:]

cols = list(all_firms_count.columns)
cols.remove("county_state")
temp_reconst = df_own.drop(cols, axis=1)
temp_reconst = temp_reconst.drop_duplicates(["county_state"]).reset_index(drop=True)

# df_county = df

all_firms_count_2 = pd.merge(all_firms_count, temp_reconst, on="county_state", how="left")

all_firms_count_2.drop(["Unnamed: 0"], axis=1, inplace=True)

# all_firms_count['county'].apply(lambda x: x.split(" ")[0] if x.split(" ")==2 else x )

df2 = pd.read_csv('https://data.cdc.gov/api/views/pbkm-d27e/rows.csv?accessType=DOWNLOAD')

df2 = df2.drop_duplicates("County").reset_index(drop=True)

# all_firms_count_2.drop(["Unnamed: 0"],axis=1, inplace = True)

# https://plot.ly/~jackp/18292.embed
import geopandas as gp

df_geo = gp.read_file("../data/county/cb_2016_us_county_500k.shp")

all_f_second = pd.merge(all_firms_count_2, df2, left_on="county_state", right_on="County", left_index=True, how="left")

all_f_second = all_f_second.reset_index(drop=True)

df_geo['FIPS'] = df_geo['STATEFP'] + df_geo['COUNTYFP']
df_geo['FIPS'] = df_geo['FIPS'].astype(float)
all_f_third = pd.merge(all_f_second, df_geo, on="FIPS", how="left").reset_index(drop=True)

all_dicts_county["All"] = all_f_third

import _pickle as pickle

pickle.dump(all_dicts_county, open(path_in_ngrams + "all_dicts_county.p", "wb"))

# pickle.dump(rat, open(path_in_ngrams+ "map_dict.p", "wb"))