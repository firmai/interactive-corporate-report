import pandas as pd
import os
import numpy as np
import _pickle as pickle

my_path = os.path.abspath(os.path.dirname('__file__'))
path_in_ngrams = os.path.join(my_path, "../data/cpickle/")

path_in_pos = os.path.join(my_path, "../data/pos/")

my_path = os.path.abspath(os.path.dirname('__file__'))
path = os.path.join(my_path, "../input_fields.csv")

input_fields = pd.read_csv(path)

code = input_fields["code_or_ticker"]


code = input_fields["code_or_ticker"]
full_dict = {}
agg = pickle.load(open(path_in_ngrams + "figures_dict_agg.p", "rb"))

code

avr = []
inde = []
for key, values in agg.items():
    male_prop = values["Male to Female"] / (values["Male to Female"] + 1)
    female_prop = 1 - male_prop
    avg_rating = values["Male"] * male_prop + values["Female"] * female_prop
    avr.append(avg_rating)
    inde.append(key)

average_rating = pd.DataFrame(avr, index=inde)

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

average_rating.columns = ["Full Rate"]

rates_df = rates_df.groupby("Target").mean()
rates_df.columns = ["Self Rate"]

rating_data = average_rating.join(rates_df, how="outer")

rating_data

for col in rating_data:
    rating_data[col] = rating_data[col] / rating_data[col].max()

service = ["waitress",
           "service",
           "time", "staff",
           "waiter",
           "manager",
           "servers",
           "check",
           "price",
           "hostess",
           "waiting",
           "bill",
           "management"
           ]

food = [
    "chicken",
    "pizza",
    "steak",
    "salad",
    "burger",
    "fries",
    "dessert",
    "cheese",
    "bread",
    "sandwich",
    "pasta",
    "sauce"
]

preparation = [
    "food",
    "dish",
    "lunch",
    "portion",
    "menu",
    "meal",
    "order",
    "dinner",
    "appetizer",
    "drinks",
    "bar",
    "beer",
    "drink",
    "water",
    "plates",
    "kitchen"
]

location = ["place",
            "restaurant",
            "experience",
            "location",
            "night",
            "visit",
            "family",
            "friends",
            "kids",
            "birthday",
            "area",
            "atmosphere",
            "outside",
            "parking"
            ]

big_pro_g = pd.read_csv(path_in_pos + "big_ass_q1_" + code[0] + "_bad_good.csv")
coll_df = pd.DataFrame(columns=big_pro_g.columns)
# code = code.iloc[0]
types_df = {}
for ar, aes in zip([service, food, preparation, location], ["service", "food", "preparation", "location"]):
    types_df[aes] = {}
    for qr, des in zip(["q1_", "q2_", ""], ["q1", "q2", "all"]):
        all_fir = pd.DataFrame(index=ar)
        for coy in code:
            coll_df = pd.read_csv(path_in_pos + "big_ass_" + qr + coy + "_good_bad.csv")

            len(coll_df)

            coll_df["good"] = coll_df["good"].astype(float)

            rat = coll_df.groupby("name").sum()

            rat.sort_values("good", ascending=False).iloc[:-1, :]

            dar = rat[rat.index.isin(ar)]
            dar[coy] = dar["good"] / dar["bad"]
            all_fir = all_fir.join(dar[coy], how="outer")
            all_t = all_fir.T
        for col in all_t.columns:
            all_t[col] = all_t[col].map(lambda x: None if (x == 0.000) else x)
        all_t = all_t.replace([np.inf, -np.inf], np.nan)

        all_t = all_t.fillna(all_t.mean())

        types_df[aes][des] = all_t.T

most = [0, 0, 0, 0.5, 0.5, 0.5, 0, 0, 0, 0.5, 0.5, 0.5, 0, 0, 0, 0.5, 0.5, 0.5, 0, 0, 0, 0.5, 0.5, 0.5, 0, 0, 0, 0.5,
        0.5, 0.5, 0, 0, 0, 0.5, 0.5, 0.5, 0, 0, 0, 0.5, 0.5, 0.5, 0, 0, 0, 0.5, 0.5, 0.5, 0, 0, 0, 0.5, 0.5, 0.5, 0, 0,
        0, 0.5, 0.5, 0.5, 0, 0, 0, 0.5, 0.5, 0.5, 0, 0, 0, 0.5, 0.5, 0.5, 0, 0, 0, 0.5, 0.5, 0.5, 0, 0, 0, 0.5, 0.5,
        0.5, 0, 0, 0, 0.5, 0.5, 0.5, 0, 0, 0, 0.5, 0.5, 0.5, 0, 0, 0, 0.5, 0.5, 0.5]

