import os
import pandas as pd
import _pickle as pickle

my_path = os.path.abspath(os.path.dirname('__file__'))
path = os.path.join(my_path, "../input_fields.csv")

input_fields = pd.read_csv(path)

not_listed = input_fields[input_fields["listed"] == "No"].reset_index(drop=True)["code_or_ticker"]
path = os.path.join(my_path, "data/stock/")

parents = input_fields[input_fields["parent"]=="Yes"].reset_index(drop=True)["code_or_ticker"]

## Loop over all#
codes = input_fields["code_or_ticker"]
big_avg = pd.DataFrame()
r = -1
for code in codes:
    r = r + 1
    path = os.path.join(my_path, "../data/stock/")
    df_com = pd.read_csv(path + code + "_tick_df.csv")
    df_com["date"] = pd.to_datetime(df_com["date"], format="%Y-%m-%d")

    if code in list(not_listed):
        my_path = os.path.abspath(os.path.dirname('__file__'))
        path = os.path.join(my_path, "../data/cpickle/")
        art_ratios = pickle.load(open(path + "art_ratios.p", "rb"))
        art_ratios = art_ratios["mv"][code]
        art_ratios["close"] = (art_ratios["MV_pred"] / art_ratios["MV_pred"].iloc[0]) * 100
        print(art_ratios)
        art_ratios["date"] = pd.to_datetime(art_ratios["date"], infer_datetime_format=True)
        art_ratios["close"] = art_ratios["close"].rolling(30).mean()
        df_com = art_ratios
        # df_com["ticker"] = code_start

    if r == 0:
        big_avg = df_com
    else:
        big_avg = pd.merge(big_avg, df_com, on="date", how="left")

df2 = big_avg.filter(regex='close|date')

df2 = df2.set_index("date")
df2["mean"] = df2.mean(axis=1)

df2 = df2.reset_index()
df2 = df2[["date", "mean"]]
# for value in codes:

#    ben_frs_dict[value] =

# bench_start = "BJRI"
# code_start = "RRGB"

path = os.path.join(my_path, "../data/stock/")

df2.to_csv(path + "bench" + "_tick_df.csv")


for code in codes:

    path = os.path.join(my_path, "../data/stock/")

    df_com = pd.read_csv(path + code + "_tick_df.csv")

    df_com["date"] = pd.to_datetime(df_com["date"], format="%Y-%m-%d")

    if code in list(not_listed):
        my_path = os.path.abspath(os.path.dirname('__file__'))
        path = os.path.join(my_path, "../data/cpickle/")
        art_ratios = pickle.load(open(path + "art_ratios.p", "rb"))
        art_ratios = art_ratios["mv"][code]
        art_ratios["date"] = pd.to_datetime(art_ratios["date"], infer_datetime_format=True)
        art_ratios["close"] = (art_ratios["MV_pred"] / art_ratios["MV_pred"].iloc[0]) * 100
        art_ratios["close"] = art_ratios["close"].rolling(60).mean()

        if code in list(parents):
            my_path = os.path.abspath(os.path.dirname('__file__'))
            path = os.path.join(my_path, "../data/stock/")
            parent_frame = pd.read_csv(path + code + "_parent_tick_df.csv")
            parent_frame["date"] = pd.to_datetime(parent_frame["date"], infer_datetime_format=True)
            parent_frame = parent_frame.sort_values("date")
            parent_frame["close"] = (parent_frame["close"] / parent_frame["close"].iloc[0]) * 100
            art_ratios = art_ratios.set_index("date")
            parent_frame = parent_frame.set_index("date")
            rat_par = input_fields[input_fields["code_or_ticker"] == code]["oi_ratio"].reset_index(drop=True).iloc[0]
            art_ratios["close"] = art_ratios["close"] * (1 - rat_par) + parent_frame["close"] * (rat_par).copy()

            art_ratios["close_2"] = parent_frame["close"]
            # art_ratios["close_2"] = art_ratios["close_2"]*(100/art_ratios["close_2"].iloc[0])
            art_ratios["close"] = art_ratios["close"].fillna(art_ratios["close_2"])



        df_com = art_ratios
        path = os.path.join(my_path, "../data/stock/")

        df_com.to_csv(path + code + "_tick_df.csv")


    if code not in list(not_listed):
        my_path = os.path.abspath(os.path.dirname('__file__'))
        path = os.path.join(my_path, "../data/cpickle/")
        dict_fram = pickle.load(open(path + "simulated_stock.p", "rb"))
        dict_fram = dict_fram[code]
        dict_fram = dict_fram.sort_values("date")
        dict_fram["close"] = (dict_fram["MV_pred"] / dict_fram["MV_pred"].iloc[0]) * 100
        dict_fram["close"] = (dict_fram["close"] + df_com["close"]) / 2
        df_com_sim = dict_fram
        path = os.path.join(my_path, "../data/stock/")

        df_com_sim.to_csv(path + code + "_sim_tick_df.csv")

