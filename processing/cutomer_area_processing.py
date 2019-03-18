
import os
import pandas as pd
import _pickle as pickle

my_path = os.path.abspath(os.path.dirname('__file__'))
path_in_file = os.path.join(my_path, "../input_fields.csv")
path = os.path.join(my_path, "../data/cpickle/")
ext_info_dict = pickle.load(open(path + "ext_info_dict.p", "rb"))
path_in_ngrams = os.path.join(my_path, "../data/cpickle/")

input_fields = pd.read_csv(path_in_file)



def run_it(target_code,all_target_location_file_names,all_target_location_small_names,all_target_location_full_addresses):

    figures_dict = pickle.load(open(path_in_ngrams + "figures_dict_"+target_code+".p", "rb"))


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

    fa = fa.iloc[:,1:]

    fa.iloc[:-2, :] = fa.iloc[:-2, :].apply(pd.to_numeric).round(2)

    nas = pd.DataFrame()

    nas["Small Names"] = all_target_location_small_names
    nas["Addresses"] = all_target_location_full_addresses

    adds = nas[nas["Small Names"].isin( [ r.title() for r in list(fa.columns)] )]["Addresses"]

    fa.columns = adds

    fa = fa.T
    return fa



dicly = {}
for target_code in input_fields["code_or_ticker"]:

    all_target_location_full_addresses =ext_info_dict[target_code]["All Target Location Full Addresses"]
    all_target_location_small_names = ext_info_dict[target_code]["All Target Location Small Names"]
    all_target_location_file_names = ext_info_dict[target_code]["All Target Location File Names"]
    frame = run_it(target_code,all_target_location_file_names,all_target_location_small_names,all_target_location_full_addresses)
    dicly[target_code] = frame

pickle.dump(dicly, open(path_in_ngrams+ "cutomer_area_dict.p", "wb"))