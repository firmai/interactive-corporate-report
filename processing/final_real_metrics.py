## After Final Real Metrics you also have to run app_processing.py

#### Additional Metrics Have Been Combined Here

import pandas as pd
import os
import _pickle as pickle

my_path = os.path.abspath(os.path.dirname('__file__'))
path = os.path.join(my_path, "../data/closure/")

my_path = os.path.abspath(os.path.dirname('__file__'))
path_in_sent = os.path.join(my_path, "../data/yelp_sentiment/")

dat = pickle.load(open(path_in_sent + "yelp_sent.p", "rb"))
ke = []

i = -1

for aes, dars in dat.items():
    i = i + 1
    ke.append(aes)
    if i == 0:
        va = pd.DataFrame(index=dars.index)
    va = pd.concat((va, dars), axis=1)

ba = va[va.index.str.contains("-TQ")].T.sum()

ba.index = [s[:-4] for s in list(ba.index)]

ba = ba / len(va.columns) * 100

here = pd.DataFrame(ba)
here.columns = ["Overall Sentiment"]

ba

## Who some crazy things:

import dash_core_components as dcc
import dash_html_components as html
import os
import pandas as pd
import _pickle as pickle

my_path = os.path.abspath(os.path.dirname('__file__'))
path_out = my_path + "/../data/doordash/"
mat = pickle.load(open(path_out + "dict_doordash.p", "rb"))
fally = "Most Loved"
vat = mat[fally]

ranks = vat.iloc[10, :].to_frame()

ranks = ranks[ranks.index.str.contains("products")]

ranks.index = [s.split("_")[1] for s in ranks.index]

ranks[10] = [s.split("/")[0] for s in ranks[10]]

ranks.columns = ["Food Rating"]

price = mat["category"][mat["category"]["Category"] == "mean"]

price = price.iloc[:, 1:].T

price.columns = ["Price"]

ranks = pd.merge(ranks, price, left_index=True, right_index=True, how="left")

ranks = pd.merge(ranks, here, left_index=True, right_index=True, how="left")

ranks = ranks.astype(float)

ranks["Quality/Price"] = ranks["Food Rating"] / ranks["Price"]

ranks

target_code = "BJRI"
option_value_bench_code_dd = "CAKE"
my_path = os.path.abspath(os.path.dirname('__file__'))

path_out = os.path.join(my_path, "../data/yelp_extra_info/")
path_in_ngrams = os.path.join(my_path, "../data/cpickle/")

final_df = pd.read_csv(path_out + "extra_info.csv")

final_df = final_df.set_index("Unnamed: 0")

i_dict = pickle.load(open(path_in_ngrams + "i_dict.p", "rb"))

path = os.path.join(my_path, "../input_fields.csv")

input_fields = pd.read_csv(path)

code_rest = list(input_fields["code_or_ticker"])

code_rest.remove(target_code)
code_rest.remove(option_value_bench_code_dd)

frame_g = pd.DataFrame.from_dict(i_dict[target_code], orient="index")
frame_g = pd.DataFrame(index=frame_g.index)

small_cols = []
file_names = [s[:-4] for s in frame_g.columns]
for col in frame_g.columns:
    wa = ""
    for r in col.split("-"):
        if r[0].isdigit():
            wa = wa + r[:-4]
        else:
            wa = wa + r[0]
    small_cols.append(wa)

frame_g.columns = small_cols

frame_agg = pd.DataFrame.from_dict(i_dict[target_code], orient="index")
frame_agg = pd.DataFrame(index=frame_agg.index)

for r in [target_code, option_value_bench_code_dd]:
    dfg = pd.DataFrame.from_dict(i_dict[r], orient="index")
    dfg.columns = [r]
    frame_agg = frame_agg.join(dfg, how="outer")

for r in code_rest:
    dfg = pd.DataFrame.from_dict(i_dict[r], orient="index")
    dfg.columns = [r]
    frame_agg = frame_agg.join(dfg, how="outer")

frame_agg = frame_agg.rename(index={'Average Hours': 'Average Weekly Hours'})

frame_g = frame_g.rename(index={'Hours Open': 'Average Weekly Hours'})

new_ff = frame_agg.join(frame_g, how="outer")

new_ff = new_ff.round(2)

new_ff = new_ff.reset_index()

new_ff = new_ff.rename(columns={"index": "Category"})

new_ff.loc[-1] = new_ff.columns
new_ff.index = new_ff.index + 1
new_ff = new_ff.sort_index()

def make_dash_table(df):
    ''' Return a dash definitio of an HTML table for a Pandas dataframe '''
    table = []
    for index, row in df.iterrows():
        html_row = []
        for i in range(len(row)):
            html_row.append(html.Td([row[i]],style={"title":"Week"}))
        table.append(html.Tr(html_row,style={"title":"Week"}))
    return table

modifed_perf_table = make_dash_table(new_ff)

modifed_perf_table.insert(
    0, html.Tr([
        html.Td([]),
        html.Td(['National (%)'], colSpan=8, style={'text-align': "center"}),
        html.Td(['Local'], colSpan=7, style={'text-align': "center"})
    ], style={'background': 'white', 'font-weight': '600'}
    )
)

