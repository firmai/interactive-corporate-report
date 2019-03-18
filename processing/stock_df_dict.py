from __future__ import print_function
import pandas as pd
import dash
from dash import Dash
from dash.dependencies import Input, Output
import dash_core_components as dcc
import dash_html_components as html
import colorlover as cl
import numpy as np
from flask import Flask
import intrinio
from six.moves import cPickle as pickle  # for performance
import numpy as n
pd.set_option('display.max_columns', None)

pd.set_option('display.max_columns', None)

from sklearn.preprocessing import MinMaxScaler
from sklearn.preprocessing import StandardScaler


def Standardisation(df):
    listed = list(df)
    scaler = StandardScaler()
    scaled = scaler.fit_transform(df)
    df = pd.DataFrame(scaled)
    df.columns = listed
    return df


def Normalisation(df):
    listed = list(df)
    index = df.index
    scaler = MinMaxScaler()
    scaled = scaler.fit_transform(df)
    df = pd.DataFrame(scaled)
    df.columns = listed
    df.index = index
    return df

import os

dict_frames = {}

my_path = os.path.abspath(os.path.dirname(__file__))
path = os.path.join(my_path, "../input_fields.csv")


input_fields = pd.read_csv(path)

ticks  = [x for x in input_fields[input_fields["ticker"]!="PE"].ticker]
codes = input_fields["code_or_ticker"]

import intrinio

intrinio.client.username = 'xxxxxx'
intrinio.client.password = 'xxxxxx'


def correlation(boola, vals, select, normalised):
    if boola:
        norms = normalised.corr()["adj_close"].sort_values()[:15].index.values;
        norms
    else:
        norms = normalised.corr()["adj_close"].sort_values()[-15:].index.values;
        norms

    dis = {}
    for i in norms:
        das = normalised[norms].corr()[i]
        dis[i] = das.sum()

    corr = pd.DataFrame(list(dis.values()), index=list(dis.keys())).sort_values(0).ix[:8].index.values

    return corr

import os

#     related = pd.DataFrame(list(dis.values()), index=list(dis.keys())).sort_values(0).ix[:select].index.values
#     related = normalised[related]
#     return related

my_path = os.path.abspath(os.path.dirname(__file__))
path = os.path.join(my_path, "../data/financial/")

def pca_transform(normalised, code):
    if code == "calculations":
        calc_pca = pd.read_csv(path+ "calc_pca.csv")  # calc_pca wass created by hand labelling
    elif code == "balance_sheet":
        calc_pca = pd.read_csv(path+"ass_pca.csv")
    elif code == "income_statement":
        calc_pca = pd.read_csv(path+"inc_pca.csv")  # calc_pca wass created by hand labelling
    elif code == "cash_flow":
        calc_pca = pd.read_csv(path+"cfs_pca.csv")

    calc_pca = calc_pca.dropna().reset_index(drop=True)
    print(calc_pca.columns)
    print(calc_pca.values)
    print(normalised.columns)

    fair_values = list(set(calc_pca["Type"].unique()).intersection(normalised.columns))

    normalised = normalised[fair_values]

    calc_pca = calc_pca[calc_pca["Type"].isin(fair_values)].reset_index()

    print(calc_pca["Dimension"].unique())
    pca_df = pd.DataFrame()
    for i in calc_pca["Dimension"].unique():
        normalised_profit = normalised[calc_pca[calc_pca["Dimension"] == i]["Type"].values]

        import numpy as np
        from sklearn.decomposition import PCA

        pca = PCA(n_components=1)
        pca.fit(normalised_profit)
        X = pca.transform(normalised_profit)
        X = list(X.reshape(-1))
        pca_df[i] = list(X)

    return pca_df


def corrsa(boola, select, diff_frame):

    diff_frame = diff_frame.drop_duplicates()


    if boola:

        norms = diff_frame.sum().sort_values(ascending=False)[:15].index.unique()
    else:
        norms = diff_frame.sum().sort_values(ascending=False)[-15:].index.unique()

    dis = {}
    for i in norms:
        das = diff_frame[norms].corr()[i]
        dis[i] = das.sum()

    related = pd.DataFrame(list(dis.values()), index=list(dis.keys()))
    print(related)
    related = related.sort_values(0)[:select].index.values
    return related

def corr_first(boola, select, normalised):
    select =8
    c = normalised.corr()

    s = c.unstack()
    so = s.sort_values()

    diff_frame = pd.DataFrame(so).drop_duplicates().sort_values(0,ascending=False)

    if boola:

        diff_frame = normalised[list(diff_frame[:15].index.get_level_values(0).unique())]

        diff_frame = Normalisation(diff_frame)

        norms = diff_frame.sum().sort_values(ascending=False)[:15].index.values
    else:

        diff_frame = normalised[list(diff_frame[-15:].index.get_level_values(0).unique())]

        diff_frame = Normalisation(diff_frame)

        norms = diff_frame.sum().sort_values(ascending=False)[-15:].index.values

    dis  = {}
    for i in norms:
        das = diff_frame[norms].corr()[i]
        dis[i] = das.sum()

    related = pd.DataFrame(list(dis.values()), index=list(dis.keys()))
    related = related.sort_values(0)[:select].index.values
    return related

