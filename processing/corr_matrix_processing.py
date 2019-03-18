import os
import pandas as pd

c = "RRGB"

input_fields = pd.read_csv("../input_fields.csv")

codes = input_fields["code_or_ticker"]

blu = -1
for c in codes:
    blu = blu + 1

    my_path = os.path.abspath(os.path.dirname('__file__'))
    path = os.path.join(my_path, "../input_fields.csv")
    path_in = os.path.join(my_path, "../data/ratings/")

    df_tick = pd.read_csv(path_in + c + "_stock_rate.csv")
    glassdoor = pd.read_csv(path_in + c + "_gdoor_employee_rate.csv")
    glassdoor_m = pd.read_csv(path_in + c + "_gdoor_mgmt_rate.csv")

    ## Alternative DF stock:

    path_in = os.path.join(my_path, "../data/stock/")
    df_tick = pd.read_csv(path_in + c + "_tick_df.csv")

    ## This is normalised, but I don't see why I shouldn't
    df_tick = df_tick.fillna(method="bfill").fillna(method="ffill")

    df_tick = df_tick[["close", "date"]]

    from scipy import signal

    glassdoor["ben_smooth"] = signal.savgol_filter(glassdoor["Final_Comp Benefits"], 199, 3)

    glassdoor["Review Date"] = pd.to_datetime(glassdoor["Review Date"], infer_datetime_format=True)
    glassdoor_m["Review Date"] = pd.to_datetime(glassdoor_m["date"], infer_datetime_format=True)
    new_door = glassdoor[["Review Date", "Final_Rating", "Final_Work Life Balance",
                          "Final_Culture Values", "Final_Career Opportunities",
                          "Final_Comp Benefits", "ben_smooth", "Final_Senior Management"]].set_index("Review Date")

    new_door_m = glassdoor_m[
        ["Review Date", "trace_mse", "trace_mwlb", "trace_mcva", "trace_mcop", "trace_mcbe", "trace_msma"]].set_index(
        "Review Date")

    df_tick["date"] = pd.to_datetime(df_tick["date"], infer_datetime_format=True)

    df_tick = df_tick.set_index("date")

    df_tick = pd.merge(df_tick, new_door, left_index=True, right_index=True, how="outer")

    df_tick = pd.merge(df_tick, new_door_m, left_index=True, right_index=True, how="outer")

    path_in = os.path.join(my_path, "../data/ratings/")
    yelp = pd.read_csv(path_in + "all_yelps_rates_" + c + ".csv")
    yelp["date"] = pd.to_datetime(yelp["date"], infer_datetime_format=True)

    df_tick = pd.merge(df_tick, yelp[["date", "all", "new"]].set_index("date"), left_index=True, right_index=True,
                       how="outer")

    df_tick = df_tick.fillna(method="bfill").fillna(method="ffill")

    df_tick.head()

    if blu == 0:
        df_full = df_tick
    else:
        df_full = pd.concat((df_full, df_tick), axis=0)

df_full = df_full.reset_index(drop=True)

corr_mat = df_full.corr()

from scipy.stats import pearsonr
import pandas as pd


def calculate_pvalues(df):
    df = df.dropna()._get_numeric_data()
    dfcols = pd.DataFrame(columns=df.columns)
    pvalues = dfcols.transpose().join(dfcols, how='outer')
    for r in df.columns:
        for c in df.columns:
            pvalues[r][c] = round(pearsonr(df[r], df[c])[1], 12)
    return pvalues


calculate_pvalues(df_full)

corr_mat

corr_mat = corr_mat[
    ["close", "Final_Work Life Balance", "Final_Culture Values", "Final_Career Opportunities", "Final_Comp Benefits",
     "trace_mcva", "Final_Senior Management", "trace_msma", "all", "new"]]

corr_mat = corr_mat[corr_mat.index.isin(["close", "all"])]

corr_mat.columns = ["Firm Value", "Work Life Balance", "Employee Culture", "Career Opportunities", "Compensation",
                    "Management Culture", "Management Competence", "Upper Management Competence",
                    "Customer Satisfaction", "Customer Transformed"]

corr_mat.index = ["Firm Value", "Customer Satisfaction"]