d = {}
d["table"] = modifed_perf_table

f_df = pd.read_csv("../big_small_add.csv")
f_df = f_df.reset_index(drop=True)

f_df = list(f_df[f_df["All Target Location File Names"].isin(file_names)].reset_index(drop=True)[
                "All Target Location Full Addresses"])

code_sap = list(input_fields["code_or_ticker"])

rw = ""
for t, c, w in zip(small_cols, code_sap, f_df):
    rw = rw + t.upper() + '/' + c + ':      ' + w + "     "

d["adds"] = rw

code = input_fields["code_or_ticker"]

my_path = os.path.abspath(os.path.dirname('__file__'))

path = os.path.join(my_path, "../data/cpickle/")

rates_df = pd.DataFrame()
for coy in code:
    rad = pd.DataFrame()
    path_in = os.path.join(my_path, "../data/ratings/")
    yelp = pd.read_csv(path_in + "all_yelps_rates_" + coy + ".csv")
    better = [d.title() for d in yelp.columns]
    yelp.columns = better
    das = yelp.iloc[-1:, :].T[1:]
    wel = das.reset_index()
    wel["Target"] = coy

    rates_df = rates_df.append(wel)

rates_df.iloc[:, 1] = rates_df.iloc[:, 1].fillna(rates_df.iloc[:, 1].mean() - .2)

final_df = pd.read_csv(path_out + "extra_info.csv")
final_df = final_df.set_index("Unnamed: 0")
final_tact = final_df.copy()

final_tact = final_tact[final_tact["Hours Open"] > 10]

for s in ['Free Wi-Fi', 'Takes Reservations',
          'Outdoor Seating', 'Delivery', 'Caters', 'Bike Parking',
          'Accepts Apple Pay', 'Accepts Android Pay']:
    final_tact[s + " - S"] = final_tact[s].apply(lambda x: 1 if x == "Yes" else 0)

final_tact["Noisy" + " - S"] = final_tact["Noisy"].apply(lambda x: 1 if x == "No" else 0)

ads = final_tact[['Free Wi-Fi - S',
                  'Takes Reservations - S', 'Outdoor Seating - S', 'Delivery - S',
                  'Caters - S', 'Bike Parking - S', 'Accepts Apple Pay - S',
                  'Accepts Android Pay - S', 'Noisy - S']]

fap = ads.sum(axis=1) + (final_tact["Hours Open"] * 2) / 100

fap = fap / (fap.sort_values()[-1]) * 10

f_df = pd.read_csv("../big_small_add.csv")

dap = pd.merge(f_df, rates_df, left_on=["All Target Location Small Names", "Target"], right_on=["index", "Target"],
               how="left")

dap["rating"] = dap.iloc[:, -1]

dap = dap.set_index(dap["All Target Location File Names"], drop=True)

fap.index = [r[:-4] for r in fap.index]

fap = pd.DataFrame(fap)

dap = dap[["rating", "Target", "All Target Location Small Names", "All Target Location Full Addresses"]].copy()
fin = fap.join(dap, how="outer")

fin = fin.fillna(fin.mean() - .15)

fin["final"] = fin[0] * 0.45 + fin["rating"] * 0.55 * 2

group_fin = fin.copy()

grouped = group_fin.groupby("Target").mean()

grouped.reset_index(inplace=True)

grouped.Target = grouped.Target.astype("category")

grouped.Target.cat.set_categories(list(frame_agg.columns), inplace=True)

import plotly.plotly as py
import plotly.graph_objs as go

grouped = grouped.sort_values(["Target"])

grouped = grouped[["final", "Target"]].set_index("Target")

ranks = pd.merge(ranks, grouped, left_index=True, right_index=True, how="left")

my_path = os.path.abspath(os.path.dirname('__file__'))
path = os.path.join(my_path, "../input_fields.csv")

input_fields = pd.read_csv(path)

short = input_fields["short_name"]
codes = input_fields["code_or_ticker"]

my_path = os.path.abspath(os.path.dirname('__file__'))
path_out = my_path + "/../data/similarweb/"
fi_dict = pickle.load(open(path_out + "website.p", "rb"))

fi_dict = fi_dict["key_metrics"][["Firm", "Category Rank"]].iloc[1:, :].set_index("Firm")

ranks = pd.merge(ranks, fi_dict, left_index=True, right_index=True, how="left")

my_path = os.path.abspath(os.path.dirname('__file__'))

# coll = pd.read_csv(my_path + "/full_synth/" + c + "_full.csv")

pricing = pd.read_csv(my_path + "/../data/closure/pricing_data.csv")

pricing["MV"] = pricing["PRC"] * pricing["SHROUT"]

codes

pricing = pricing[pricing["TICKER"].isin(codes)]

pricing = pricing.drop_duplicates("TICKER", keep="last")[["TICKER", "MV"]]

pricing = pricing.dropna()

""""
pricing

pricing = pricing[pricing["TICKER"].isin([c])].reset_index(drop=True)

"""

my_path = os.path.abspath(os.path.dirname('__file__'))
path = os.path.join(my_path, "../data/cpickle/")
art_ratios = pickle.load(open(path + "art_ratios.p", "rb"))

