import concurrent.futures
import os
from datetime import *
import pandas as pd

my_path = os.path.abspath(os.path.dirname('__file__'))
path = os.path.join(my_path, "../input_fields.csv")
path_in = os.path.join(my_path, "../data/ratings/")

input_fields = pd.read_csv(path)

# c= "SBUX"

code = input_fields["code_or_ticker"]


def runner(c):
    import pandas as pd
    import os
    import _pickle as pickle

    my_path = os.path.abspath(os.path.dirname('__file__'))
    path = os.path.join(my_path, "../input_fields.csv")
    path_in = os.path.join(my_path, "../data/ratings/")

    input_fields = pd.read_csv(path)

    glassdoor = pd.read_csv(path_in + c + "_gdoor_employee_rate.csv")
    glassdoor_m = pd.read_csv(path_in + c + "_gdoor_mgmt_rate.csv")
    df_tick = pd.read_csv(path_in + c + "_stock_rate.csv")
    yelp = pd.read_csv(path_in + "all_yelps_rates_" + c + ".csv")

    # c_corr = input_fields[input_fields["code_or_ticker"]==code]["ticker"].reset_index(drop=True)[0]

    from sklearn.decomposition import PCA

    pca = PCA(n_components=1)

    principalComponents = pca.fit_transform(yelp.iloc[:, 1:])

    my_path = os.path.abspath(os.path.dirname('__file__'))
    path = os.path.join(my_path, "../data/yelp/" + c + "/")

    path_out = os.path.join(my_path, "../data/ratings/")

    df_tick = pd.read_csv(path_out + c + "_stock_rate.csv")

    df_tick["date"] = pd.to_datetime(df_tick['date'], infer_datetime_format=True)

    full = df_tick.iloc[:, 1:]
    fol = pd.DataFrame()

    fol["date"] = pd.to_datetime(yelp['date'], infer_datetime_format=True)

    import numpy as np
    ##### Customers
    fol["customer_rating_pca"] = np.array([r[0] for r in principalComponents])

    fol["customer_rating_min"] = yelp.iloc[:, 1:].min(axis=1)

    fol["customer_rating_max"] = yelp.iloc[:, 1:].max(axis=1)

    fol["customer_rating_std"] = yelp.iloc[:, 1:].std(axis=1)

    full = pd.merge(full, fol, left_on="date", right_on="date", how="left")

    full = full.fillna(method="ffill")
    full = full.fillna(method="bfill")

    glassdoor["Review Date"] = pd.to_datetime(glassdoor['Review Date'], infer_datetime_format=True)

    glassdoor_m["date"] = pd.to_datetime(glassdoor_m['date'], infer_datetime_format=True)

    glassdoor = glassdoor.groupby("Review Date").mean().reset_index()

    full = pd.merge(full, glassdoor[["Review Date", 'Final_Rating', 'Final_Work Life Balance', 'Final_Culture Values',
                                     'Final_Career Opportunities', 'Final_Comp Benefits',
                                     'Final_Senior Management']], left_on="date", right_on="Review Date", how="left")

    glassdoor_m = glassdoor_m[['date', 'trace_mse', 'trace_mwlb', 'trace_mcva', 'trace_mcop', 'trace_mcbe',
                               'trace_msma']]

    glassdoor_m.columns = ["Review Date", 'Final_Rating M', 'Final_Work Life Balance M', 'Final_Culture Values M',
                           'Final_Career Opportunities M', 'Final_Comp Benefits M',
                           'Final_Senior Management M']

    glassdoor_m = glassdoor_m.groupby("Review Date").mean().reset_index()

    full = pd.merge(full, glassdoor_m, left_on="date", right_on="Review Date", how="left")

    # There might be an issue with glassdoor M being every day and glassdoor normal not - I don't think so, I think I can fill in the sleeves.

    ## Interview:
    from scipy import signal
    from datetime import datetime, timedelta

    from plotly.offline import download_plotlyjs, init_notebook_mode, plot, iplot

    init_notebook_mode(connected=True)

    from datetime import datetime
    from dateutil.parser import parse
    import os

    my_path = os.path.abspath(os.path.dirname('__file__'))
    path_2 = os.path.join(my_path, "../input_fields.csv")
    path_in_gdoor = os.path.join(my_path, "../data/glassdoor/")

    # input_fields = pd.read_csv(path)

    # code = input_fields["code_or_ticker"]

    p = c

    # y_path = os.path.abspath(os.path.dirname('__file__'))
    # pathy = os.path.join(y_path, "../data/interviews/")

    inter = pd.read_csv(path_in_gdoor + p + "_interview.csv")

    inter.loc[:, "Offer":"Question"] = inter.loc[:, "Offer":"Question"].applymap(lambda x: x[2:-2])

    inter

    inter['Interview Date'] = pd.to_datetime(inter['Interview Date'], infer_datetime_format=True, errors='coerce')

    inter = inter[~inter["Interview Date"].isnull()]

    inter = inter.sort_values("Interview Date")

    inter["Experience"].value_counts()

    exp = inter["Experience"].value_counts()

    try:
        pos = exp[0]
    except:
        pos = 0
    try:
        neu = exp[1]
    except:
        neu = 0
    try:
        neg = exp[2]
    except:
        neg = 0

    all_i = pos + neu + neg

    uno = (pos * 5 + neu * 2.5 + neg * 1) / (all_i * 5) * 5

    # Then we round it to 2 places
    uno = round(uno, 1)

    off = inter["Offer"].value_counts()

    try:
        of = off[0]
    except:
        of = 0
    try:
        no = off[1]
    except:
        no = 0
    try:
        de = off[2]
    except:
        de = 0

    inter["accepted"] = inter["Offer"].apply(lambda x: 1 if x == "Accepted Offer" else 0)

    inter["perc_acc"] = inter["accepted"].rolling(30).sum()

    inter["perc_acc"] = inter["perc_acc"].fillna(method="bfill")

    inter["perc_acc"] = inter["perc_acc"] / 30

    inter["perc_acc"] = inter["perc_acc"].round(2)

    try:
        inter["perc_acc"] = signal.savgol_filter(inter["perc_acc"], 31, 3)
    except:
        try:
            inter["perc_acc"] = signal.savgol_filter(inter["perc_acc"], 20, 3)
        except:
            inter["perc_acc"] = 0.5

    int_type = exp = inter["Interview Type"].value_counts()

    inter = inter.groupby("Interview Date").mean().reset_index()

    full = pd.merge(full, inter[["Interview Date", "perc_acc"]], left_on="date", right_on="Interview Date", how="left")

    try:
        easy = int_type[0]
    except:
        easy = 0
    try:
        avg = int_type[1]
    except:
        avg = 0
    try:
        diff = int_type[2]
    except:
        diff = 0

    full["Easy_Int"] = easy / int_type.sum()
    full["Easy_Int"] = full["Easy_Int"] * (1 + np.random.normal(-0.01, 0.01, len(full)))
    full["Avg_Int"] = avg / int_type.sum()
    full["Avg_Int"] = full["Avg_Int"] * (1 + np.random.normal(-0.01, 0.01, len(full)))
    full["Diff_Int"] = diff / int_type.sum()
    full["Diff_Int"] = full["Diff_Int"] * (1 + np.random.normal(-0.01, 0.01, len(full)))

    full["Pos_Int"] = pos / int_type.sum()
    full["Pos_Int"] = full["Pos_Int"] * (1 + np.random.normal(-0.01, 0.01, len(full)))
    full["Neu_Int"] = neu / int_type.sum()
    full["Neu_Int"] = full["Neu_Int"] * (1 + np.random.normal(-0.01, 0.01, len(full)))
    full["Neg_Int"] = neg / int_type.sum()
    full["Neg_Int"] = full["Neg_Int"] * (1 + np.random.normal(-0.01, 0.01, len(full)))

    full["Offered_Int"] = of / int_type.sum()
    full["Offered_Int"] = full["Offered_Int"] * (1 + np.random.normal(-0.01, 0.01, len(full)))
    full["Nooffer_Int"] = no / int_type.sum()
    full["Nooffer_Int"] = full["Nooffer_Int"] * (1 + np.random.normal(-0.01, 0.01, len(full)))
    full["Decline_Int"] = de / int_type.sum()
    full["Decline_Int"] = full["Decline_Int"] * (1 + np.random.normal(-0.01, 0.01, len(full)))

    short = input_fields["short_name"]
    codes = input_fields["code_or_ticker"]
    my_path = os.path.abspath(os.path.dirname('__file__'))
    path_out = my_path + "/../data/linkedin/"

    dop_dict = pickle.load(open(path_out + "employee.p", "rb"))

    employee_frame = dop_dict["insights"][c][
        ["date", "allEmployeeHireCount", "employee_count", "employee_add", "employee_left"]]

    full = pd.merge(full, employee_frame, on="date", how="left")

    full.shape

    ## Some Convenience Stuff

    target_code = c

    import _pickle as pickle
    import pandas as pd
    import dash_html_components as html
    import os

    def make_dash_table(df):
        ''' Return a dash definitio of an HTML table for a Pandas dataframe '''
        table = []
        for index, row in df.iterrows():
            html_row = []
            for i in range(len(row)):
                html_row.append(html.Td([row[i]]))
            table.append(html.Tr(html_row))
        return table

    my_path = os.path.abspath(os.path.dirname('__file__'))

    path_out = os.path.join(my_path, "../data/yelp_info/")
    path_in_ngrams = os.path.join(my_path, "../data/cpickle/")

    final_df = pd.read_csv(path_out + "extra_info.csv")

    final_df = final_df.set_index("Unnamed: 0")

    i_dict = pickle.load(open(path_in_ngrams + "i_dict.p", "rb"))

    path = os.path.join(my_path, "input_fields.csv")

    # input_fields = pd.read_csv(path)

    # code_rest = list(input_fields["code_or_ticker"])

    try:
        frame_g = pd.DataFrame.from_dict(i_dict[target_code], orient="columns").T
    except:
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

    try:
        frame_agg = pd.DataFrame.from_dict(i_dict[target_code], orient="columns").T
    except:
        frame_agg = pd.DataFrame.from_dict(i_dict[target_code], orient="index")

    frame_agg = pd.DataFrame(index=frame_agg.index)

    for key, value in i_dict[target_code].items():
        print(value)
        if key == "Average Hours":
            full[key] = value
        else:
            try:
                try:
                    full[key] = value["Yes"]
                except:
                    full[key] = value
            except KeyError:
                full[key] = 1

        full[key] = full[key] * (1 + np.random.normal(-0.01, 0.01, len(full)))

    rull = full.copy()

    import pandas as pd
    import numpy as np
    import json
    import os
    from datetime import *

    my_path = os.path.abspath(os.path.dirname('__file__'))
    path_in_ngrams = os.path.join(my_path, "../data/cpickle/")
    my_path = os.path.abspath(os.path.dirname('__file__'))
    path = os.path.join(my_path, "../input_fields.csv")

    input_fields = pd.read_csv(path)

    code = input_fields["code_or_ticker"]

    from os import listdir
    from os.path import isfile, join

    code = input_fields["code_or_ticker"]
    full_dict = {}

    # code = code.iloc[0]
    code = [c]
    for coy in code:
        full_dict[coy] = {}

        my_path = os.path.abspath(os.path.dirname('__file__'))
        path = os.path.join(my_path, "../data/yelp_info/" + coy + "/")

        path_out = os.path.join(my_path, "../data/extra_info/")

        onlyfiles = [f for f in listdir(path) if isfile(join(path, f))]

        names_final = []
        for li in onlyfiles:
            if len(li) > 15:
                li = li[:-4]
                names_final.append(li)

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
        for i in range(len(onlyfiles)):
            my_string = onlyfiles[i]
            full_names.append(my_string)
            li = my_string
            if len(li) > 4:
                li = re.sub(r'|'.join(map(re.escape, list(words))), '', li)
                small_names.append(li[:-4])

        for big, small in zip(full_names, small_names):

            if big == ".DS_Store":
                continue

            path = my_path + "/../data/yelp_info/" + coy + "/" + big

            extra = pd.read_csv(path)

            extra.columns = ["Day", "Hours Opened", "Business Info", "Detail", "Also-Considered", "Considered Link",
                             "Also-Viewed", "Viewed Link"]

            extra_dict = {}

            extra_dict["hours_open"] = {}

            for i, h in zip(extra["Day"], extra["Hours Opened"]):
                try:
                    if len(i) > 1:
                        extra_dict["hours_open"][i] = h
                except:
                    continue

            extra_dict["business_info"] = {}

            for i, h in zip(extra["Business Info"], extra["Detail"]):
                try:
                    if len(i) > 1:
                        extra_dict["business_info"][i] = h
                except:
                    continue

            extra_dict["also_considered"] = {}

            for i, h in zip(extra["Also-Considered"], extra["Considered Link"]):
                try:
                    if len(i) > 1:
                        extra_dict["also_considered"][i] = h
                except:
                    continue

            extra_dict["also_viewed"] = {}

            for i, h in zip(extra["Also-Viewed"], extra["Viewed Link"]):
                try:
                    if len(i) > 1:
                        extra_dict["also_viewed"][i] = h
                except:
                    continue
            extra_dict["small_name"] = small

            full_dict[coy][big] = extra_dict

    info_dict = {}
    for i in full_dict.keys():
        info_dict[i] = {}
        for r in full_dict[i].keys():
            ext = full_dict[i][r]
            info_dict[i][r] = {}
            total_hours = 0
            for g, hours in ext["hours_open"].items():
                if hours == "Open 24 hours":
                    hours = 24
                else:
                    hours = hours.replace(' Open now', "")
                    if hours == "Closed":
                        continue
                    if len(hours) > 33:

                        ga = hours.split(" pm - ")
                        time_1 = ga[0].split(" - ")[0]
                        time_2 = ga[1]

                        if len(ga) == 3:
                            ga = hours.split(" - ")
                            time_1 = ga[0]
                            time_2 = ga[2]

                        t1 = datetime.strptime(time_1, '%I:%M %p')
                        t2 = datetime.strptime(time_2, '%I:%M %p')
                        tdiff = t2 - t1 - timedelta(hours=2.5)

                    elif len(hours.split("-")) > 2:

                        ga = hours.split("-")
                        ra = ga[1].split(ga[1][6:9].replace(" ", ""))

                        str_dict = {}
                        a = -1
                        for w in ra[:2]:
                            a = a + 1
                            if ga[1][6:9].replace(" ", "") not in w:
                                str_dict[a] = w + ga[1][6:9].replace(" ", "")

                        time_1 = str_dict[0][1:]
                        time_2 = str_dict[0][1:]

                        t1 = datetime.strptime(time_1, '%I:%M %p')
                        t2 = datetime.strptime(time_2, '%I:%M %p')
                        diffy_dat = t2 - t1

                        time_1 = hours.split("-")[0][:-1]

                        time_2 = hours.split("-")[2][1:]

                        t1 = datetime.strptime(time_1, '%I:%M %p')
                        t2 = datetime.strptime(time_2, '%I:%M %p')
                        tdiff = t2 - t1
                        tdiff = tdiff - diffy_dat
                    else:
                        time_1 = hours.split("-")[0][:-1]

                        time_2 = hours.split("-")[1][1:]
                        print(time_1, time_2)
                        try:
                            t1 = datetime.strptime(time_1, '%I:%M %p')
                            t2 = datetime.strptime(time_2, '%I:%M %p')
                        except:
                            continue
                        tdiff = t2 - t1
                    hours = tdiff.seconds / (60 * 60)
                total_hours = total_hours + hours
            info_dict[i][r]["total_hours"] = total_hours
    list_infos = []
    for i in full_dict.keys():
        for r in full_dict[i].keys():
            ext = full_dict[i][r]
            list_infos.extend(list(ext["business_info"].keys()))

    list_infos.append("Small Name")
    list_infos.append("Target Name")
    list_infos.append("Hours Open")

    new_frame = pd.DataFrame(index=list(set(list_infos)))

    for i in full_dict.keys():
        for r in full_dict[i].keys():
            ext = full_dict[i][r]
            ext["business_info"]["Small Name"] = ext["small_name"]
            ext["business_info"]["Target Name"] = i
            ext["business_info"]["Hours Open"] = info_dict[i][r]["total_hours"]
            fa = pd.DataFrame.from_dict(ext["business_info"], orient='index', dtype=None)
            fa.columns = [r]
            new_frame = new_frame.join(fa, how="outer")

    frame_t = new_frame.T
    frame_t_2 = frame_t.fillna(frame_t.mode().T[0])

    frame_t_2["Wi-Fi"] = frame_t_2["Wi-Fi"].replace(['Paid', 'Paid'], 'No')

    frame_t_2["Noisy"] = frame_t_2['Noise Level'].replace(['Average', 'Quiet'], 'No')

    frame_t_2["Noisy"] = frame_t_2["Noisy"].replace(['Loud', 'Very Loud'], 'Yes')

    final_df = frame_t_2[
        ['Wi-Fi', 'Target Name', 'Hours Open', 'Takes Reservations', 'Outdoor Seating', 'Delivery', 'Caters',
         'Bike Parking', 'Accepts Apple Pay', 'Accepts Android Pay', 'Noisy']]

    final_df = final_df.replace({"Yes": 1, "No": 0, "Free": 1}).drop("Target Name", axis=1).T

    from sklearn.decomposition import PCA

    pca = PCA(n_components=1)

    principalComponents = pca.fit_transform(final_df)

    final_df["convenience_pca"] = np.array([r[0] for r in principalComponents])

    final_df["convenience_std"] = final_df.std(axis=1)

    final_df = final_df[["convenience_pca", "convenience_std"]].T

    # PCA and STD convenience Transformations
    for ind in final_df.index:
        for col in final_df.columns:
            full[col + "_" + ind] = final_df.loc[ind, col]
            full[col + "_" + ind] = full[col + "_" + ind] * (1 + np.random.normal(-0.01, 0.01, len(full)))

    ##  Social Websites And Stuff:

    my_path = os.path.abspath(os.path.dirname('__file__'))
    path = os.path.join(my_path, "../input_fields.csv")

    input_fields = pd.read_csv(path)

    short = input_fields["short_name"]
    codes = input_fields["code_or_ticker"]

    my_path = os.path.abspath(os.path.dirname('__file__'))
    path_out = my_path + "/../data/similarweb/"
    fi_dict = pickle.load(open(path_out + "website.p", "rb"))

    import plotly.plotly as py
    import plotly.graph_objs as go
    from plotly import tools
    import plotly.plotly as py
    import plotly.graph_objs as go
    from plotly import tools

    fi_dict["key_metrics"] = fi_dict["key_metrics"].set_index("Firm")

    c = c
    prox = fi_dict["key_metrics"]["Category Rank"].iloc[1:].replace({',': ''},
                                                                    regex=True).fillna(method="bfill").astype(
        int).sort_values(ascending=False).index[0]
    try:
        fram = fi_dict["key_metrics"].loc[c, :]
    except:
        fram = fi_dict["key_metrics"].loc[prox, :]

    my_time = fram.loc["Avg Visit Duration"]

    t1 = sum(i * j for i, j in zip(map(int, my_time.split(':')), [60, 1, 1 / 60]))

    fram.loc["Avg Visit Duration"] = t1

    fram.loc["Total Visits"] = fram.loc["Total Visits"][:-1]

    fram.loc["Pages Per Visit"] = fram.loc["Total Visits"][:-1]
    fram.loc["Bounce Rate"] = fram.loc["Bounce Rate"][:-1]
    fram.loc["Seo Click"] = fram.loc["Seo Click"][:-1]
    fram.loc["PPC Click"] = fram.loc["PPC Click"][:-1]
    fram.loc["Adwords Budget"] = fram.loc["Adwords Budget"][:-1]

    fram = fram.replace({',': ''},
                        regex=True).astype(float)

    for key, values in fram.items():
        full[key] = values
        full[key] = full[key] * (1 + np.random.normal(-0.01, 0.01, len(full)))

    ## Similar Web Frame
    path_out = my_path + "/../data/similarweb/"

    try:
        rad = pd.read_csv(path_out + coy + "_similarweb.csv")
    except:
        try:
            rad = pd.read_csv(path_out + prox + "_similarweb.csv")
        except:
            print("no similarweb")

    fi_dict["referrals"] = fi_dict["referrals"].set_index("index")

    fi_dict["referrals"].columns = fi_dict["referrals"].iloc[0].values

    try:

        fra = fi_dict["referrals"].loc[c]

        fra = fra.to_frame()

        fra[c] = [f[:-2] for f in fra[c].values]

        fra = fra[c]

        fra = fra.replace({',': ''},
                          regex=True).astype(float)
    except:
        fra = fi_dict["referrals"].loc[prox]

        fra = fra.to_frame()

        fra[prox] = [f[:-2] for f in fra[prox].values]

        fra = fra[prox]

        fra = fra.replace({',': ''},
                          regex=True).astype(float)

    for key, values in fra.items():
        full[key] = values
        full[key] = full[key] * (1 + np.random.normal(-0.01, 0.01, len(full)))

    # ## Some Larger Form Ratings:

    # import _pickle as pickle
    # import pandas as pd

    # agg = pickle.load(open(path_in_ngrams + "figures_dict_agg.p", "rb"))

    # fig_d_n = agg[target_code]


    # figures_dict = pickle.load(open(path_in_ngrams + "figures_dict_" + target_code + ".p", "rb"))

    ## Stealing Some Previous Agg Functions:


    my_path = os.path.abspath(os.path.dirname('__file__'))
    path = os.path.join(my_path, "../input_fields.csv")

    input_fields = pd.read_csv(path)

    # tick  = [x for x in input_fields[input_fields["ticker"]!="PE"].ticker]

    code = input_fields[input_fields["code_or_ticker"] != "x"]["code_or_ticker"]
    path_in_ngrams = os.path.join(my_path, "../data/cpickle/")

    dicta = {}

    figures_dict = pickle.load(open(path_in_ngrams + "figures_dict_" + coy + ".p", "rb"))
    df_frame = pd.DataFrame(index=range(len(figures_dict)))

    fig_d = figures_dict[next(iter(figures_dict))]

    df_frame["Male to Female"] = fig_d["Male to Female"]

    df_frame["Foreign to Local"] = fig_d["Foreign to Local"]

    df_frame["Male"] = fig_d["Male"]

    df_frame["Female"] = fig_d["Female"]

    df_frame["Local"] = fig_d["Local"]

    df_frame["Foreign"] = fig_d["Foreign"]

    df_frame["High Network"] = fig_d["High Network"]

    df_frame["Low Network"] = fig_d["Low Network"]

    df_frame["Connoisseur"] = fig_d["Connoisseur"]

    df_frame["Food Aestheticist"] = fig_d["Food Aestheticist"]

    df_frame["Patrons"] = fig_d["Patrons"]

    df_frame["First Visit"] = fig_d["First Visit"]

    df_frame["Visual Importance"] = fig_d["Visual Importance"]

    df_frame["Female Importance"] = fig_d["Female Importance"]

    df_frame["Foreign Importance"] = fig_d["Foreign Importance"]

    df_frame["Average Customer Network"] = fig_d["Average Customer Network"]

    df_frame["Total Network"] = fig_d["Total Network"]

    df_frame["Number of Reviewers"] = fig_d["Number of Reviewers"]

    rant = -1
    for key, fig_d in figures_dict.items():
        rant = rant + 1
        df_frame["Male to Female"][rant] = fig_d["Male to Female"]

        df_frame["Foreign to Local"][rant] = fig_d["Foreign to Local"]

        df_frame["Male"][rant] = fig_d["Male"]

        df_frame["Female"][rant] = fig_d["Female"]

        df_frame["Local"][rant] = fig_d["Local"]

        df_frame["Foreign"][rant] = fig_d["Foreign"]

        df_frame["High Network"][rant] = fig_d["High Network"]

        df_frame["Low Network"][rant] = fig_d["Low Network"]

        df_frame["Connoisseur"][rant] = fig_d["Connoisseur"]

        df_frame["Food Aestheticist"][rant] = fig_d["Food Aestheticist"]

        df_frame["Patrons"][rant] = fig_d["Patrons"]

        df_frame["First Visit"][rant] = fig_d["First Visit"]

        df_frame["Visual Importance"][rant] = fig_d["Visual Importance"]

        df_frame["Female Importance"][rant] = fig_d["Female Importance"]

        df_frame["Foreign Importance"][rant] = fig_d["Foreign Importance"]

        df_frame["Average Customer Network"][rant] = fig_d["Average Customer Network"]

        df_frame["Total Network"][rant] = fig_d["Total Network"]

        df_frame["Number of Reviewers"][rant] = fig_d["Number of Reviewers"]

    df_frame["reviewers_percentage"] = df_frame["Number of Reviewers"] / df_frame["Number of Reviewers"].sum()

    df_frame_2 = df_frame.drop(["reviewers_percentage"], axis=1) * df_frame["reviewers_percentage"]

    df_frame = df_frame.fillna(df_frame.mean())

    df_frame_2 = df_frame.drop(["reviewers_percentage", "Total Network", "Number of Reviewers"], axis=1).mul(
        df_frame["reviewers_percentage"], axis=0)

    df_frame_2["reviewers_percentage"] = df_frame["reviewers_percentage"]
    df_frame_2["Total Network"] = df_frame["Total Network"]
    df_frame_2["Number of Reviewers"] = df_frame["Number of Reviewers"]

    dicta[coy] = df_frame_2.sum().to_dict()

    for key, values in dicta[c].items():
        full[key + "_avg"] = values
        full[key + "_avg"] = full[key + "_avg"] * (1 + np.random.normal(-0.01, 0.01, len(full)))

    df_frame = df_frame.T

    from sklearn.decomposition import PCA

    # pca = PCA(n_components=1)

    # principalComponents = pca.fit_transform(df_frame)

    # import numpy as np
    # ##### Customers
    # full["customer_rating_pca"] = np.array([r[0] for r in principalComponents])

    df_frame["min"] = df_frame.min(axis=1)

    df_frame["max"] = df_frame.max(axis=1)

    df_frame["std"] = df_frame.std(axis=1)

    df_frame = df_frame[["min", "max", "std"]]

    df_frame = df_frame.T

    # PCA and STD convenience Transformations
    for ind in df_frame.index:
        for col in df_frame.columns:
            full[col + "_" + ind] = df_frame.loc[ind, col]
            full[col + "_" + ind] = full[col + "_" + ind] * (1 + np.random.normal(-0.01, 0.01, len(full)))

    ## Do the Filla Forward and Backward From here: You just ocunt nULLS AND START FROM THERE.

    full.shape

    pd.set_option('display.max_rows', 500)
    pd.set_option('display.max_columns', 500)

    forward = full[["Review Date_x",
                    "Final_Rating",
                    "Final_Work Life Balance",
                    "Final_Culture Values",
                    "Final_Career Opportunities",
                    "Final_Comp Benefits",
                    "Final_Senior Management",
                    "Interview Date",
                    "perc_acc",
                    "allEmployeeHireCount",
                    "employee_count",
                    "employee_add",
                    "employee_left"]]

    forward = forward.fillna(method="ffill")
    forward = forward.fillna(method="bfill")
    forward.columns = [g + "_ffill" for g in forward.columns]

    coll = pd.concat((full, forward), axis=1)

    backward = full[["Review Date_x",
                     "Final_Rating",
                     "Final_Work Life Balance",
                     "Final_Culture Values",
                     "Final_Career Opportunities",
                     "Final_Comp Benefits",
                     "Final_Senior Management",
                     "Interview Date",
                     "perc_acc",
                     "allEmployeeHireCount",
                     "employee_count",
                     "employee_add",
                     "employee_left"]]

    backward = backward.fillna(method="bfill")
    backward = backward.fillna(method="ffill")
    backward.columns = [g + "_bfill" for g in backward.columns]

    coll = pd.concat((coll, backward), axis=1)

    coll = coll.drop(["Review Date_x",
                      "Final_Rating",
                      "Final_Work Life Balance",
                      "Final_Culture Values",
                      "Final_Career Opportunities",
                      "Final_Comp Benefits",
                      "Final_Senior Management",
                      "Interview Date",
                      "perc_acc",
                      "allEmployeeHireCount",
                      "employee_count",
                      "employee_add",
                      "employee_left"], axis=1)

    coll = coll.drop(["Review Date_y", "Review Date_x_ffill", "Interview Date_ffill", "Review Date_x_ffill"], axis=1)

    coll.to_csv(my_path + "/full_synth/" + c + "_full.csv", index=False)


# code =["SBUX"]

with concurrent.futures.ProcessPoolExecutor() as executor:
    for c in executor.map(runner, code):
        print(c)