dt = {}
for ar, aes in zip([service, food, preparation, location], ["service", "food", "preparation", "location"]):
    # Set Final All
    pow_a = types_df[aes]["all"].pow(1 / 4)

    max_row = [1 / max(row) for index, row in pow_a.iterrows()]

    import numpy as np

    noise = np.random.normal(0, 1, len(pow_a)) * .10

    noise = 1 - np.absolute(noise)

    pow_a_final = pow_a.mul(max_row, axis=0).mul(noise, axis=0)

    q1_frame = types_df[aes]["q1"]

    pow_q1 = q1_frame.pow(1 / 4)

    max_row = [1 / max(row) for index, row in pow_q1.iterrows()]

    import numpy as np

    np.random.seed(1)

    noise = np.random.normal(0, 1, len(pow_q1)) * .10

    noise = 1 - np.absolute(noise)

    pow_q1 = pow_q1.mul(max_row, axis=0).mul(noise, axis=0)

    pow_q1 = pow_q1.fillna(pow_a_final.mean())

    np.random.seed(1)

    noise = np.random.normal(0, 1, len(pow_q1)) * .10

    noise = 1 + np.absolute(noise)

    pow_q1 = pow_q1.mul(noise, axis=0)

    np.random.seed(3)

    noise = np.random.normal(0, 1, len(pow_q1)) * .10

    noise = 1 - np.absolute(noise)

    pow_q1 = pow_q1.mul(noise, axis=0)

    pow_q1_final = pow_q1 * 0.40 + pow_a_final * 0.60

    q2_frame = types_df[aes]["q2"]

    pow_q2 = q2_frame.pow(1 / 4)

    max_row = [1 / max(row) for index, row in pow_q2.iterrows()]

    import numpy as np

    np.random.seed(1)

    noise = np.random.normal(0, 1, len(pow_q2)) * .10

    noise = 1 - np.absolute(noise)

    pow_q2 = pow_q2.mul(max_row, axis=0).mul(noise, axis=0)

    pow_q2 = pow_q2.fillna(pow_a_final.mean())

    np.random.seed(1)

    noise = np.random.normal(0, 1, len(pow_q2)) * .10

    noise = 1 + np.absolute(noise)

    pow_q2 = pow_q2.mul(noise, axis=0)

    np.random.seed(3)

    noise = np.random.normal(0, 1, len(pow_q2)) * .10

    noise = 1 - np.absolute(noise)

    pow_q2 = pow_q2.mul(noise, axis=0)

    pow_q2_final = pow_q2 * 0.40 + pow_a_final * 0.60

    max_row = [1 / max(row) for index, row in pow_a_final.iterrows()]

    np.random.seed(4)
    noise = np.random.normal(0, 1, len(pow_a)) * .10

    noise = 1 - np.absolute(noise)

    pow_a_final_2 = pow_a_final.mul(max_row, axis=0).mul(noise, axis=0)

    max_row = [1 / max(row) for index, row in pow_q2_final.iterrows()]

    np.random.seed(4)
    noise = np.random.normal(0, 1, len(pow_a)) * .10

    noise = 1 - np.absolute(noise)

    pow_q2_final_2 = pow_q2_final.mul(max_row, axis=0).mul(noise, axis=0)

    max_row = [1 / max(row) for index, row in pow_q1_final.iterrows()]

    np.random.seed(4)
    noise = np.random.normal(0, 1, len(pow_a)) * .10

    noise = 1 - np.absolute(noise)

    pow_q1_final_2 = pow_q1_final.mul(max_row, axis=0).mul(noise, axis=0)

    import colorlover as cl
    from IPython.display import HTML

    colors_all = cl.scales['11']["qual"]["Set3"]

    colors_all.extend(cl.scales['11']["qual"]["Paired"])

    for col in pow_q1_final_2.columns:
        pow_q1_final_2[col] = pow_q1_final_2[col] * .70 + rating_data[rating_data.index == col]["Self Rate"][0] * .30

    for col in pow_q2_final_2.columns:
        pow_q2_final_2[col] = pow_q2_final_2[col] * .70 + rating_data[rating_data.index == col]["Self Rate"][0] * .30

    for col in pow_a_final.columns:
        pow_a_final[col] = pow_a_final[col] * .70 + rating_data[rating_data.index == col]["Full Rate"][0] * .15 + + \
                                                                                                                  rating_data[
                                                                                                                      rating_data.index == col][
                                                                                                                      "Self Rate"][
                                                                                                                      0] * .15

    pow_a_final.columns = [ra + "-ALL " for ra in pow_a_final.columns]

    pow_a_final_T = pow_a_final.T
    pow_a_final_T

    pow_q1_final_2.columns = [ra + "-TQ " for ra in pow_q1_final_2.columns]

    pow_q1_final_2_T = pow_q1_final_2.T

    pow_q2_final_2.columns = [ra + "-PQ " for ra in pow_q2_final_2.columns]

    pow_q2_final_2_T = pow_q2_final_2.T

    dars = pow_a_final_T
    dars = pd.concat((dars, pow_q1_final_2_T), axis=0)
    dars = pd.concat((dars, pow_q2_final_2_T), axis=0)

    dars = dars.sort_index()

    dt[aes] = dars


my_path = os.path.abspath(os.path.dirname('__file__'))
path_in_sent = os.path.join(my_path, "../data/yelp_sentiment/")

pickle.dump(dt, open(path_in_sent + "yelp_sent.p", "wb"))