ra = -1
for i in art_ratios["mv"].keys():
    ra = ra + 1
    if ra == 0:
        pad = art_ratios["mv"][i]
        pad["ticker"] = i
    else:
        here = art_ratios["mv"][i]
        here["ticker"] = i
        pad = pd.concat((pad, here), axis=0)

pad = pad.drop_duplicates("ticker", keep="last")[["ticker", "MV_pred"]]

pad = pad[~pad["ticker"].isin(pricing["TICKER"].values)]

pad.columns = ["TICKER", "MV"]

pad = pd.concat((pad, pricing), axis=0)

ranks = pd.merge(ranks, pad.set_index("TICKER"), left_index=True, right_index=True, how="left")

#### Here I am making some manual ammendments
#################################################################################

ranks["MV"]["CPKI"] = ranks["MV"]["CPKI"] / 6

################################################################################

ranks["MV Norm"] = 1 / (ranks["MV"] / ranks["MV"].max())

ranks["Internet Presence"] = (1 / (ranks["Category Rank"] / ranks["MV Norm"])) * 100

posts_num = []
num_reactions = []
num_comments = []
num_shares = []

c = "BJRI"
for c in codes:
    fb = pd.read_csv("../data/facebook/" + c + "_facebook.csv")

    fb["status_published"] = pd.to_datetime(fb["status_published"], infer_datetime_format=True)

    from datetime import timedelta

    fb = fb[fb["status_published"] > (fb["status_published"].max() - timedelta(120))]

    fb_sum = fb.sum()
    posts_num.append(len(fb))
    num_reactions.append(fb_sum["num_reactions"])
    num_comments.append(fb_sum["num_comments"])
    num_shares.append(fb_sum["num_shares"])

fb_df = pd.DataFrame()
fb_df["ticker"] = codes
fb_df["posts_num"] = posts_num
fb_df["num_reactions"] = num_reactions
fb_df["num_comments"] = num_comments
fb_df["num_shares"] = num_shares

fb_df["Post Quality"] = (fb_df["num_comments"] + fb_df["num_shares"]) / fb_df["num_reactions"]

ranks = pd.merge(ranks, fb_df.set_index("ticker"), left_index=True, right_index=True, how="left")

ranks["Social Media Reach"] = (ranks["num_comments"] + ranks["num_shares"] + ranks["num_reactions"]) * ranks["MV Norm"]

ranks["Quality Reach"] = ranks["Social Media Reach"] * ranks["Post Quality"]

ga = va[va.index.str.contains("-TQ")]

ga.index = [s[:-4] for s in list(ga.index)]

ga["Experience Sentiment"] = ga[['area', 'atmosphere',
                                 'birthday', 'experience', 'family', 'friends', 'kids', 'location',
                                 'night', 'outside', 'parking', 'place', 'restaurant', 'visit']].mean(axis=1)

ga["Process Sentiment"] = ga[['kitchen', 'lunch', 'meal',
                              'menu', 'order', 'plates', 'portion', 'water']].mean(axis=1)

ga["Service Sentiment"] = ga[['bill', 'check', 'hostess', 'management', 'manager', 'price', 'servers',
                              'service', 'staff', 'time', 'waiter', 'waiting', 'waitress']].mean(axis=1)

ga["Food Sentiment"] = ga[['bread',
                           'burger', 'cheese', 'chicken', 'dessert', 'fries', 'pasta', 'pizza',
                           'salad', 'sandwich', 'sauce', 'steak', 'appetizer', 'bar', 'beer',
                           'dinner', 'dish', 'drink', 'drinks', 'food']].mean(axis=1)

ranks = pd.merge(ga[["Service Sentiment", "Food Sentiment", "Experience Sentiment", "Process Sentiment"]], ranks,
                 left_index=True, right_index=True, how="left")

## Preferrably Just Run this one.

import pandas as pd
import os
import numpy as np

my_path = os.path.abspath(os.path.dirname('__file__'))
path = os.path.join(my_path, "../data/closure/")

bulla_Run = pd.read_csv(path + "bulla_Run1.csv")

bulla_Run = bulla_Run.drop(bulla_Run.filter(regex='std'), axis=1)

# bulla_Run = bulla_Run.filter(regex="chain|date|ticker")

bulla_Run = bulla_Run[["ticker", "diffs_sum_chain_avg", "diffs_mean_chain_avg", "review_count_usr_mean_chain_avg",
                       "review_count_usr_max_chain_avg",
                       "Bike Parking_chain_avg", "Takes Reservations_chain_avg", "Caters_chain_avg",
                       "Delivery_chain_avg", "Connoisseur_chain_avg", "Food Aestheticist_chain_avg",
                       "first_sent_mean_chain_avg", "last_sent_mean_chain_avg", "senti_polarity_mean_chain_avg",
                       "friend_count_mean_chain_avg", "Average Customer Network_chain_avg"
                       ]]

bulla_Run = bulla_Run.drop_duplicates("ticker")

from sklearn.preprocessing import MinMaxScaler

scaler = MinMaxScaler(feature_range=(2.8, 4.1))
# scaler.fit(art_ratios["Extend"].values.reshape(-1, 1))
scaler.fit(bulla_Run.drop(["Connoisseur_chain_avg", "ticker", "Food Aestheticist_chain_avg"], axis=1))

