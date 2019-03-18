import pandas as pd
import os
import _pickle as pickle

my_path = os.path.abspath(os.path.dirname('__file__'))
path = os.path.join(my_path, "../input_fields.csv")

input_fields = pd.read_csv(path)

# tick  = [x for x in input_fields[input_fields["ticker"]!="PE"].ticker]

code = input_fields[input_fields["code_or_ticker"] != "x"]["code_or_ticker"]
path_in_ngrams = os.path.join(my_path, "../data/cpickle/")

dicta = {}
for coy in code:

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

    df_frame_2 = df_frame.drop(["reviewers_percentage","Total Network","Number of Reviewers"], axis=1).mul(df_frame["reviewers_percentage"], axis=0)

    df_frame_2["reviewers_percentage"] = df_frame["reviewers_percentage"]
    df_frame_2["Total Network"] = df_frame["Total Network"]
    df_frame_2["Number of Reviewers"] = df_frame["Number of Reviewers"]

    dicta[coy] = df_frame_2.sum().to_dict()

my_path = os.path.abspath(os.path.dirname('__file__'))

path_in_ngrams = os.path.join(my_path, "../data/cpickle/")
pickle.dump(dicta, open(path_in_ngrams + "figures_dict_agg.p", "wb"))