# Bench comp here has a null df, and it has to be wixed
def bench_comp(bj_qtr, cmg_qtr, code):

    dwad = {"calculations": 1.5, "income_statement": 1, "cash_flow": 1, "balance_sheet": 1}

    rwad = dwad[code]

    name = np.where(bj_qtr.ix[:, 1:].sum().values > rwad, bj_qtr.ix[:, 1:].sum().index, np.nan)

    framed = pd.DataFrame(name)

    framed = framed.dropna().reset_index(drop=True)

    name = np.where(cmg_qtr.ix[:, 1:].sum().values > rwad, cmg_qtr.ix[:, 1:].sum().index, np.nan)

    framed_comp = pd.DataFrame(name)

    framed_comp = framed_comp.dropna().reset_index(drop=True)

    full = list(set(framed_comp[0]).intersection(framed[0]))

    diff_frame = pd.DataFrame()
    for i in full:
        diff_frame[i] = bj_qtr[i] - cmg_qtr[i]

    positive = corrsa(True, 8, diff_frame)
    negative = corrsa(False, 8, diff_frame)
    return positive, negative, full


def volat(boola, select, frame, vola):
    if boola:

        norms = vola.std().sort_values(ascending=False).ix[:15].index.values
    else:
        norms = vola.std().sort_values(ascending=False).ix[-15:].index.values

    dis = {}
    for i in norms:
        das = frame[norms].corr()[i]
        dis[i] = das.sum()

    related = pd.DataFrame(list(dis.values()), index=list(dis.keys())).sort_values(0).ix[:select].index.values
    return related


def smoothed(bj_qtr):
    smooth = pd.rolling_mean(bj_qtr.ix[:, 1:], window=8)

    smooth_rev = pd.rolling_mean(bj_qtr.iloc[::-1].ix[:, 1:].reset_index(drop=True), window=8)

    smooth_rev.head()

    smooth.ix[:6] = smooth_rev[-7:][::-1].reset_index(drop=True)
    return smooth


req = ["calculations", "income_statement", "cash_flow","balance_sheet"]
for ticker, cod in zip(ticks,codes):
    for request in req:

        original = pd.read_csv(path + "org_" + request + "_" + ticker + ".csv")
        normalised = pd.read_csv(path + "sta_" +  request + "_" + ticker + ".csv")

        corr_ft = correlation(True, 15, 8, normalised)
        uncorr_ft = correlation(False, -15, 8, normalised)
        pca_df = pca_transform(normalised, request)
        for i in ticks:
            if i not in ticker:
                bench = pd.read_csv(path + "sta_" + request + "_" + i + ".csv")
                benched_pos_ft, benched_neg_ft, full = bench_comp(normalised, bench, request)
        vola_df = normalised[full]
        volatile_ft = volat(True, 8, normalised, vola_df)
        stable_ft = volat(False, 8, normalised, vola_df)
        smooth_df = smoothed(normalised)
        uncor_pair = corr_first(False, 8, normalised)
        cor_pair = corr_first(True, 8, normalised)


        corr_ft = normalised[corr_ft.tolist() + ["year"]]
        stable_ft = normalised[stable_ft.tolist() + ["year"]]
        cor_pair = normalised[cor_pair.tolist() + ["year"]]
        uncor_pair = normalised[uncor_pair.tolist() + ["year"]]
        volatile_ft = normalised[volatile_ft.tolist() + ["year"]]
        benched_pos_ft = normalised[benched_pos_ft.tolist() + ["year"]]
        benched_neg_ft = normalised[benched_neg_ft.tolist() + ["year"]]
        uncorr_ft = normalised[uncorr_ft.tolist() + ["year"]]


        dict_frames[cod, request, "Original"] = original
        dict_frames[cod, request, "Normalised"] = normalised
        dict_frames[cod, request, "Correlated Fundamentals"] = corr_ft
        dict_frames[cod, request, "Neg Correlated Pairs"] = uncorr_ft
        dict_frames[cod, request, "Principal Component"] = pd.concat((pca_df, normalised["year"]),axis=1)
        dict_frames[cod, request, "Benchmark"] = bench
        dict_frames[cod, request, "Better Than Bench"] = benched_pos_ft
        dict_frames[cod, request, "Worse Than Bench"] = benched_neg_ft
        dict_frames[cod, request, "Volatile"] = volatile_ft
        dict_frames[cod, request, "Stable"] = stable_ft
        dict_frames[cod, request, "Smooth"] =  pd.concat((smooth_df, normalised["year"]),axis=1)
        dict_frames[cod, request,"Price Correlated"] = cor_pair
        dict_frames[cod, request,"Price Neg Correlated"] = uncor_pair


def save_dict(di_, filename_):
    with open(filename_, 'wb') as f:
        pickle.dump(di_, f)


def load_dict(filename_):
    with open(filename_, 'rb') as f:
        ret_di = pickle.load(f)
    return ret_di

save_dict(dict_frames, path+'data.pkl')
dict_frames = load_dict(path+'data.pkl')