transed = scaler.transform(bulla_Run.drop(["Connoisseur_chain_avg", "ticker", "Food Aestheticist_chain_avg"], axis=1))

transed = pd.DataFrame(transed,
                       columns=bulla_Run.drop(["Connoisseur_chain_avg", "ticker", "Food Aestheticist_chain_avg"],
                                              axis=1).columns)

transed

transed = transed.applymap(lambda x: x + np.random.normal(0.02, 0.04))

transed["ticker"] = bulla_Run["ticker"].values

transed["Connoisseur_chain_avg"] = bulla_Run["Connoisseur_chain_avg"].values
transed["Food Aestheticist_chain_avg"] = bulla_Run["Food Aestheticist_chain_avg"].values

transed.head(10)

mv_ai = pd.read_csv(path + "collected_frame_ai_mv.csv")

mv_ai["Employee Retention"] = mv_ai["employee_count_bfill"] / mv_ai["employee_left_bfill"]
mv_ai["Employee Growth"] = mv_ai["employee_add_bfill"] / mv_ai["employee_count_bfill"]

mv_ai["Employee Retention_f"] = mv_ai["employee_count_ffill"] / mv_ai["employee_left_ffill"]
mv_ai["Employee Growth_f"] = mv_ai["employee_add_ffill"] / mv_ai["employee_count_ffill"]

mv_ai["date"] = pd.to_datetime(mv_ai["date"], infer_datetime_format=True)

from datetime import timedelta

new_mv_ai = mv_ai[mv_ai["date"] > mv_ai["date"].max() - timedelta(int(365 * 0.25))]

new_mv_ai = new_mv_ai.groupby("ticker").mean()

new_mv_ai = new_mv_ai.replace(np.inf, np.nan)

new_mv_ai = new_mv_ai.fillna(new_mv_ai.mean())

# Search and Direct is probably indicative of very strong branding.
colly = [
    "Bounce Rate",
    "Search",
    "Direct",
    "Visual Importance_max",

    "perc_acc_ffill",
    "perc_acc_bfill",

    "Employee Retention", "Employee Growth",
    "Employee Retention_f", "Employee Growth_f",

    "Caters_convenience_pca",
    "customer_rating_pca",
    "Total Network_avg",
    "Average Customer Network_avg",
    "Number of Reviewers_avg",
    "Final_Rating_bfill",
    "Final_Rating_ffill",
    "Foreign_avg",
    "Food Aestheticist_avg",

    "Final_Career Opportunities_bfill", "Final_Senior Management_bfill", "Final_Senior Management_ffill",
    "Final_Culture Values_bfill", "Final_Culture Values_ffill"
    , "Final_Rating M", "Final_Culture Values M", "Final_Comp Benefits M", "Final_Senior Management M"]

new_mv_ai = new_mv_ai[colly]

transy = new_mv_ai.loc[:, :"Number of Reviewers_avg"]

scaler = MinMaxScaler(feature_range=(2.8, 4.1))
# scaler.fit(art_ratios["Extend"].values.reshape(-1, 1))
scaler.fit(transy)

# transed=scaler.transform(art_ratios["Extend"].values.reshape(-1, 1))
transyc = scaler.transform(transy)

transyc = pd.DataFrame(transyc, columns=transy.columns)

transyc = transyc.applymap(lambda x: x + np.random.normal(0.02, 0.04))

new_mv_full = pd.concat((new_mv_ai.loc[:, "Final_Rating_bfill":].reset_index(), transyc), axis=1)

# new_mv_full["mean"] = new_mv_full.iloc[:,1:].mean(axis=1)

# del new_mv_full["mean"]

ranks = pd.read_csv("../data/closure/ranks_metrics.csv")

ranks = ranks.drop(["posts_num", "num_reactions", "num_comments", "num_shares", "MV", "MV Norm"], axis=1)

from sklearn.preprocessing import MinMaxScaler

scaler = MinMaxScaler(feature_range=(3.3, 4.6))
# scaler.fit(art_ratios["Extend"].values.reshape(-1, 1))

ranks.head()

caty = pd.concat((ranks.loc[:, "Service Sentiment":"Process Sentiment"], ranks.loc[:, "Price":]), axis=1)

scaler.fit(caty)
# transed=scaler.transform(art_ratios["Extend"].values.reshape(-1, 1))

transr = scaler.transform(caty)

transr = pd.DataFrame(transr, columns=caty.columns)

transr = transr.applymap(lambda x: x + np.random.normal(0.02, 0.04))

transr["ticker"] = ranks["Unnamed: 0"].values

transr = pd.merge(ranks[["Unnamed: 0", "Food Rating"]].set_index("Unnamed: 0"), transr.set_index("ticker"),
                  left_index=True, right_index=True, how="left")

transr = pd.merge(transr, transed.set_index("ticker"), left_index=True, right_index=True, how="left")

transr["mean"] = transr.mean(axis=1)

transr["Foodie Index"] = (transr["review_count_usr_mean_chain_avg"] + transr["review_count_usr_max_chain_avg"]) / 2

transr["Network Size"] = (transr["Average Customer Network_chain_avg"] + transr["friend_count_mean_chain_avg"]) / 2

