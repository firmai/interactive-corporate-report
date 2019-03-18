import os
import pandas as pd
import _pickle as pickle
target_code= "BJRI"

my_path = os.path.abspath(os.path.dirname('__file__'))
path_in_file = os.path.join(my_path, "../input_fields.csv")
path = os.path.join(my_path, "../data/cpickle/")
ext_info_dict = pickle.load(open(path + "ext_info_dict.p", "rb"))
path_in_ngrams = os.path.join(my_path, "../data/cpickle/")

input_fields = pd.read_csv(path_in_file)

def run_it(target_small_name, target_long_name, target_code, all_target_location_file_names,
           all_target_location_small_names, all_target_location_full_addresses):
    figures_dict = pickle.load(open(path_in_ngrams + "figures_dict_" + target_code + ".p", "rb"))

    lat_list = []
    lon_list = []
    name_list = []
    avg_ratings = []
    for key, values in figures_dict.items():
        location = key[1]
        lat = values["Response Data"]["coordinates"]["latitude"]
        lon = values["Response Data"]["coordinates"]["longitude"]
        male_prop = values["Male to Female"] / (values["Male to Female"] + 1)
        female_prop = 1 - male_prop
        avg_rating = values["Male"] * male_prop + values["Female"] * female_prop
        avg_ratings.append(avg_rating)
        lat_list.append(lat)
        lon_list.append(lon)

    fig_d = figures_dict[target_code, all_target_location_file_names[0]]

    fa = pd.DataFrame.from_dict(fig_d, orient='index')

    fa.columns = [fa[0][0]]

    fa = fa[1:-1]

    for i in all_target_location_file_names:
        fig_d = figures_dict[target_code, i]

        kar = pd.DataFrame.from_dict(fig_d, orient='index')

        kar.columns = [kar[0][0]]

        kar = kar[1:-1]

        fa[kar.columns[0]] = kar

    fa = fa.iloc[:, 1:]

    fa.iloc[:-2, :] = fa.iloc[:-2, :].apply(pd.to_numeric).round(2)

    nas = pd.DataFrame()

    nas["Small Names"] = all_target_location_small_names
    nas["Addresses"] = all_target_location_full_addresses
    nas["target_code"] = all_target_location_full_addresses
    nas["lat"] = lat_list
    nas["lon"] = lon_list
    nas["Average Rating"] = avg_ratings

    adds = nas[nas["Small Names"].isin([r.title() for r in list(fa.columns)])]["Addresses"]
    latty = nas[nas["Small Names"].isin([r.title() for r in list(fa.columns)])]["lat"]
    lonny = nas[nas["Small Names"].isin([r.title() for r in list(fa.columns)])]["lon"]
    avg = nas[nas["Small Names"].isin([r.title() for r in list(fa.columns)])]["Average Rating"]

    fa.columns = adds

    fa = fa.T
    fa["lat"] = np.array(latty)
    fa["lon"] = np.array(lonny)
    fa["target_small_name"] = target_small_name
    fa["target_long_name"] = target_long_name
    fa["Average Rating"] = np.array(avg)
    return fa


dicly = {}
for target_code in input_fields["code_or_ticker"]:
    target_small_name = \
    input_fields[input_fields["code_or_ticker"] == target_code]["short_name"].reset_index(drop=True)[0]
    target_long_name = input_fields[input_fields["code_or_ticker"] == target_code]["yelp_name"].reset_index(drop=True)[
        0]
    all_target_location_full_addresses = ext_info_dict[target_code]["All Target Location Full Addresses"]
    all_target_location_small_names = ext_info_dict[target_code]["All Target Location Small Names"]
    all_target_location_file_names = ext_info_dict[target_code]["All Target Location File Names"]
    frame = run_it(target_small_name, target_long_name, target_code, all_target_location_file_names,
                   all_target_location_small_names, all_target_location_full_addresses)
    dicly[target_code] = frame

rat = next(iter(dicly.values()))
rat = rat.iloc[:0, :]
for i in dicly.values():
    rat = pd.concat((rat, i), axis=0)

# pickle.dump(rat, open(path_in_ngrams+ "map_dict.p", "wb"))

rat.reset_index(inplace=True)
pickle.dump(rat, open(path_in_ngrams + "map_dict.p", "wb"))