import pandas as pd
import os
import _pickle as pickle

my_path = os.path.abspath(os.path.dirname('__file__'))

path = os.path.join(my_path, "../input_fields.csv")

input_fields = pd.read_csv(path)

code = input_fields["code_or_ticker"]

my_path = os.path.abspath(os.path.dirname('__file__'))

path = os.path.join(my_path, "../data/cpickle/")

ext_info_dict = pickle.load(open(path + "ext_info_dict.p", "rb"))

f_df = pd.DataFrame()
for coy in code:
    rad = pd.DataFrame()
    rad["All Target Location File Names"] = ext_info_dict[coy]["All Target Location File Names"]
    rad["All Target Location Small Names"] = ext_info_dict[coy]["All Target Location Small Names"]
    rad["All Target Location Full Addresses"] = ext_info_dict[coy]["All Target Location Full Addresses"]

    lat = []
    lon = []
    for r in list(rad["All Target Location File Names"]):
        lat.append(ext_info_dict[coy]['Figures Dictionary'][coy, r]["Response Data"]["coordinates"]["latitude"])
        lon.append(ext_info_dict[coy]['Figures Dictionary'][coy, r]["Response Data"]["coordinates"]["longitude"])

    rad["lat"] = lat
    rad["lon"] = lon
    rad["Target"] = coy

    f_df = f_df.append(rad)

small_cols = []
#file_names = [s[:-4] for s in big_small_add["All Target Location File Names"]]
for val in f_df["All Target Location File Names"]:
    wa = ""
    for r in val.split("-"):
        wa = wa + r[0]
    small_cols.append(wa)

f_df["Small Code"] = small_cols

f_df.to_csv("../big_small_add.csv")