transr = transr.drop(
    ["diffs_sum_chain_avg", "Category Rank", "review_count_usr_mean_chain_avg", "review_count_usr_max_chain_avg",
     "Average Customer Network_chain_avg", "mean", "friend_count_mean_chain_avg"], axis=1)

transr.head()

transr.columns = ["Food Quality", "Service Sentiment", "Food Sentiment", "Experience Sentiment", "Process Sentiment",
                  "Price Index", "Restaurant Sentiment", "Good Value", "Convenience", "Website Popularity",
                  "Advertising Quality", "Social Media Reach", "Quality Reach", "Visit Frequency", "Parking",
                  "Reservation", "Catering", "Delivery", "Early Sentiment", "Late Sentiment", "Overall Sentiment",
                  "Connoisseur Rating", "Aesthetician Rating", "Foodie Index", "Network Size"]

distrib = transr.copy()

distrib.loc[:, "Price Index":"Delivery"] = distrib.loc[:, "Service Sentiment":"Delivery"].applymap(
    lambda x: x + np.log(3.9 / x) + 1 - 1 + np.sqrt(3.9 / x) - 1)

distrib.loc[:, "Early Sentiment":"Overall Sentiment"] = distrib.loc[:, "Early Sentiment":"Overall Sentiment"].applymap(
    lambda x: x + np.log(3.9 / x) + 1 - 1 + np.sqrt(3.9 / x) - 1)

distrib.loc[:, "Foodie Index":"Network Size"] = distrib.loc[:, "Foodie Index":"Network Size"].applymap(
    lambda x: x + np.log(3.9 / x) + 1 - 1 + np.sqrt(3.9 / x) - 1)

new_mv_full = new_mv_full.drop(
    ["Final_Rating_bfill", "Final_Rating_ffill", "Foreign_avg", "Food Aestheticist_avg", "Caters_convenience_pca",
     "customer_rating_pca", "Total Network_avg", "Average Customer Network_avg", "Number of Reviewers_avg"], axis=1)

new_full = pd.DataFrame()

new_full["Employee Opportunities"] = new_mv_full["Final_Career Opportunities_bfill"]
new_full["Management Proficiency"] = (new_mv_full["Final_Senior Management_bfill"] + new_mv_full[
    "Final_Senior Management_bfill"]) / 2
new_full["Company Culture"] = (
                              new_mv_full["Final_Culture Values_bfill"] + new_mv_full["Final_Culture Values_bfill"]) / 2
new_full["Management Happiness"] = new_mv_full["Final_Rating M"]
new_full["Management Culture"] = new_mv_full["Final_Culture Values M"]
new_full["Management Comp."] = new_mv_full["Final_Comp Benefits M"]
new_full["Search Traffic"] = new_mv_full["Search"]
new_full["Direct Traffic"] = new_mv_full["Direct"]
new_full["Visual Importance"] = new_mv_full["Visual Importance_max"]

new_full["Offers Accepted"] = (new_mv_full["perc_acc_ffill"] + new_mv_full["perc_acc_bfill"]) / 2
new_full["Employee Retention"] = (new_mv_full["Employee Retention"] + new_mv_full["Employee Retention_f"]) / 2
new_full["Employee Growth"] = (new_mv_full["Employee Growth"] + new_mv_full["Employee Growth_f"]) / 2

new_full["ticker"] = new_mv_full["ticker"]
absolute_df = pd.merge(transr, new_full.set_index("ticker"), left_index=True, right_index=True, how="left")

absolute_df = absolute_df.round(2)

mv_ai = pd.read_csv(path + "collected_frame_ai_mv.csv")

mv_ai["Employee Retention"] = mv_ai["employee_count_bfill"] / mv_ai["employee_left_bfill"]
mv_ai["Employee Growth"] = mv_ai["employee_add_bfill"] / mv_ai["employee_count_bfill"]

mv_ai["Employee Retention_f"] = mv_ai["employee_count_ffill"] / mv_ai["employee_left_ffill"]
mv_ai["Employee Growth_f"] = mv_ai["employee_add_ffill"] / mv_ai["employee_count_ffill"]

mv_ai["date"] = pd.to_datetime(mv_ai["date"], infer_datetime_format=True)

series_frame = pd.DataFrame()

series_frame["Search Traffic"] = mv_ai["Search"]
series_frame["Direct Traffic"] = mv_ai["Direct"]
series_frame["Visual Importance"] = mv_ai["Visual Importance_max"]

series_frame["Offers Accepted"] = (mv_ai["perc_acc_ffill"] + mv_ai["perc_acc_bfill"]) / 2
series_frame["Employee Retention"] = (mv_ai["Employee Retention"] + mv_ai["Employee Retention_f"]) / 2
series_frame["Employee Growth"] = (mv_ai["Employee Growth"] + mv_ai["Employee Growth_f"]) / 2

series_frame["Employee Opportunities"] = mv_ai["Final_Career Opportunities_bfill"]
series_frame["Management Proficiency"] = (mv_ai["Final_Senior Management_bfill"] + mv_ai[
    "Final_Senior Management_bfill"]) / 2
series_frame["Company Culture"] = (mv_ai["Final_Culture Values_bfill"] + mv_ai["Final_Culture Values_bfill"]) / 2
series_frame["Management Happiness"] = mv_ai["Final_Rating M"]
series_frame["Management Culture"] = mv_ai["Final_Culture Values M"]
series_frame["Management Comp."] = mv_ai["Final_Comp Benefits M"]

mv_ai = mv_ai[["ticker", "date", "Female_avg", "Male_avg", "Local_avg", "Foreign_avg", "High Network_avg",
               "Food Aestheticist_avg", "Female Importance_avg", "Average Customer Network_avg",
               "Number of Reviewers_avg"]]

mv_ai.columns = ["ticker", "date", "Female Rating", "Male Rating", "Local Rating", "Foreign Rating",
                 "High Network Rating", "Food Aestheticist Rating", "Female Importance", "Average Customer Network",
                 "Number of Reviewers"]

mv_ai = pd.concat((mv_ai, series_frame), axis=1)

ra = mv_ai.loc[:, "Female Importance":"Number of Reviewers"]
ba = pd.concat((ra, mv_ai.loc[:, "Search Traffic":"Employee Growth"]), axis=1)

ba = ba.replace(np.inf, np.nan)
ba = ba.fillna(method="ffill")
ba = ba.fillna(method="bfill")

ba = ba.fillna(ba.mean())

from sklearn.preprocessing import MinMaxScaler

scaler = MinMaxScaler(feature_range=(3.2, 4.6))
# scaler.fit(art_ratios["Extend"].values.reshape(-1, 1))
scaler.fit(ba)

# transed=scaler.transform(art_ratios["Extend"].values.reshape(-1, 1))

tranba = scaler.transform(ba)

tranba = pd.DataFrame(tranba, columns=ba.columns)

tranba = tranba.applymap(lambda x: x + np.random.normal(0.02, 0.04))

tranba = tranba.applymap(lambda x: x + np.log(3.9 / x) + 1 - 1 + np.sqrt(3.9 / x) - 1).round(2)

mv_ai = pd.concat((mv_ai.drop(tranba, axis=1), tranba), axis=1)

path = os.path.join(my_path, "../data/closure/")

market_series = pd.read_csv(path + "market_figure_series.csv").iloc[:, 1:]

bo = -1
for col in market_series.iloc[:, 1:]:
    bo = bo + 1
    if bo == 0:
        new = market_series[["date", col]]
        new["ticker"] = col
        new.columns = ["date", "AI Pred", "ticker"]
    rat = market_series[["date", col]]
    rat["ticker"] = col
    rat.columns = ["date", "AI Pred", "ticker"]
    new = pd.concat((new, rat), axis=0)

new["date"] = pd.to_datetime(new["date"], infer_datetime_format=True)

new = new[["date", "ticker", "AI Pred"]]

new = pd.merge(new, mv_ai, on=["date", "ticker"], how="left")

new.iloc[:, 2:] = new.iloc[:, 2:].round(2)

new["Qualitative Part"] = new.loc[:, "Female Rating":"Management Comp."].mean(axis=1)

new["Survival Part"] = new.loc[:, "Female Importance":].mean(axis=1)

new["Valuation Part"] = new["AI Pred"]

my_path = os.path.abspath(os.path.dirname('__file__'))
path_in_closure = os.path.join(my_path, "../data/closure/")

first = pd.read_csv(path_in_closure + "location_closure_2.csv")

first = first.iloc[:, 1:]

first["y_pred_proba"] = first["y_pred_proba"].astype("float") / 10
first["y_pred_proba"] = first["y_pred_proba"].round(4) * 100
first["y_pred_proba"] = first["y_pred_proba"].round(1)

averages = first.groupby("ticker").mean()

sorted_frame = averages
sorted_frame["rating"] = 1 / averages["y_pred_proba"]

from sklearn.preprocessing import MinMaxScaler

scaler = MinMaxScaler(feature_range=(3, 4.6))
# scaler.fit(art_ratios["Extend"].values.reshape(-1, 1))
scaler.fit(sorted_frame["rating"].to_frame())

# transed=scaler.transform(art_ratios["Extend"].values.reshape(-1, 1))

transr = scaler.transform(sorted_frame["rating"].to_frame())

transr = pd.DataFrame(transr, columns=sorted_frame["rating"].to_frame().columns)

sorted_frame["rating"] = transr["rating"].values

sorted_frame["rating"] = sorted_frame["rating"].apply(lambda x: np.log(4 / x) + x)

sorted_frame["rating"]

new = new.fillna(method="bfill")
new = new.fillna(method="ffill")

pd.set_option("display.max_rows", None)

new["Qualitative Part"] = new.loc[:, "Female Rating":"Management Comp."].mean(axis=1)

new["Survival Part"] = new.loc[:, "Female Importance":].mean(axis=1)

new["Valuation Part"] = new["AI Pred"]

new[["ticker", "date", "Qualitative Part"]][new["ticker"] == "BJRI"].isnull().sum()

## You have to do this roll, I 100% agree with it.
rare = new.sort_values("date").reset_index(drop=True)
# here = rare.iloc[:,:].copy()

rare.head()

rols = rare.groupby("ticker").rolling(90, on="date").mean().reset_index(drop=True)

# closures_real.loc[:,"closed":] = closures_real.loc[:,"closed":].applymap(lambda x: x + np.log(3.9/x)+1-1 + np.sqrt(3.9/x)-1 )
rew = rols

# closures_real[closures_real.index==c].values[0][0]

### Here I have historical closures - I cdo not yet have a purpose for it.
import _pickle as pickle

closed_list = []
dict_rea = {}
bo = -1
path_one = os.path.join(my_path, "../data/cpickle/")
for c in rew["ticker"].unique():
    closed_firm_list = []

    bo = bo + 1

    coy = c

    figures_dict = pickle.load(open(path_one + "figures_dict_" + coy + ".p", "rb"))

    # Of course you would eentually have to loop over all of these

    onlyfiles = [key[1] for key in figures_dict.keys()]
    counter = len(onlyfiles)

    path_out = os.path.join(my_path, "data/" + "/yelp/" + c + "/")

    code_start = onlyfiles[0]

    fulla_bulla = pd.DataFrame()
    h = -1

    for code_start in onlyfiles[:]:
        frame_already = pd.DataFrame.from_dict(figures_dict[c, code_start])

        if frame_already.loc["is_closed", "Response Data"] == True:
            closed_list.append(code_start)
            closed_firm_list.append(code_start)
    dict_rea[c] = len(closed_firm_list) / counter

closures_real = pd.DataFrame.from_dict(dict_rea, orient="index")

closures_real.columns = ["closed"]

closures_real["closed"] = 1 / closures_real["closed"].pow(1. / 3)
closures_real.loc[:, "closed":] = closures_real.loc[:, "closed":].applymap(
    lambda x: x + np.log(4.2 / x) + 1 - 1 + np.sqrt(4.2 / x) - 1 + np.sqrt(4.2 / x) - 1)

# rew = rew.dropna()

c = "BJRI"
gp = -1
for c in rew["ticker"].unique():
    gp = gp + 1
    subsamp = rew[rew["ticker"] == c]
    # Recalibration
    actual_valuation = new[new["ticker"] == c]["AI Pred"].rolling(window=90).mean().iloc[-1]
    subsamp["Valuation Part"] = subsamp["Valuation Part"] * actual_valuation / subsamp.iloc[-1, :]["Valuation Part"]

    actual_survival = sorted_frame[sorted_frame.index == c]["rating"].values[0]
    subsamp["Survival Part"] = subsamp["Survival Part"] * 0.40 + subsamp["Qualitative Part"] * 0.40 + subsamp[
                                                                                                          "Valuation Part"] * 0.20

    subsamp["Survival Part"] = subsamp["Survival Part"] * actual_survival / subsamp.iloc[-1, :]["Survival Part"]
    subsamp = subsamp.reset_index(drop=True)
    term = (closures_real[closures_real.index == c].values[0][0] - actual_survival) / len(subsamp)
    accy = 0
    for i in range(len(subsamp)):
        if i > 600:
            accy = accy + term
            subsamp.iloc[-i, -2] = subsamp.iloc[-i, -2] + accy

    actual_qualitative = absolute_df[absolute_df.index == c].mean(axis=1).values[0]
    subsamp["Qualitative Part"] = subsamp["Qualitative Part"] * actual_qualitative / subsamp.iloc[-1, :][
        "Qualitative Part"]

    if gp == 0:
        fullar = subsamp
    else:
        fullar = pd.concat((fullar, subsamp), axis=0)

fullar = fullar.reset_index(drop=True)
fullar["Overall Rating"] = fullar["Qualitative Part"] * .60 + fullar["Survival Part"] * .20 + fullar[
                                                                                                  "Valuation Part"] * .20

fullar.to_csv(path + "overall_rank_ts.csv", index=False)

absolute_df

col_newr = [
    'Service Sentiment', 'Food Sentiment',
    'Experience Sentiment', 'Process Sentiment', 'Restaurant Sentiment', 'Early Sentiment', 'Late Sentiment',
    'Overall Sentiment',

    'Food Quality', 'Price Index', 'Good Value', 'Visual Importance',
    'Foodie Index',

    'Convenience', 'Parking', 'Reservation', 'Catering', 'Delivery',

    'Connoisseur Rating', 'Aesthetician Rating', 'Visit Frequency', 'Network Size',

    'Management Proficiency', 'Company Culture', 'Management Happiness',
    'Management Culture', 'Management Comp.',

    'Offers Accepted', 'Employee Retention', 'Employee Growth', 'Employee Opportunities',

    'Website Popularity', 'Advertising Quality', 'Social Media Reach',
    'Quality Reach', 'Search Traffic',
    'Direct Traffic']

absolute_df = absolute_df[col_newr]

first_abs = absolute_df.loc[:, "Service Sentiment":'Delivery']

second_abs = absolute_df.loc[:, 'Connoisseur Rating':'Search Traffic']

second_abs = second_abs.T
second_abs["Avg"] = second_abs.mean(axis=1)

second_abs = second_abs.round(2).reset_index()

second_abs = second_abs.rename(columns={"index": "Metric"})

second_abs.loc[-1] = list(second_abs.columns)
second_abs.index = second_abs.index + 1  # shifting index
second_abs = second_abs.sort_index()

first_abs = first_abs.T
first_abs["Avg"] = first_abs.mean(axis=1)

first_abs = first_abs.round(2).reset_index()

first_abs = first_abs.rename(columns={"index": "Metric"})

first_abs.loc[-1] = list(first_abs.columns)
first_abs.index = first_abs.index + 1  # shifting index
first_abs = first_abs.sort_index()

my_path = os.path.abspath(os.path.dirname('__file__'))
path = os.path.join(my_path, "../data/closure/")

first_abs.to_csv(path + "first_abs.csv", index=False)

second_abs.to_csv(path + "second_abs.csv", index=False)

description_first = ["",
                     "Customer sentiment of in-house sentiment. It is an aggregate measure of waiting, price, manager, bill and check concerns.",
                     "Food sentiment gauges the overall sentiment for 12 core food items from bread, burgers, chicken to steak sauce and sandwiches.",
                     "Experience sentiment identifies key characteristics relating to location, parking, night atmosphere, kid friendliness, outside atmosphere, party suitability, friendly and family environment.",
                     "This measure tracks the overall process convenience. It includes sentiment surrounding the kitchen, orders, cutlery, water, drinks and the bar.",
                     "It is the average of Service, Food, Experience and Process sentiment.",
                     "Early Sentiment tracks the overall happiness of customers in the past and excludes the current quarter.",
                     "Late Sentiment tracks the overall happiness of customers in the past year, with a higher weighting on the current quarter.",
                     "This is an average of Early and Late Sentiment.",
                     "This is the best food quality isolating metric. It is obtained from delivery websites so it is not tainted by the in-house restaurant environment.",
                     "The Price Index gives an indication of the general prices of the restaurant's offering. It is obtained by looking at the prices for general items like Appetizers, Burgers and Sandwiches, Desserts, Pizzas and Pastas and Ribs and Steak.",
                     "Good Value measures the Food Quality divided by the Price Index.",
                     "Visual Importance tracks the amount of photos customers take of their food and the proportion of photo posts made by the restaurant in relation to general posts.",
                     "Foodie Index identifies the amount of restaurant experience i.e. food knowledge the average customer has.",
                     "Convenience measures the overall convenience and accessibility of the restaurant. It ranges from whether or not the firm accepts android and apple pay, the average weekly hours open, whether it is noisy, outdoor seating availability, parking and free Wi-Fi.",
                     "The general convenience of finding parking. It is included here because it has been shown to be one of the strong indicators for success especially the bike parking component.",
                     "Identifies whether the success of the restaurant's reservation system across all locations.",
                     "Identifies whether a catering service is provided by the firm and if so the quality of such service.",
                     "Identifies the extent of the delivery service is provided by the restaurant."]

description_second = ["",
                      "This rating identifies the average score knowledgeable food enthusiasts give the Restaurant. Unlike the Foodie Index, this does not track the number of such visitors, but just their average rating.",
                      "This rating identifies the average score visual or photo-active customers give the firm. This is a good indication of the presentation of the food as well as the general presentation of the restaurant.",
                      "Visit Frequency is primarily an indicator of how seasonal the firm is. A low number might suggest that the firm is busy in concentrated periods of the year rather than throughout the year.",
                      "Network size is a measure of the connectedness of the firm. It identifies the amount of friends/acquaintances patrons have. This measure can potentially be  proxy for the age group as it has a strong relation with youth. A lower measure can be indicative of an older age group.",
                      "Management proficiency identifies how effective and good management it from a lower-level employee perspective.",
                      "Company Culture Rating from perspective of lower level employees.",
                      "This measure tracks the general contentedness of management. ",
                      "This is a measure of management's rating of the restaurant's corporate culture.",
                      "This tracks managements's contentedness with their compensation package. This measure can be indicative of whether a firm pays, below, at or above average management salaries.",
                      "This measure tracks the extent to which when offered a job candidates accepted the position.",
                      "This measure tracks how good the firm is at retaining talented individuals. ",
                      "This measure tracks to what extent additional employees are added to the firm. This is calculated by dividing the additional employees with those that left.",
                      "This measure tracks lower level employees' perception of available opportunities to move up in the organization.",
                      "This calculates the website ranking reweighted by market value or expected market value.",
                      "This measure tracks the extent to which customers interact with advertisement. Shares, Comments and Reactions on Facebook, Shares on Twitter and Comments on Instagram. It includes a transformation by which Shares and Comments are divided by easy interactions to further isolate the quality of the ads.",
                      "This measures the total social media reach divided by the market value of the firm or the expected market value.",
                      "Quality reach measures the proportion of quality reach. Quality is defined as active customer interaction. If this measure is lower than the Social Media Reach it means that the firm should improve the quality of their ads, potentially by offering improved media or better interactive deals and coupons. On the other hand if this measure is too high, firms can focus on their reach and lower the quality of ads.",
                      "This measure offers a good proxy of customer brand awareness. It includes both a component of search directed to a website and general search trends on Google."]

descriptors = pd.DataFrame(columns=["First", "Second"])
descriptors["First"] = pd.Series(description_first)

descriptors["Second"] = pd.Series(description_second)

descriptors.to_csv(path + "descriptors.csv", index=False)